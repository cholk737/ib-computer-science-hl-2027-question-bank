# Runtime

Bundled Python: `/Users/lucamilo/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`

Available libraries used: pypdf, pdfplumber, Pillow. Poppler `pdftoppm` is on PATH. PyMuPDF/fitz is absent; no installation was required. Source PDFs were read only; rendering created separate PNG evidence. No external browsing or prior-project data was used.

Rebuild inventory with `scripts/inventory_sources.py` then `scripts/enrich_inventory.py`. The first script resets enrichment, so always run both in order. These scripts never change original PDFs. Historical checks are inventory-level only.
