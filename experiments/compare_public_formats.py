"""Small, read-only comparison of public PMC HTML, JATS XML, and PDF.

Inputs belong in an ignored data directory. This reports structural counts and
spot-check anchors; it does not score complete extraction accuracy.
"""

import argparse
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup
from pypdf import PdfReader


ANCHORS = ("method of savings", "30.77", "10.1371/journal.pone.0120644")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(directory: Path, anchors: tuple[str, ...] = ANCHORS) -> dict:
    xml_path, html_path, pdf_path = (directory / f"article.{ext}" for ext in ("xml", "html", "pdf"))
    root = ET.parse(xml_path).getroot()
    body = root.find("body")
    if body is None:
        raise ValueError("JATS article body missing")
    abstract = root.find(".//abstract")
    floats = root.find("floats-group")
    xml_text = re.sub(
        r"\s+", " ",
        " ".join("".join(part.itertext()) for part in (abstract, body, floats) if part is not None),
    )
    soup = BeautifulSoup(html_path.read_bytes(), "html.parser") if html_path.exists() else None
    article = soup.select_one("article") if soup else None
    html_text = article.get_text(" ", strip=True) if article else None
    pdf = PdfReader(pdf_path)
    pdf_text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    texts = {"xml": xml_text, "pdf_pypdf": pdf_text}
    if html_text is not None:
        texts["html"] = html_text
    results = {
        "identity": {
            "doi_xml": next(("".join(e.itertext()) for e in root.findall(".//article-id") if e.get("pub-id-type") == "doi"), None),
            "doi_html": (soup.select_one('meta[name="citation_doi"]') or {}).get("content") if article else None,
        },
        "formats": {
            "xml": {
                "bytes": xml_path.stat().st_size,
                "sha256": sha256(xml_path),
                "abstract_body_and_floats_chars": len(xml_text),
                "tables": len(root.findall(".//table-wrap")),
                "figures": len(root.findall(".//fig")),
                "figures_outside_body": len(root.findall(".//fig")) - len(body.findall(".//fig")),
                "references": len(root.findall(".//ref")),
                "replacement_chars": xml_text.count("\ufffd"),
            },
            "html": ({
                "available": True,
                "bytes": html_path.stat().st_size,
                "sha256": sha256(html_path),
                "article_chars": len(html_text),
                "tables": len(article.select("table.content")),
                "figures": len(article.select("figure.fig")),
                "references": len(article.select("section.ref-list li[id*='.ref']")),
                "replacement_chars": html_text.count("\ufffd"),
            } if article else {"available": False, "reason": "No article element in downloaded HTML"}),
            "pdf_pypdf": {
                "bytes": pdf_path.stat().st_size,
                "sha256": sha256(pdf_path),
                "text_chars": len(pdf_text),
                "pages": len(pdf.pages),
                "replacement_chars": pdf_text.count("\ufffd"),
            },
        },
        "anchors": {
            anchor: {name: anchor.casefold() in text.casefold() for name, text in texts.items()}
            for anchor in anchors
        },
    }
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("--anchor", action="append", dest="anchors", help="Exact text anchor; repeat as needed")
    args = parser.parse_args()
    print(json.dumps(check(args.directory, tuple(args.anchors) if args.anchors else ANCHORS), indent=2, ensure_ascii=False))
