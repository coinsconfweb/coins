#!/usr/bin/env python3
"""
IEEE COINS Website Builder
Usage: python build.py
Reads conference.yml, renders Jinja2 templates → dist/
"""
import os, sys, shutil, yaml, json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup

# Windows consoles often default to a legacy codepage (cp1252) that can't
# encode the ✓ / ✅ characters below — force UTF-8 stdout so builds don't crash.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE   = Path(__file__).parent
TMPL   = BASE / "templates"
STATIC = BASE / "static"
DIST   = BASE / "dist"

# ── load conference data ──────────────────────────────────────
with open(BASE / "conference.yml", encoding="utf-8") as f:
    conf = yaml.safe_load(f)

# ── Jinja2 environment ────────────────────────────────────────
env = Environment(
    loader=FileSystemLoader(str(TMPL)),
    autoescape=select_autoescape(["html"]),
    trim_blocks=True,
    lstrip_blocks=True,
)
# Safely embed Python values as JS literals inside <script> blocks (e.g. the
# program page's COINS_DATA/DAYS/COINS_ROOMS objects). Escaping </>&' guards
# against a value ever containing "</script>" and closing the tag early.
def to_js(value):
    encoded = json.dumps(value)
    for ch, esc in (("<", "\\u003c"), (">", "\\u003e"), ("&", "\\u0026"), ("'", "\\u0027")):
        encoded = encoded.replace(ch, esc)
    return Markup(encoded)

env.filters["tojson"] = to_js

# ── helpers ───────────────────────────────────────────────────
def get_deadline(key):
    """Look up an entry in dates.deadlines by its stable `key` field, so
    templates don't have to index the list positionally (fragile if the
    list is reordered or resized year to year)."""
    for d in conf.get("dates", {}).get("deadlines", []):
        if d.get("key") == key:
            return d
    return {}

env.globals["deadline"] = get_deadline

TITLES = {"prof.", "prof", "dr.", "dr", "mr.", "mr", "ms.", "ms", "mrs.", "mrs"}

def name_initials(name):
    """Initials for a plain name string (used by archive pages, which store
    people as name/affiliation strings rather than structured person objects
    with an explicit `initials` field)."""
    words = [w.strip(".") for w in (name or "").split() if w.strip(".").lower() not in TITLES]
    return "".join(w[0] for w in words[:2]).upper()

env.globals["initials"] = name_initials

def sc_affiliation(person, year=None):
    """Affiliation of a steering-committee member as of a given edition year:
    the first `earlier_affiliations` entry whose `until` covers the year, else
    the current `affiliation` (also used when no year is given)."""
    if year is not None:
        for e in sorted(person.get("earlier_affiliations", []), key=lambda e: e["until"]):
            if int(year) <= e["until"]:
                return e["affiliation"]
    return person.get("affiliation", "")

env.globals["sc_affiliation"] = sc_affiliation

def render(template_name, out_path, extra=None):
    t = env.get_template(template_name)
    ctx = {"conf": conf}
    if extra:
        ctx.update(extra)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(t.render(**ctx), encoding="utf-8")
    print(f"  ✓  {out_path.relative_to(DIST)}")

def rmtree_retry(path, attempts=12, delay=1.0, initial_delay=2.0, fallback_attempts=4):
    """Remove a directory tree robustly on Windows/OneDrive.

    OneDrive can turn a just-created subfolder into an NTFS reparse point
    (cloud placeholder) while it negotiates sync state, which makes
    shutil.rmtree's os.rmdir fail with PermissionError even after the
    normal retry window. This also shows up right after something else
    (e.g. a local preview server) was just using dist/ — the OS/OneDrive
    can hold the lock for a couple seconds after the other process exits.
    An upfront delay plus a longer retry window covers both cases. The
    OS-level `rmdir /s /q` (and PowerShell's Remove-Item) handle the
    reparse-point case reliably, so fall back to it — retried too, since
    it can hit the same transient lock immediately after the shutil loop.
    """
    import time
    time.sleep(initial_delay)
    last_exc = None
    for i in range(attempts):
        try:
            shutil.rmtree(path)
            return
        except PermissionError as e:
            last_exc = e
            time.sleep(delay)
    if os.name == "nt":
        import subprocess
        for i in range(fallback_attempts):
            result = subprocess.run(
                ["cmd", "/c", "rmdir", "/s", "/q", str(path)],
                capture_output=True, text=True,
            )
            if not path.exists():
                return
            time.sleep(delay)
        raise RuntimeError(
            f"Could not remove {path} even via 'rmdir /s /q': {result.stderr.strip()}"
        ) from last_exc
    raise last_exc

# ── clean & rebuild dist ──────────────────────────────────────
if DIST.exists():
    rmtree_retry(DIST)
DIST.mkdir()

# copy static assets
shutil.copytree(STATIC, DIST / "static")

# generate CNAME from conference.yml (meta.domain) so the custom domain
# only needs to be edited in one place
domain = conf.get("meta", {}).get("domain")
if domain:
    (DIST / "CNAME").write_text(domain.strip() + "\n", encoding="utf-8")

# NOTE: .github/workflows is intentionally NOT copied into dist/ — the
# GitHub Actions workflow builds from the source repo and uploads dist/
# as the Pages artifact directly (see .github/workflows/deploy.yml).

# ── frozen past-edition snapshots ───────────────────────────────
# Each past edition's full built site is preserved as a static, self-contained
# snapshot in a source-root folder named after its year (e.g. "2026/", created
# once when that edition became history — see past_editions[].mirror in
# conference.yml). These are plain copies, not templated, so every future
# build just carries them forward into dist/<year>/ unchanged.
import re
for entry in sorted(BASE.iterdir()):
    if entry.is_dir() and re.fullmatch(r"\d{4}", entry.name):
        shutil.copytree(entry, DIST / entry.name)
        print(f"  ✓  {entry.name}/ (frozen snapshot)")

print("\nBuilding IEEE COINS website...\n")

# ── root pages ────────────────────────────────────────────────
render("index.html",        DIST / "index.html")

# ── sub-pages ─────────────────────────────────────────────────
pages = [
    ("cfp.html",            "cfp.html"),
    ("authors.html",        "authors.html"),
    ("proposals.html",      "proposals.html"),
    ("committee.html",      "committee.html"),
    ("outreach.html",       "outreach.html"),
    ("sponsorship.html",    "sponsorship.html"),
    ("program.html",        "program.html"),
    ("keynotes.html",       "keynotes.html"),
    ("tutorials.html",      "tutorials.html"),
    ("competitions.html",   "competitions.html"),
    ("phd-forum.html",      "phd-forum.html"),
    ("workshops.html",      "workshops.html"),
    ("registration.html",   "registration.html"),
    ("venue.html",          "venue.html"),
    ("visa.html",           "visa.html"),
    ("contact.html",        "contact.html"),
]

for tmpl, out in pages:
    render(tmpl, DIST / "pages" / out)

# ── archive pages (one per past edition with recorded content) ─
archives = conf.get("archives", [])
for entry in archives:
    render("archive.html", DIST / "pages" / f"archive-{entry['year']}.html", {"archive": entry})

print(f"\n✅  Build complete → {DIST}\n")
print(f"    Pages generated: {len(pages)+1+len(archives)}")
print(f"    To deploy: push dist/ contents to your GitHub Pages branch.")
