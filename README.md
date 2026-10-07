# IEEE COINS Conference Website

Parametrized static website for the IEEE International Conference on Omni-Layer Intelligent Systems. All content is driven by a single YAML file — no HTML editing required from year to year.

Live site: **https://coinsconf.com** · Repository: **https://github.com/coinsconfweb/coins**

## Quick Start for New Chairs

You do not need to know HTML. The normal loop is: **edit `conference.yml` → preview locally → commit & push → the site updates itself.**

### 1. One-time setup

1. **Get access.** Ask the previous chairs to add your GitHub account to the `coinsconfweb` organization (write access to the `coins` repository). See [Handover Checklist](#handover-checklist) for the other accounts to transfer.
2. **Install tools:** [Git](https://git-scm.com/downloads) and [Python 3.9+](https://www.python.org/downloads/) (on Windows, tick *"Add Python to PATH"* in the installer).
3. **Download the project and install the two Python libraries:**
   ```bash
   git clone https://github.com/coinsconfweb/coins.git coins-website
   cd coins-website
   pip install pyyaml jinja2
   ```

### 2. Every time you update the site

```bash
git pull                      # get the latest version first (others may have edited it)
# ... edit conference.yml (and add images under static/img/) ...
python build.py               # regenerate the site into dist/ — fix any error it prints
cd dist && python -m http.server 8000   # preview at http://localhost:8000, Ctrl+C to stop
cd ..
git add -A
git commit -m "Describe what you changed"
git push
```

After `git push`, GitHub rebuilds and publishes the site automatically in about 1–2 minutes. Check progress (green tick = live, red cross = failed, click it to read the error) under the repository's **Actions** tab. You never upload `dist/` yourself — it is regenerated on every build and is ignored by Git.

> Prefer not to use the command line? Small text edits can be made directly on github.com: open `conference.yml`, click the ✏️ pencil, edit, and *Commit changes*. The site rebuilds the same way. Do preview locally for larger changes, since a YAML mistake stops the whole build.

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
│   ├── contact.html        ← Contact (program chairs auto-populated)
│   ├── archive.html        ← One summary page per pre-2026 edition (from archives[])
│   └── partials/           ← Reusable snippets (person avatars, keynote cards, …)
├── static/
│   ├── css/style.css
│   ├── js/main.js
│   └── img/
│       ├── logos/          ← conference logo + sponsor logos
│       ├── sponsors/       ← (optional) more sponsor logos
│       └── people/         ← headshots, named First_Last.jpg (all editions share this folder)
├── 2026/                   ← Frozen copy of the full 2026 site (plain HTML, never rebuilt)
├── .github/workflows/deploy.yml ← Builds & publishes the site on every push to main
└── dist/                   ← Generated output (not in Git — rebuilt automatically)
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
| EasyChair link, contact email, domain | `meta.easychair_url`, `meta.contact_email`, `meta.domain` |
| Homepage numbers ("12 Technical Tracks"…) | `stats[]` |
| Panels, social events, workshops | `panels[]`, `social_events[]`, `workshops[]` |
| Special sessions | `cfp.special_sessions[]` |
| VISA page | `visa.*` |
| Past editions (nav "Past Events" menu) | `past_editions[]` |
| Archived summary pages for 2019–2025 | `archives[]` |

`conference.yml` itself is commented throughout. For keynotes, tutorials, panels and competitions it contains a commented-out example block (lines starting with `#`) showing every available field — copy it, remove the `# `, and fill it in; for other lists, copy an existing entry. An empty keynote/tutorial/competition list (`[]`) makes that page show a "to be announced" message automatically.

### YAML in 30 seconds

- **Indentation matters** and must use **spaces, never tabs**. Copy an existing entry and keep the same indentation.
- Each list item starts with `- `. Fields belong to the item above them by being indented under it.
- Put text in `"double quotes"`, especially if it contains `:` `#` `&` or starts with a special character. A literal `"` inside must be written `\"`.
- Long paragraphs use `>` on the key line and the text indented on the next lines.
- If `python build.py` fails with a `yaml` error, it prints the line and column — the mistake is usually on that line or just above it.

## Archiving a Past Edition (Rolling Over to a New Year)

Each finished edition's full site is preserved as a permanent, self-contained
snapshot instead of being overwritten. 2026 has already been archived this way
(the `2026/` folder). Example for rolling **2027 → 2028** (replace the years as needed):

1. **Before changing anything for the new year**, `git pull`, build the current
   site and copy its output into a new top-level folder named after the finishing year:
   ```bash
   python build.py
   mkdir 2027
   cp -r dist/index.html dist/pages dist/static 2027/
   ```
   (On Windows without Git Bash, copy those three items from `dist\` into `2027\`
   with File Explorer.) Do **not** copy `dist/CNAME` or the other year folders inside
   `dist/` — those are site-wide. This folder is plain static HTML, never templated
   again: `build.py` copies every top-level folder named with 4 digits into
   `dist/<year>/` on each build, so the snapshot survives every later rebuild
   untouched. (If you ever need to fix something in it, edit its HTML files directly.)
2. Add an entry for that year at the top of `past_editions[]` with a `mirror:` field
   (e.g. `mirror: "2027/index.html"`) instead of `url:` — this makes the
   "Past Events" menu link to the frozen copy.
3. Commit and push the new folder on its own (`git add 2027 conference.yml`,
   `git commit -m "Archive the 2027 site"`, `git push`) so the archive is safe
   before you start editing.
4. Now edit `conference.yml` for the new year (see the table above): `meta.edition`,
   `short_name`, `easychair_url`, `dates.*`, `venue.*`, etc. Reset year-specific
   content (`keynotes`, `tutorials`, `competitions`, `program.days`,
   `cfp.special_sessions`, `committee`, deadlines, venue) to `[]`/`"TBA"` until it
   is known; evergreen content (CFP track taxonomy, sponsorship tiers, steering
   committee, featured activities) can stay as-is.
5. `python build.py`, preview, commit and push as usual.

Editions before 2026 (2019-2025), whose original sites were external, instead have
a condensed single-page summary under `archives[]` in `conference.yml`, published
at `<year>/index.html` (the old `pages/archive-<year>.html` addresses redirect
there) — see `templates/archive.html`. That mechanism only applies to those
legacy years; you normally don't need to touch it.

## Local Development

```bash
pip install pyyaml jinja2               # one-time
python build.py                         # build into dist/
cd dist && python -m http.server 8000   # preview at http://localhost:8000
```

## GitHub Pages Deployment

The site is published by **GitHub Actions** (repository *Settings → Pages → Source: GitHub Actions*).
On every push to `main`, `.github/workflows/deploy.yml`:
1. Installs Python + dependencies
2. Runs `build.py`
3. Deploys `dist/` to GitHub Pages

You can also re-run it by hand from the **Actions** tab → *Build and Deploy to GitHub Pages* → *Run workflow*.
There is no `gh-pages` branch and nothing to upload manually.

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
3. Archived editions (`archives[].general_chairs` / `program_chairs`) accept the same `photo` field. All headshots share the single `static/img/people/` pool (named `First_Last.ext`, ASCII only), so a person who chaired several editions has one file. Don't create top-level `<year>/` folders for photos: `build.py` treats any 4-digit source-root folder as a frozen site snapshot. The frozen 2026 snapshot keeps its own copies in `2026/static/img/people/`.
4. Run `python build.py`. If no photo is set (`photo: ""`), the person's initials are shown in a colored circle instead — nothing looks broken either way.

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

Drop logo files anywhere under `static/img/` (current logos live in `static/img/logos/`; `static/img/sponsors/` is also available). Run `python build.py` after editing.

## Call for Sponsorship Page

`pages/sponsorship.html` is driven entirely by the `sponsorship:` block in `conference.yml`: an intro blurb, a "why sponsor" list, and a `tiers[]` list (name, price, benefits, and an optional `featured: true` to highlight one tier). It also automatically lists `sponsors[]` (with logos, if set) as "Current Sponsors". Edit the tier prices/benefits and `sponsorship.deadline` once they're finalized — everything currently says `"TBA"`.

## Troubleshooting & Pitfalls

| Symptom | Cause / fix |
|---|---|
| `python build.py` prints a `yaml.scanner` / `yaml.parser` error | Indentation or quoting mistake in `conference.yml` at the reported line (see *YAML in 30 seconds*). |
| `archives[<year>] collides with the frozen snapshot folder` | A top-level folder named with a year exists (e.g. `2024/`) for a year that also has an `archives[]` entry. Only use year folders for frozen site snapshots — never to store photos or documents. |
| `ModuleNotFoundError: No module named 'yaml'` / `'jinja2'` | Run `pip install pyyaml jinja2`. |
| An image doesn't show | Path typo or wrong case: paths are case-sensitive on the live server (`Photo.JPG` ≠ `photo.jpg`). Use plain ASCII file names without spaces, e.g. `Jane_Smith.jpg`. |
| Push succeeded but the site didn't change | Open the **Actions** tab: a red ✗ means the build failed (click it for the error). Otherwise wait 1–2 minutes and hard-refresh the browser (Ctrl+F5). |
| `git push` is rejected ("fetch first") | Someone else pushed in the meantime: run `git pull`, then `git push` again. |
| Build fails to delete `dist/` on Windows | Close any preview server (`Ctrl+C`) or File Explorer window showing `dist/`, then retry. In a OneDrive-synced folder the build waits and retries automatically. |

Keep images reasonably small (headshots ≤ ~300 KB, about 400×400 px) so pages load fast.

## Handover Checklist

Everything about the *content* lives in this repository. These accounts and services live **outside** it and must be handed over explicitly by the outgoing chairs:

- [ ] **GitHub** — admin/write access to the `coinsconfweb` organization and the `coins` repository.
- [ ] **Domain `coinsconf.com`** — access to the domain registrar account (renewal and the DNS records listed under *Custom Domain*).
- [ ] **Contact mailbox** `coins@coinsconf.com` (`meta.contact_email`) — who receives it and how to access/forward it.
- [ ] **EasyChair** — create the new year's conference instance and update `meta.easychair_url`.
- [ ] **IEEE / conference management** — registration platform, IEEE conference record, and any payment/registration links used in `registration`.

When you hand over in turn, update this list with anything new and make sure the next chairs can log in to each item before you step down.

## Tech Stack

- **Python** + **Jinja2** — templating engine
- **PyYAML** — YAML parsing
- **Vanilla HTML/CSS/JS** — no frontend framework
- **GitHub Actions** — CI/CD pipeline
- **GitHub Pages** — hosting
