# Pilot dependency record — pypdf

- Candidate/version: `pypdf==7.1.1`, released 2026-11-18; checked 2026-11-25.
- Purpose: extract text from the bundled synthetic, text-layer PDF. No arbitrary PDF upload in the technical pilot.
- License: BSD-3-Clause, per [PyPI metadata](https://pypi.org/project/pypdf/7.1.1/) and installed package metadata. Paideia's own license remains undecided.
- Python/dependencies: Python >=3.10; no mandatory transitive package on Python 3.12 in the installed metadata. Optional extras are not used.
- Maintenance/security: the upstream [release list](https://github.com/py-pdf/pypdf/releases) shows a recent 7.1.1 release with security fixes. The host's preinstalled 6.7.0 has published resource-exhaustion advisories, including [GHSA-jw7q-gvrg-4vj3](https://github.com/py-pdf/pypdf/security/advisories/GHSA-jw7q-gvrg-4vj3); it is not used for the pilot. Latest-version pinning does not eliminate future vulnerability checks.
- Fit: pure Python text extraction, small wheel, no OCR. Scanned documents and complex layouts are outside this pilot. Upstream [text-extraction guidance](https://pypdf.readthedocs.io/en/stable/user/extract-text.html) describes those limits.
- Alternative: Research MCP's PDF processor is currently untracked in its working tree and brings a broader dependency path; compare it on authorized fixtures later.
- Adoption state: pilot only. Reassess extraction fidelity, resource use, and security before importing arbitrary files or promoting this to the user-usable release.
