#!/usr/bin/env bash
set -euo pipefail

SITE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOOLKIT_DIR="${SITE_DIR}/resume_toolkit"
PUBLIC_RESUME="${SITE_DIR}/resume/jasonyuezhang_latest.pdf"

"${TOOLKIT_DIR}/build.sh"

latest_pdf="$(find "${TOOLKIT_DIR}/outputs" -maxdepth 1 -type f -name 'Resume Yue Zhang *.pdf' -print | sort | tail -n 1)"
if [[ -z "${latest_pdf}" ]]; then
  echo "No generated resume PDF found in ${TOOLKIT_DIR}/outputs." >&2
  exit 1
fi

mkdir -p "$(dirname "${PUBLIC_RESUME}")"
cp "${latest_pdf}" "${PUBLIC_RESUME}"
echo "Published ${latest_pdf} -> ${PUBLIC_RESUME}"
