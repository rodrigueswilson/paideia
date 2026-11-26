"""Behavioral checks for the synthetic JATS persistence proof."""

from pathlib import Path
from contextlib import closing
import sqlite3
import tempfile
import unittest

from defusedxml.common import EntitiesForbidden

from format_import_proof import ingest_jats, project_jats, search, verify_quote


DOI = "10.1234/synthetic.1"
SYNTHETIC_JATS = b"""<?xml version="1.0"?>
<!DOCTYPE article SYSTEM "unused-jats.dtd">
<article><front><article-meta>
<article-id pub-id-type="doi">10.1234/synthetic.1</article-id>
<abstract><p>A short invented abstract passage.</p></abstract>
</article-meta></front>
<body><sec><title>Invented method</title>
<p>Delayed recall tests an invented claim.</p>
<table-wrap id="t1"><label>Table 1</label><table><tbody>
<tr><td>Practice</td><td>Review later</td></tr>
</tbody></table></table-wrap></sec></body>
<back><ref-list><ref id="r1"><mixed-citation>Example Author. Synthetic reference.</mixed-citation></ref></ref-list></back>
<floats-group><fig id="f1"><caption><p>Invented figure caption.</p></caption></fig></floats-group>
</article>"""


class FormatImportProofTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.xml = self.root / "invented.xml"
        self.xml.write_bytes(SYNTHETIC_JATS)
        self.db = self.root / "proof.sqlite"

    def test_persist_retrieve_and_reuse_without_source_file(self):
        first = ingest_jats(self.db, "source-1", DOI, self.xml, "synthetic fixture")
        self.assertFalse(first["reused"])
        self.assertTrue(ingest_jats(self.db, "source-1", DOI, self.xml, "synthetic fixture")["reused"])
        self.assertTrue(ingest_jats(self.db, "source-copy", DOI, self.xml, "second fixture origin")["reused"])
        self.xml.unlink()
        for phrase, kind in (
            ("abstract passage", "passage"),
            ("Delayed recall", "passage"),
            ("Review later", "table"),
            ("figure caption", "figure_caption"),
            ("Synthetic reference", "reference"),
        ):
            found = search(self.db, first["run_id"], phrase)
            self.assertEqual(len(found), 1, phrase)
            self.assertEqual(found[0]["kind"], kind)
            self.assertTrue(found[0]["locator"].startswith("/article[1]/"))
            self.assertTrue(verify_quote(found[0], phrase))
            self.assertFalse(verify_quote(found[0], "Invented unsupported quotation"))
        with closing(sqlite3.connect(self.db)) as db:
            self.assertEqual(db.execute("SELECT bytes FROM representations").fetchone()[0], SYNTHETIC_JATS)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM runs").fetchone()[0], 1)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM source_representations").fetchone()[0], 2)
            self.assertEqual(db.execute("SELECT COUNT(DISTINCT source_url) FROM source_representations").fetchone()[0], 2)
        self.assertIsNone(search(self.db, first["run_id"], "Invented method")[0]["native_id"])
        self.assertEqual(search(self.db, first["run_id"], "figure caption")[0]["native_id"], "f1")

    def test_reject_wrong_identity_and_entity(self):
        with self.assertRaises(ValueError):
            ingest_jats(self.db, "source-1", "10.1234/other", self.xml, "synthetic fixture")
        unsafe = b'<!DOCTYPE article [<!ENTITY secret SYSTEM "file:///example">]><article>&secret;</article>'
        with self.assertRaises(EntitiesForbidden):
            project_jats(unsafe, DOI)


if __name__ == "__main__":
    unittest.main()
