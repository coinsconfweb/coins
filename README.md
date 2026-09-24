# IEEE COINS Conference Website

Parametrized static website for the IEEE International Conference on Omni-Layer Intelligent Systems. All content is driven by a single YAML file — no HTML editing required from year to year.

## Project Structure

```
coins-website/
├── conference.yml          ← EDIT THIS EACH YEAR (all content here)
├── build.py                ← Run to regenerate the site
├── templates/
│   ├── base.html           ← Shared nav + footer (reads from YAML)
│   ├── index.html          ← Homepage
│   ├── cfp.html            ← Call for Papers (tracks auto-generated from YAML)
│   ├── authors.html        ← Author's Guide
│   ├── proposals.html      ← Call for Proposals
│   ├── committee.html      ← Conference Committee (auto-generated from YAML)
│   ├── outreach.html       ← Engagement & Outreach / RAS CARES
│   ├── sponsorship.html    ← Call for Sponsorship (tiers + current sponsors, from YAML)
│   ├── program.html        ← Full Schedule (tabbed, days from YAML) + Panelists section
│   ├── keynotes.html       ← Keynote Speakers (cards from YAML)
│   ├── tutorials.html      ← Tutorials (from YAML)
│   ├── competitions.html   ← Competitions (from YAML)
│   ├── phd-forum.html      ← PhD & Student Forum (from YAML)
│   ├── workshops.html      ← Workshops (from YAML)
│   ├── registration.html   ← Registration rates (from YAML)
│   ├── venue.html          ← Venue + photo gallery + hotels (from YAML)
│   ├── visa.html           ← VISA Information
│   └── contact.html        ← Contact (program chairs auto-populated)
├── static/
│   ├── css/style.css
│   ├── js/main.js
│   └── img/
│       ├── coins-logo.png (example) ← conference logo, sponsor logos, etc.
│       └── people/       ← put uploaded headshots here (or link an external URL)
└── dist/                   ← Generated output (deploy this to GitHub Pages)
    ├── index.html
    ├── pages/
    ├── static/
    └── CNAME               ← generated from meta.domain in conference.yml
```

## Updating for a New Year

**Only edit `conference.yml`.** Every piece of content on the site is sourced from it:

| What to update | YAML key |
|---|---|
| Conference year, dates, location | `meta.edition`, `dates.*`, `venue.*` |
| Submission deadlines | `dates.deadlines[]` |
| Venue photos | `venue.photos[]` |
| Keynote speakers | `keynotes[]` |
| Tutorials | `tutorials[]` |
| Competitions | `competitions[]` |
| PhD Forum chairs | `phd_forum.chairs[]` |
| Committee members | `committee[]` |
| Steering Committee (shown on every edition; per-year affiliations via `earlier_affiliations`) | `steering_committee[]` |
| Panelists (Program page) | `panelists[]` |
| Track topics | `cfp.clusters[].tracks[]` |
| Registration rates | `registration.rates[]` |
| Program schedule | `program.days[].sessions[]` |
| Sponsors (+ logos) | `sponsors[]` |
| Sponsorship tiers & benefits | `sponsorship.tiers[]` |
| Conference logo (nav + footer) | `meta.logo` |
| Past editions | `past_editions[]` |

## Archiving a Past Edition (Rolling Over to a New Year)

Starting with the 2026 edition, each finished edition's full site is preserved as a
permanent, self-contained snapshot instead of being overwritten:

1. **Before editing `conference.yml` for the new year**, build the current site
   (`python build.py`) and copy its output into a new source-root folder named after
   that year, e.g.:
   ```bash
   mkdir 2026
   cp -r dist/index.html dist/pages dist/static 2026/
   ```
   (Leave out `dist/CNAME` — that's site-wide, not per-edition.) This folder is
   plain static HTML, never templated again — `build.py` automatically copies any
   source-root folder matching a 4-digit year into `dist/<year>/` on every future
   build, so the snapshot survives every later rebuild untouched.
2. Add an entry for that year to `past_editions[]` with a `mirror:` field pointing
   at it (e.g. `mirror: "2026/index.html"`) instead of `url:` — this makes the
   "Past Events" nav link locally to the frozen mirror rather than an external site.
3. Now edit `conference.yml` for the new year as normal (see the table below).
   Reset year-specific content (`keynotes`, `tutorials`, `competitions`,
   `program.days`, `cfp.special_sessions`, `committee`, deadlines, venue) to
   `[]`/`"TBA"` as it becomes unknown again; evergreen content (CFP track
   taxonomy, sponsorship tiers, featured activities) can stay as-is.

Editions before 2026 (2019-2025), whose own sites live externally and are being
retired, instead get a condensed single-page summary under `archives[]` — see
`templates/archive.html` and `build.py`'s per-entry render loop. That mechanism is
separate from the full-mirror approach above and only applies to those legacy years.

Then run:
```bash
python build.py
```

The rebuilt site lands in `dist/`. Push that to GitHub and you're done.

## Local Development

```bash
# Install dependencies (one-time)
pip install pyyaml jinja2

# Build
python build.py

# Preview (Python's built-in server)
cd dist && python -m http.server 8000
# Open http://localhost:8000
```

## GitHub Pages Deployment

### Option A — Automatic (GitHub Actions)
Push the repository. The `.github/workflows/deploy.yml` workflow automatically:
1. Installs Python + dependencies
2. Runs `build.py`
3. Deploys `dist/` to GitHub Pages

### Option B — Manual
```bash
python build.py
cd dist
git init && git add . && git commit -m "Build"
git push -f origin main:gh-pages
```

### Custom Domain
The `CNAME` file in `dist/` is generated automatically from `meta.domain` in `conference.yml` — change the domain there, not by hand. Add these DNS records at your registrar:

**A records** (point to GitHub Pages IPs):
```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

**CNAME record**:
```
www → <your-github-username>.github.io
```

In GitHub: **Settings → Pages → Custom domain → coinsconf.com**.

## Adding a Keynote Speaker

In `conference.yml`, add an entry under `keynotes:`:

```yaml
keynotes:
  - id: "k5"
    type: "Academic Keynote"      # or "Industrial Keynote"
    name: "Jane Smith"
    affiliation: "MIT, USA"
    title: "The Future of AI Systems"
    abstract: "Abstract text here..."
    bio: "Bio text here..."
    photo: "https://example.com/photo.jpg"  # or leave "" for initials avatar
    day: "Monday, September 7, 2026"
    time: "09:00 – 10:00 CEST"
    confirmed: true
```

Run `python build.py`. The keynote card appears on both the homepage teaser and the keynotes page.

## Adding a Photo for Someone

Every named person on the site — committee members (including track chairs), keynote speakers, tutorial presenters, PhD Forum chairs, and panelists — supports an optional `photo` field (keynotes use `photo`; tutorials use `presenter_photo`). **Normal TPC/reviewer members are not listed individually, so they have no photo field.**

1. Drop the image file into `static/img/people/` (e.g. `static/img/people/jane-smith.jpg`), **or** use a hosted image URL.
2. Set the field to that path/URL:
   ```yaml
   - name: "Jane Smith"
     affiliation: "MIT, USA"
     initials: "JS"          # fallback shown as a colored avatar if no photo
     photo: "static/img/people/jane-smith.jpg"   # or "" to keep the initials avatar
   ```
3. Run `python build.py`. If no photo is set (`photo: ""`), the person's initials are shown in a colored circle instead — nothing looks broken either way.

To add named panelists, fill in the `panelists:` list in `conference.yml` (currently empty — the Program page section is hidden until it has entries).

## Adding the Conference Logo and Sponsor Logos

Same pattern as person photos — a local file under `static/img/` or a hosted URL, and empty means "use the text fallback".

- **Conference logo** (shown in the nav bar and footer, replacing the "IEEE COINS 2026" text badge): set `meta.logo` in `conference.yml`, e.g. `logo: "static/img/coins-logo.png"`.
- **Sponsor logos** (shown on the homepage and the Call for Sponsorship page): add `logo:` to the matching entry under `sponsors[]`, e.g.
  ```yaml
  - name: "IEEE Italy Section"
    role: "Co-Sponsor"
    url: "https://italy.ieeer8.org"
    logo: "static/img/sponsors/ieee-italy.png"   # or "" to keep the text badge
  ```

Drop logo files anywhere under `static/img/` (e.g. `static/img/sponsors/`) — that folder doesn't exist yet, create it when you add the first one. Run `python build.py` after editing.

## Call for Sponsorship Page

`pages/sponsorship.html` is driven entirely by the `sponsorship:` block in `conference.yml`: an intro blurb, a "why sponsor" list, and a `tiers[]` list (name, price, benefits, and an optional `featured: true` to highlight one tier). It also automatically lists `sponsors[]` (with logos, if set) as "Current Sponsors". Edit the tier prices/benefits and `sponsorship.deadline` once they're finalized — everything currently says `"TBA"`.

## Tech Stack

- **Python** + **Jinja2** — templating engine
- **PyYAML** — YAML parsing
- **Vanilla HTML/CSS/JS** — no frontend framework
- **GitHub Actions** — CI/CD pipeline
- **GitHub Pages** — hosting
