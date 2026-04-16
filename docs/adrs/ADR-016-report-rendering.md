# ADR-016: WeasyPrint + python-pptx for Report Rendering

**Status:** Accepted  
**Date:** 2026-04-12  
**Decides:** Libraries for generating PDF and PPTX report outputs

## Decision

WeasyPrint converts HTML/CSS report templates to PDF. python-pptx generates PowerPoint presentations. HTML output is served directly from the template engine (no additional library needed).

## What This Solves

The Report Rendering service (Service_Interface_Contracts.md §11) outputs three formats: PDF, HTML, and PPTX (Report_Template_Specification.md, DDL `report_render.format` enum). This ADR locks the rendering technology for each format.

## Format-to-Library Mapping

| Output Format | Library | How It Works |
|---------------|---------|-------------|
| `html` | Jinja2 (already in FastAPI stack) | Templates render directly to styled HTML |
| `pdf` | WeasyPrint | Same HTML/CSS templates are passed to WeasyPrint, which converts them to PDF |
| `pptx` | python-pptx | Separate PPTX template files with placeholder shapes, populated with data programmatically |

## Report Design Workflow

1. Report templates are designed as HTML + CSS (Jinja2 templates)
2. Data bindings inject scored data, findings, charts, and narrative into templates
3. For PDF: WeasyPrint renders the populated HTML to PDF with print-quality layout
4. For PPTX: A parallel template defines slide layouts; python-pptx fills placeholders with the same bound data
5. Rendered artifacts are stored in S3 with metadata in `report_render`

## Rationale

- **Why WeasyPrint over headless Chrome (Puppeteer/Playwright):** WeasyPrint is pure Python — no external browser binary, no Node.js dependency, no headless Chrome process management. Simpler to deploy and maintain. Print-quality CSS support (@page, margins, headers/footers) is purpose-built.
- **Why not wkhtmltopdf:** Unmaintained, depends on an old Qt WebKit fork. WeasyPrint is actively maintained with modern CSS support.
- **Why python-pptx for PPTX:** It is the only mature Python library for creating/modifying PowerPoint files. No viable alternatives exist.
- **Why HTML-first design:** Report templates only need to be designed once in HTML/CSS. PDF rendering reuses the same templates. This halves the template maintenance burden.

## Implications

- `pyproject.toml` adds `weasyprint`, `python-pptx` dependencies
- WeasyPrint requires system-level dependencies (`pango`, `cairo`, `gdk-pixbuf`) — documented in Dockerfile and local dev setup
- Report templates live in `src/services/report_rendering/templates/` as Jinja2 HTML files
- PPTX templates live alongside as `.pptx` template files
- `docker/docker-compose.yml` does not need changes (WeasyPrint runs in-process)
- Charts are rendered as SVG/PNG and embedded in both HTML and PPTX outputs
