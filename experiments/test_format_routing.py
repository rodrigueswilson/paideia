"""Synthetic route selection, persistence, and fallback checks."""

from contextlib import closing
from pathlib import Path
import sqlite3
import tempfile
import unittest

from reportlab.pdfgen import canvas

from format_import_proof import Candidate, route, search


DOI = "10.1234/synthetic.route"
XML = b"""<article><front><article-meta>
<article-id pub-id-type="doi">10.1234/synthetic.route</article-id>
<abstract><p>Invented XML abstract phrase.</p></abstract>
</article-meta></front><body><sec><title>Invented section</title>
<p>Invented XML body passage.</p></sec></body>
<back><ref-list><ref id="r1">Synthetic citation.</ref></ref-list></back>
<floats-group><fig id="f1"><caption>Invented figure caption.</caption></fig></floats-group>
</article>"""
HTML = b"""<!doctype html><html><head>
<meta name="citation_doi" content="10.1234/synthetic.route"></head>
<body><article><section><h2>HTML section</h2><p>Invented HTML passage.</p>
<table><tr><td>Cell alpha</td><td>Cell beta</td></tr></table>
<figure id="f1"><figcaption>Invented HTML figure.</figcaption></figure>
<div class="ref-list"><li id="r1">Synthetic HTML citation.</li></div>
</section></article></body></html>"""


class SyntheticRoutingTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.db = self.root / "route.sqlite"
        self.xml = self.root / "article.xml"
        self.html = self.root / "article.html"
        self.pdf = self.root / "article.pdf"
        self.xml.write_bytes(XML)
        self.html.write_bytes(HTML)
        pdf = canvas.Canvas(str(self.pdf))
        pdf.drawString(60, 730, "Invented PDF fallback passage.")
        pdf.save()

    def candidate(self, kind, path=None, link_mode="stored"):
        return Candidate(kind, "synthetic fixture origin", path, link_mode)

    def test_verified_xml_wins_and_persists_source_independent_search(self):
        chosen = route(self.db, "source-1", DOI, [
            self.candidate("pdf", self.pdf), self.candidate("html", self.html),
            self.candidate("jats_xml", self.xml),
        ])
        self.assertEqual((chosen["status"], chosen["kind"]), ("selected", "jats_xml"))
        self.assertIn("section_locator_fallback", chosen["review_flags"])
        self.assertIn("figure_evidence_review", chosen["review_flags"])
        self.xml.unlink()
        found = search(self.db, chosen["run_id"], "Invented figure caption")
        self.assertEqual(found[0]["native_id"], "f1")
        self.assertIsNone(found[0]["page"])
        self.assertTrue(found[0]["locator"].startswith("/article[1]/floats-group[1]"))
        with closing(sqlite3.connect(self.db)) as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM representations").fetchone()[0], 1)

    def test_rejected_xml_falls_to_verified_html(self):
        self.xml.write_bytes(XML.replace(DOI.encode(), b"10.1234/wrong"))
        chosen = route(self.db, "source-1", DOI, [
            self.candidate("jats_xml", self.xml), self.candidate("html", self.html),
            self.candidate("pdf", self.pdf),
        ])
        self.assertEqual(chosen["kind"], "html")
        self.assertIn("jats_xml_rejected", chosen["review_flags"])
        self.assertIn("html_structure_review", chosen["review_flags"])
        self.assertIn("table_structure_review", chosen["review_flags"])
        self.html.unlink()
        self.assertEqual(search(self.db, chosen["run_id"], "Cell beta")[0]["kind"], "table")
        self.assertEqual(search(self.db, chosen["run_id"], "HTML figure")[0]["native_id"], "f1")

    def test_link_only_or_browser_check_falls_to_pdf_with_page(self):
        self.html.write_bytes(b"<title>Checking your browser</title>")
        original_pdf = self.pdf.read_bytes()
        chosen = route(self.db, "source-1", DOI, [
            self.candidate("html", None, "linked_url"),
            self.candidate("html", self.html), self.candidate("pdf", self.pdf),
        ])
        self.assertEqual(chosen["kind"], "pdf")
        self.assertIn("html_link_only", chosen["review_flags"])
        self.assertIn("html_rejected", chosen["review_flags"])
        self.assertIn("pdf_identity_unverified", chosen["review_flags"])
        self.assertIn("pdf_structure_review", chosen["review_flags"])
        self.assertTrue(route(self.db, "source-1", DOI, [self.candidate("pdf", self.pdf)])["reused"])
        self.pdf.unlink()
        found = search(self.db, chosen["run_id"], "Invented PDF fallback passage")
        self.assertEqual((found[0]["page"], found[0]["locator"]), (1, "pdf:page:1:line:1"))
        with closing(sqlite3.connect(self.db)) as db:
            self.assertEqual(db.execute("SELECT bytes FROM representations").fetchone()[0], original_pdf)

    def test_no_valid_local_bytes_needs_review_without_storage(self):
        self.html.write_bytes(b"<title>Checking your browser</title>")
        self.pdf.write_bytes(b"not a PDF")
        chosen = route(self.db, "source-1", DOI, [
            self.candidate("html", self.html), self.candidate("pdf", self.pdf),
        ])
        self.assertEqual(chosen["status"], "needs_review")
        self.assertEqual(chosen["review_flags"], ["html_rejected", "pdf_rejected"])
        self.assertFalse(self.db.exists())

    def test_pdf_without_text_layer_is_held_for_review(self):
        image_only = self.root / "image_only.pdf"
        pdf = canvas.Canvas(str(image_only))
        pdf.rect(60, 700, 200, 30, fill=1)
        pdf.save()
        chosen = route(self.db, "source-1", DOI, [self.candidate("pdf", image_only)])
        self.assertEqual(chosen["status"], "needs_review")
        self.assertEqual(chosen["review_flags"], ["pdf_no_text_layer"])
        self.assertFalse(self.db.exists())


if __name__ == "__main__":
    unittest.main()
