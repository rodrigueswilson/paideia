"""Generate a small, entirely synthetic text-layer PDF fixture in memory."""

from __future__ import annotations

SAMPLE_TITLE = "A synthetic note on learning"
SAMPLE_LINES = (
    "Retrieval helps a learner notice what they can recall without looking.",
    "Feedback helps correct an answer after the learner makes an attempt.",
    "A later question can check whether the idea remains available over time.",
)
QUESTIONS = (
    ("What can retrieval reveal before looking at a source?", "It shows what a learner can recall without looking."),
    ("When is feedback most useful in this example?", "After the learner makes an attempt, to correct the answer."),
    ("Why ask a later question?", "To check whether the idea remains available over time."),
)


def sample_pdf() -> bytes:
    """Create a minimal single-page PDF with only public synthetic text."""
    lines = ["BT", "/F1 14 Tf", "50 750 Td"]
    for index, value in enumerate(SAMPLE_LINES):
        escaped = value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        if index:
            lines.append("0 -24 Td")
        lines.append(f"({escaped}) Tj")
    lines.append("ET")
    stream = "\n".join(lines).encode("ascii")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream",
    ]
    result = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for number, obj in enumerate(objects, 1):
        offsets.append(len(result))
        result.extend(f"{number} 0 obj\n".encode())
        result.extend(obj + b"\nendobj\n")
    xref_at = len(result)
    result.extend(f"xref\n0 {len(offsets)}\n0000000000 65535 f \n".encode())
    for offset in offsets[1:]:
        result.extend(f"{offset:010d} 00000 n \n".encode())
    result.extend(
        f"trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{xref_at}\n%%EOF\n".encode()
    )
    return bytes(result)
