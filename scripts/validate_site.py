"""Read-only QA for the public static site. Run from any directory.

Development-only requirements: beautifulsoup4 and tinycss2.
Never print potential secret values in diagnostics.
"""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import sys
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup
import tinycss2

ROOT = Path(__file__).resolve().parents[1]
PREFIX = "/toolglow-lab-site/"
PAGES = ["index.html", "privacy.html", "terms.html", "404.html"]
errors = []
checks = 0


def check(condition, message):
    global checks
    checks += 1
    if not condition:
        errors.append(message)


documents = {name: BeautifulSoup((ROOT / name).read_text(encoding="utf-8"), "html.parser") for name in PAGES}
for name, doc in documents.items():
    check(doc.html and doc.html.get("lang") == "en", f"{name}: missing English language")
    check(len(doc.select("h1")) == 1, f"{name}: expected exactly one h1")
    check(len(doc.select("main")) == 1, f"{name}: expected exactly one main")
    check(bool(doc.title and doc.title.get_text(strip=True)), f"{name}: missing title")
    check(bool(doc.select_one('meta[name="description"]')), f"{name}: missing description")
    check(bool(doc.select_one('meta[name="viewport"]')), f"{name}: missing viewport")
    check(bool(doc.select_one('a.skip-link[href="#main"]')), f"{name}: missing skip link")
    check(bool(doc.select_one('nav[aria-label="Legal navigation"]')), f"{name}: missing legal navigation")
    check(not doc.select("script, iframe, form, object, embed"), f"{name}: unexpected active or embedded content")
    ids = [node["id"] for node in doc.select("[id]")]
    check(len(ids) == len(set(ids)), f"{name}: duplicate IDs")
    for nav in doc.select("nav"):
        check(bool(nav.get("aria-label")), f"{name}: unnamed navigation")
    previous_level = 0
    for heading in doc.select("h1,h2,h3,h4,h5,h6"):
        # A table-of-contents h2 and subsequent article h2 are intentional.
        level = int(heading.name[1])
        check(level <= previous_level + 1, f"{name}: skipped heading level")
        previous_level = level
    for node in doc.select("a[href], link[href], img[src]"):
        value = node.get("href", node.get("src", ""))
        check(bool(value), f"{name}: empty link or asset URL")
        parts = urlsplit(value)
        if parts.scheme or parts.netloc:
            check(parts.scheme in ("https", "mailto"), f"{name}: unsafe or non-HTTPS URL")
            if node.name in ("link", "img"):
                check(node.get("rel") == ["canonical"], f"{name}: external asset dependency")
            continue
        path = unquote(parts.path)
        if path.startswith(PREFIX):
            path = path[len(PREFIX):]
        else:
            check(not path.startswith("/"), f"{name}: incorrect project-relative URL")
        target_name = path or name
        target = ROOT / target_name
        check(target.is_file(), f"{name}: missing local target {target_name}")
        if parts.fragment:
            target_doc = documents.get(target_name)
            check(bool(target_doc and target_doc.find(id=unquote(parts.fragment))), f"{name}: missing fragment in {target_name}")
        if node.name == "a":
            check(bool(node.get_text(strip=True) or node.get("aria-label")), f"{name}: unnamed link")
    for image in doc.select("img"):
        check(image.has_attr("alt"), f"{name}: image missing alternative text")
    for svg in doc.select("svg"):
        check(svg.get("aria-hidden") == "true" or bool(svg.find("title")), f"{name}: SVG lacks accessible treatment")
    footer = doc.select_one("footer")
    for destination in ("privacy.html", "terms.html"):
        check(bool(footer and any(a.get("href", "").endswith(destination) for a in footer.select("a[href]"))), f"{name}: missing footer link to {destination}")


def walk_css(tokens):
    for token in tokens:
        check(token.type != "error", "styles.css: CSS parsing error")
        if token.type == "at-rule" and token.content is not None:
            walk_css(tinycss2.parse_rule_list(token.content, skip_comments=True, skip_whitespace=True))
        elif token.type == "qualified-rule":
            walk_css(tinycss2.parse_declaration_list(token.content, skip_comments=True, skip_whitespace=True))


css = (ROOT / "styles.css").read_text(encoding="utf-8")
walk_css(tinycss2.parse_stylesheet(css, skip_comments=True, skip_whitespace=True))
check("prefers-reduced-motion" in css, "CSS: missing reduced-motion support")
check(":focus-visible" in css, "CSS: missing keyboard focus")
check(not re.search(r"@import|url\(\s*['\"]?https?://", css, re.I), "CSS: external dependency")
check((ROOT / ".nojekyll").is_file(), "Missing .nojekyll")
check((ROOT / "assets/social.png").is_file(), "Missing social image")
ET.parse(ROOT / "assets/favicon.svg")
ET.parse(ROOT / "sitemap.xml")

# Inspect public content, never local QA output or .git credential/config data.
patterns = [
    r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    r"AIza[0-9A-Za-z_-]{35}",
    r"(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})",
    r"1//[A-Za-z0-9_-]{30,}",
    r"ya29\.[A-Za-z0-9_-]{20,}",
    r'"(?:client_secret|refresh_token|access_token)"\s*:\s*"[^"\s]+"',
]
public_files = PAGES + ["styles.css", "README.md", "assets/favicon.svg", "sitemap.xml", ".gitignore"]
for name in public_files:
    content = (ROOT / name).read_text(encoding="utf-8")
    check(not any(re.search(pattern, content) for pattern in patterns), f"{name}: potential secret detected (value withheld)")

if errors:
    print("FAILED:")
    for error in errors:
        print(" -", error)
    sys.exit(1)
print(f"PASS: {checks} structure, navigation, local asset, CSS, accessibility-basics, and secret-pattern checks across {len(PAGES)} HTML pages.")
print("This is not a browser, WCAG certification, or exhaustive credential audit.")
