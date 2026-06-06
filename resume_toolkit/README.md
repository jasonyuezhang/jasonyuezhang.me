# Resume Toolkit

This directory contains the editable resume source for `jasonyuezhang.me`.

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

Generated files are written to `resume_toolkit/outputs/` and ignored by Git.

## Publish To Site

From the site repo root:

```bash
make publish-resume
```

This builds the LaTeX resume and copies the latest generated PDF to:

```text
resume/jasonyuezhang_latest.pdf
```

That PDF is the public file linked from the site.
