#!/usr/bin/env python3
"""build_site.py
Convert all markdown strategy documents in the repository into beautifully styled
HTML files using the template system under `templates/`.

Usage:
    python build_site.py

The script
1. Scans the repository for Markdown files (`*.md`).
2. Converts each to HTML with the Python `markdown` package (with TOC, tables, etc.).
3. Injects the rendered HTML into `templates/base.html` via Jinja2.
4. Writes the output `.html` files alongside their markdown counterparts.

External dependencies: `markdown`, `jinja2`  (add via `pip install -r requirements.txt`).
"""

import pathlib
import datetime
import shutil
import re

import markdown as md
from jinja2 import Environment, FileSystemLoader, select_autoescape

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
ROOT_DIR = pathlib.Path(__file__).resolve().parent
TEMPLATE_DIR = ROOT_DIR / "templates"
STATIC_DIR = ROOT_DIR / "static"
OUTPUT_DIR = ROOT_DIR  # Keeping HTML beside MD for simplicity

MD_EXTENSIONS = [
    "toc",
    "fenced_code",
    "tables",
    "attr_list",
    "admonition",
]

# ---------------------------------------------------------------------------
# Template helpers
# ---------------------------------------------------------------------------

def slug_to_title(slug: str) -> str:
    """Convert filename slug to Title Case string."""
    return slug.replace("_", " ").title()

# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------

def build_html_from_markdown(md_path: pathlib.Path, env: Environment):
    """Render a single markdown file to HTML using the base template."""
    raw_markdown = md_path.read_text(encoding="utf-8")

    # First heading is assumed to be the title
    first_line = raw_markdown.splitlines()[0]
    if first_line.startswith("#"):
        title = first_line.lstrip("# ").strip()
    else:
        title = md_path.stem.replace("_", " ").title()

    # Pre-process: ensure there is a blank line between bold metric headings and following list
    raw_markdown = re.sub(r'(^\*\*[^\n]+\*\*)\n-', r'\1\n\n-', raw_markdown, flags=re.MULTILINE)

    # Convert markdown to HTML
    html_content = md.markdown(raw_markdown, extensions=MD_EXTENSIONS)

    # Post-process links: change *.md hrefs to *.html so that internal navigation works
    html_content = re.sub(r'href="([^"]+?)\.md(#[^"]*)?"',
                          lambda m: f'href="{m.group(1)}.html{m.group(2) or ""}"',
                          html_content)

    template = env.get_template("base.html")

    # Choose hero image based on filename stem
    hero_images = {
        "strategic_partnerships": "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?auto=format&fit=crop&w=1950&q=80",
        "social_proof_credibility": "https://images.unsplash.com/photo-1524253482453-3fed8d2fe12b?auto=format&fit=crop&w=1950&q=80",
        "seo_content_strategy": "https://images.unsplash.com/photo-1531496181981-6c1f5e293b15?auto=format&fit=crop&w=1950&q=80",
        "marketing_strategies": "https://images.unsplash.com/photo-1557425529-b1ae9c2642f4?auto=format&fit=crop&w=1950&q=80",
        "lead_generation_systems": "https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=1950&q=80",
        "growth_measurement_framework": "https://images.unsplash.com/photo-1581091012184-7bcf06b7cb06?auto=format&fit=crop&w=1950&q=80",
        "corporate_offsite_destinations": "https://images.unsplash.com/photo-1502920917128-1aa500764cec?auto=format&fit=crop&w=1950&q=80",
        "competitor_market_analysis": "https://images.unsplash.com/photo-1559521782-9a5f32e1533c?auto=format&fit=crop&w=1950&q=80",
        "implementation_roadmap": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1950&q=80",
    }
    hero_url = hero_images.get(md_path.stem, "https://images.unsplash.com/photo-1542744095-fcf48d80b0fd?auto=format&fit=crop&w=1950&q=80")

    rendered = template.render(
        title=title,
        content=html_content,
        year=datetime.datetime.now().year,
        hero=hero_url,
    )

    output_file = OUTPUT_DIR / f"{md_path.stem}.html"
    output_file.write_text(rendered, encoding="utf-8")
    print(f"✔  Generated {output_file.relative_to(ROOT_DIR)}")

# ---------------------------------------------------------------------------
# Main build routine
# ---------------------------------------------------------------------------

def main():
    # Prepare Jinja2 environment
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=select_autoescape(["html", "xml"]),
    )

    # Copy static assets to output directory if they don't already exist
    dest_static = OUTPUT_DIR / "static"
    if not dest_static.exists():
        shutil.copytree(STATIC_DIR, dest_static)
    else:
        # Sync newer files
        for static_file in STATIC_DIR.rglob("*.*"):
            rel = static_file.relative_to(STATIC_DIR)
            dest_file = dest_static / rel
            if not dest_file.exists() or static_file.stat().st_mtime > dest_file.stat().st_mtime:
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(static_file, dest_file)

    # Build HTML pages from markdown
    md_files = sorted(ROOT_DIR.glob("*.md"))
    for md_path in md_files:
        build_html_from_markdown(md_path, env)

    # Build master index page
    index_template = env.get_template("base.html")
    links_html = "\n".join(
        f'<li><a href="{p.stem}.html">{slug_to_title(p.stem)}</a></li>' for p in md_files
    )
    index_content = f"""
    <h2>Documents</h2>
    <ol>{links_html}</ol>
    <p>Select any strategy document to view its full content.</p>
    """
    index_rendered = index_template.render(title="Trebound Strategy Index",
                                           content=index_content,
                                           year=datetime.datetime.now().year,
                                           hero="https://images.unsplash.com/photo-1542744095-fcf48d80b0fd?auto=format&fit=crop&w=1950&q=80")
    (OUTPUT_DIR / "index.html").write_text(index_rendered, encoding="utf-8")
    print("✔  Generated index.html")


if __name__ == "__main__":
    main() 