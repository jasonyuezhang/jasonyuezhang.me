#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT_DIR="${REPO_DIR}/outputs"
SOURCE_TEX="${REPO_DIR}/resume.tex"
RAW_PDF="${OUT_DIR}/resume.pdf"
FINAL_STEM="${RESUME_STEM:-Resume Yue Zhang 2026}"
FINAL_PDF="${OUT_DIR}/${FINAL_STEM}.pdf"
FINAL_PREVIEW="${OUT_DIR}/${FINAL_STEM}.preview.png"
PYTHON_BIN="${REPO_DIR}/.venv/bin/python"

if ! command -v tectonic >/dev/null 2>&1; then
  echo "Missing tectonic. Install it before building the LaTeX resume." >&2
  exit 1
fi

if [[ ! -x "${PYTHON_BIN}" ]]; then
  echo "Missing local virtual environment. Run:" >&2
  echo "  cd resume_toolkit" >&2
  echo "  python3 -m venv .venv" >&2
  echo "  .venv/bin/python -m pip install -r requirements.txt" >&2
  exit 1
fi

mkdir -p "${OUT_DIR}"

tectonic \
  --keep-logs \
  --synctex \
  --outdir "${OUT_DIR}" \
  "${SOURCE_TEX}"

mv -f "${RAW_PDF}" "${FINAL_PDF}"

"${PYTHON_BIN}" - <<'PY' "${FINAL_PDF}" "${FINAL_PREVIEW}"
from pathlib import Path
import sys
import fitz

pdf_path = Path(sys.argv[1])
preview_path = Path(sys.argv[2])

doc = fitz.open(pdf_path)
pix = doc[0].get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
pix.save(preview_path)
print(pdf_path)
print(preview_path)
PY

rm -f "${OUT_DIR}/resume.log" "${OUT_DIR}/resume.synctex.gz"
