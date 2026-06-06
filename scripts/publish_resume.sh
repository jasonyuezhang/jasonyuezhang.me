#!/usr/bin/env bash
set -euo pipefail

SITE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RESUME_DIR="${SITE_DIR}/resume"
LATEST_LINK="${RESUME_DIR}/jasonyuezhang_latest.pdf"

"${RESUME_DIR}/build.sh"

latest_pdf="$(find "${RESUME_DIR}/outputs" -maxdepth 1 -type f -name 'Resume Yue Zhang *.pdf' -print | sort | tail -n 1)"
if [[ -z "${latest_pdf}" ]]; then
  echo "No generated resume PDF found in ${RESUME_DIR}/outputs." >&2
  exit 1
fi

timestamp="${RESUME_PUBLISH_TIMESTAMP:-$(date +%Y%m%d_%H%M%S)}"
sequence=1
while true; do
  public_name="jasonyuezhang_${timestamp}_$(printf "%03d" "${sequence}").pdf"
  public_resume="${RESUME_DIR}/${public_name}"
  [[ ! -e "${public_resume}" ]] && break
  sequence=$((sequence + 1))
done

cp "${latest_pdf}" "${public_resume}"
rm -f "${LATEST_LINK}"
ln -s "${public_name}" "${LATEST_LINK}"

echo "Published ${latest_pdf} -> ${public_resume}"
echo "Latest resume link: ${LATEST_LINK} -> ${public_name}"
