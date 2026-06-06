# Resume

This directory contains the editable resume source and public downloadable PDFs for `jasonyuezhang.me`.

## Files

- `resume.tex`: canonical LaTeX source for the published PDF
- `resume_meta_propel.toml`: structured resume content for the optional Python renderer
- `generate_resume.py`: optional TOML-to-PDF/text/Markdown renderer
- `build.sh`: builds the LaTeX PDF and preview image into `outputs/`

## Setup

From the site repo root:

```bash
make setup-resume
```

This requires Python 3.11+. The LaTeX build also requires `tectonic`.

## Build

From the site repo root:

```bash
make resume
```

Generated files are written to `resume/outputs/` and ignored by Git.

## Publish To Site

From the site repo root:

```bash
make publish-resume
```

This builds the LaTeX resume, copies it to a timestamped public filename, and updates the latest symlink:

```text
jasonyuezhang_YYYYMMDD_HHMMSS_001.pdf
jasonyuezhang_latest.pdf -> jasonyuezhang_YYYYMMDD_HHMMSS_001.pdf
```

The site links to `jasonyuezhang_latest.pdf`, so downloads always resolve to the latest published resume.
