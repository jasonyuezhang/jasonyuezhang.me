#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 \"Post Title\" [category]" >&2
  exit 1
fi

SITE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TITLE="$1"
CATEGORY="${2:-notes}"
DATE="$(date +%Y-%m-%d)"
TIMEZONE="$(date +%z)"
TIMEZONE="${TIMEZONE:0:3}:${TIMEZONE:3:2}"

slug="$(
  printf '%s' "${TITLE}" |
    tr '[:upper:]' '[:lower:]' |
    sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//'
)"

if [[ -z "${slug}" ]]; then
  echo "Title did not produce a valid slug." >&2
  exit 1
fi

post_path="${SITE_DIR}/_posts/${DATE}-${slug}.markdown"
if [[ -e "${post_path}" ]]; then
  echo "Post already exists: ${post_path}" >&2
  exit 1
fi

cat >"${post_path}" <<EOF
---
layout: post
title: "${TITLE}"
date: $(date '+%Y-%m-%d %H:%M:%S') ${TIMEZONE}
categories: ${CATEGORY}
---

EOF

echo "${post_path}"
