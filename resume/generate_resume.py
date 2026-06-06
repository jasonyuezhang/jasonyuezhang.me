#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
import tomllib
from pathlib import Path

import fitz


PAGE_W = 612
PAGE_H = 792
MARGIN = 40
CONTENT_W = PAGE_W - (2 * MARGIN)
FONT_NAMES = {"regular": "helv", "bold": "hebo", "italic": "heit"}
FONTS = {key: fitz.Font(name) for key, name in FONT_NAMES.items()}


def load_resume(path: Path) -> dict:
    with path.open("rb") as f:
        data = tomllib.load(f)

    transition = data.get("transition_date")
    for entry in data.get("experience", []):
        if entry.get("use_transition_start"):
            entry["start"] = transition
        if entry.get("use_transition_end"):
            entry["end"] = transition
        entry["date"] = f"{entry['start']} - {entry['end']}"
    return data


def width(text: str, font_key: str, size: float) -> float:
    return FONTS[font_key].text_length(text, fontsize=size)


def wrap(text: str, font_key: str, size: float, max_width: float) -> list[str]:
    font = FONTS[font_key]
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if font.text_length(candidate, fontsize=size) <= max_width:
            current = candidate
            continue
        if current:
            lines.append(current)
        current = word
    if current:
        lines.append(current)
    return lines


def put(page: fitz.Page, x: float, y: float, text: str, font_key: str = "regular", size: float = 10) -> None:
    page.insert_text((x, y), text, fontname=FONT_NAMES[font_key], fontsize=size)


def left_right(
    page: fitz.Page,
    y: float,
    left: str,
    right: str,
    left_font: str = "bold",
    right_font: str = "regular",
    left_size: float = 11.4,
    right_size: float = 10.2,
) -> None:
    put(page, MARGIN, y, left, left_font, left_size)
    put(page, PAGE_W - MARGIN - width(right, right_font, right_size), y, right, right_font, right_size)


def bullet(page: fitz.Page, y: float, text: str, size: float = 9.55, leading: float = 11.7) -> float:
    bullet_x = MARGIN + 4
    text_x = MARGIN + 16
    lines = wrap(text, "regular", size, PAGE_W - MARGIN - text_x)
    put(page, bullet_x, y, "•", "regular", size)
    for i, line in enumerate(lines):
        put(page, text_x, y + (i * leading), line, "regular", size)
    return y + (len(lines) * leading)


def render_pdf(data: dict, pdf_path: Path, preview_path: Path) -> None:
    doc = fitz.open()
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    y = 35

    put(page, MARGIN, y, data["name"], "bold", 20)
    y += 19
    put(page, MARGIN, y, data["contact"], "regular", 10.2)
    y += 16

    for line in wrap(data["summary"], "regular", 9.5, CONTENT_W):
        put(page, MARGIN, y, line, "regular", 9.5)
        y += 11.0

    for line in wrap(data["skills"], "regular", 9.3, CONTENT_W):
        put(page, MARGIN, y, line, "regular", 9.3)
        y += 10.8

    y += 7
    put(page, MARGIN, y, "WORK EXPERIENCE", "bold", 10.8)
    y += 5
    page.draw_line((MARGIN, y), (PAGE_W - MARGIN, y), color=(0, 0, 0), width=0.8)
    y += 12

    for entry in data["experience"]:
        left_right(page, y, entry["company"], entry["date"])
        y += 13
        if "role" in entry:
            left_right(page, y, entry["role"], entry["location"], "italic", "regular", 9.8, 9.3)
            y += 11.4
            for item in entry["bullets"]:
                y = bullet(page, y, item)
            y += 7
        else:
            for sub in entry["subroles"]:
                left_right(page, y, sub["role"], sub["location"], "italic", "regular", 9.6, 9.2)
                y += 10.8
                for item in sub["bullets"]:
                    y = bullet(page, y, item)
                y += 4.5
            y += 2

    put(page, MARGIN, y, "EDUCATION", "bold", 10.8)
    y += 5
    page.draw_line((MARGIN, y), (PAGE_W - MARGIN, y), color=(0, 0, 0), width=0.8)
    y += 12
    put(page, MARGIN, y, data["education"]["school"], "bold", 10.4)
    y += 11.5
    put(page, MARGIN, y, data["education"]["degree"], "regular", 9.7)

    if y > PAGE_H - 28:
        raise RuntimeError(f"layout overflow: final_y={y:.1f}")

    doc.save(pdf_path)
    pix = doc[0].get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
    pix.save(preview_path)


def render_text(data: dict) -> str:
    lines = [
        data["name"],
        data["contact"],
        data["summary"],
        data["skills"],
        "",
        "WORK EXPERIENCE",
        "",
    ]
    for entry in data["experience"]:
        lines.append(f"{entry['company']} | {entry['date']}")
        if "role" in entry:
            lines.append(f"{entry['role']} | {entry['location']}")
            lines.extend(f"- {b}" for b in entry["bullets"])
        else:
            for sub in entry["subroles"]:
                lines.append(f"{sub['role']} | {sub['location']}")
                lines.extend(f"- {b}" for b in sub["bullets"])
        lines.append("")
    lines.extend(
        [
            "EDUCATION",
            data["education"]["school"],
            data["education"]["degree"],
        ]
    )
    return "\n".join(lines)


def render_markdown(data: dict) -> str:
    lines = [
        f"# {data['name']}",
        "",
        data["contact"],
        "",
        data["summary"],
        "",
        f"**Skills:** {data['skills']}",
        "",
        "## Work Experience",
        "",
    ]
    for entry in data["experience"]:
        lines.append(f"### {entry['company']} | {entry['date']}")
        if "role" in entry:
            lines.append(f"*{entry['role']} | {entry['location']}*")
            lines.append("")
            lines.extend(f"- {b}" for b in entry["bullets"])
            lines.append("")
        else:
            for sub in entry["subroles"]:
                lines.append(f"*{sub['role']} | {sub['location']}*")
                lines.append("")
                lines.extend(f"- {b}" for b in sub["bullets"])
                lines.append("")
    lines.extend(
        [
            "## Education",
            "",
            f"**{data['education']['school']}**",
            "",
            data["education"]["degree"],
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a one-page PDF resume from TOML.")
    parser.add_argument("source", type=Path, help="Path to the resume TOML file.")
    parser.add_argument("--out-dir", type=Path, default=Path("python_outputs"), help="Output directory.")
    args = parser.parse_args()

    data = load_resume(args.source)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    stem = "Resume Yue Zhang 2026"
    pdf_path = args.out_dir / f"{stem}.pdf"
    txt_path = args.out_dir / f"{stem}.txt"
    md_path = args.out_dir / f"{stem}.md"
    preview_path = args.out_dir / f"{stem}.preview.png"

    render_pdf(data, pdf_path, preview_path)
    txt_path.write_text(render_text(data))
    md_path.write_text(render_markdown(data))

    print(pdf_path)
    print(txt_path)
    print(md_path)
    print(preview_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
