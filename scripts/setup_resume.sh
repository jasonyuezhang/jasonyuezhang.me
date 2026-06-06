#!/usr/bin/env bash
set -euo pipefail

SITE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RESUME_DIR="${SITE_DIR}/resume"

python_bin=""
for candidate in python3.13 python3.12 python3.11 python3; do
  if ! command -v "${candidate}" >/dev/null 2>&1; then
    continue
  fi

  if "${candidate}" - <<'PY'
import sys
raise SystemExit(0 if sys.version_info >= (3, 11) else 1)
PY
  then
    python_bin="${candidate}"
    break
  fi
done

if [[ -z "${python_bin}" ]]; then
  echo "Missing Python 3.11+. Install Python 3.11 or newer before setting up the resume toolkit." >&2
  exit 1
fi

cd "${RESUME_DIR}"
"${python_bin}" -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
