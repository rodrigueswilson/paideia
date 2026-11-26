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


def check(directory: Path) -> dict:
    xml_path, html_path, pdf_path = (directory / f"article.{ext}" for ext in ("xml", "html", "pdf"))
    root = ET.parse(xml_path).getroot()
    body = root.find("body")
    if body is None:
        raise ValueError("JATS article body missing")
    abstract = root.find(".//abstract")
    xml_text = re.sub(
        r"\s+", " ",
        " ".join("".join(part.itertext()) for part in (abstract, body) if part is not None),
    )
    soup = BeautifulSoup(html_path.read_bytes(), "html.parser")
    article = soup.select_one("article")
    if article is None:
        raise ValueError("HTML article element missing")
    html_text = article.get_text(" ", strip=True)
    pdf = PdfReader(pdf_path)
    pdf_text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    texts = {"xml": xml_text, "html": html_text, "pdf_pypdf": pdf_text}
    results = {
        "identity": {
            "doi_xml": next(("".join(e.itertext()) for e in root.findall(".//article-id") if e.get("pub-id-type") == "doi"), None),
            "doi_html": (soup.select_one('meta[name="citation_doi"]') or {}).get("content"),
        },
        "formats": {
            "xml": {
                "bytes": xml_path.stat().st_size,
                "sha256": sha256(xml_path),
                "abstract_and_body_chars": len(xml_text),
                "tables": len(root.findall(".//table-wrap")),
                "figures": len(root.findall(".//fig")),
                "references": len(root.findall(".//ref")),
                "replacement_chars": xml_text.count("\ufffd"),
            },
            "html": {
                "bytes": html_path.stat().st_size,
                "sha256": sha256(html_path),
                "article_chars": len(html_text),
                "tables": len(article.select("table.content")),
                "figures": len(article.select("figure.fig")),
                "references": len(article.select("section.ref-list li[id*='.ref']")),
                "replacement_chars": html_text.count("\ufffd"),
            },
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
            for anchor in ANCHORS
        },
    }
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    print(json.dumps(check(args.directory), indent=2, ensure_ascii=False))
