# Custom GitHub Profile README Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create and deploy a highly polished, monochromatic, automated custom GitHub profile README for Reinhart-py containing custom hero banners, automated GitHub stats, contribution snake, and projects panel.

**Architecture:** We will set up automated python scripts to fetch project metrics and render them to SVGs inside GitHub actions. Visuals are theme-aware and use a slate-grey/monochromatic design.

**Tech Stack:** GitHub Actions, Python 3, SVG/XML, Markdown.

---

### Task 1: Setup Projects Configuration

**Files:**
- Create: `projects.json`

- [ ] **Step 1: Write `projects.json` containing metadata for the 6 selected repositories**

Create `projects.json` with the following content:
```json
[
  {
    "name": "Orange-carrier",
    "repo": "Reinhart-py/Orange-carrier",
    "description": "Python bot for real-time OrangeCarrier CDR monitoring with cinematic terminal UI and instant Telegram alerts",
    "tags": ["Python", "Terminal UI", "Telegram Bot"]
  },
  {
    "name": "flipbook",
    "repo": "Reinhart-py/flipbook",
    "description": "Web-based flipbook viewer engine and visualizer",
    "tags": ["JavaScript", "HTML", "GPL"]
  },
  {
    "name": "Crow",
    "repo": "Reinhart-py/Crow",
    "description": "A specialized GitHub username checker utility written in Python",
    "tags": ["Python", "GitHub API", "CLI"]
  },
  {
    "name": "Ella",
    "repo": "Reinhart-py/Ella",
    "description": "A 5-letter username finder and checker for Instagram and Threads",
    "tags": ["Python", "Social Media", "Automation"]
  },
  {
    "name": "ESA",
    "repo": "Reinhart-py/ESA",
    "description": "Full-stack application built using TypeScript and modern web tech",
    "tags": ["TypeScript", "Full-Stack"]
  },
  {
    "name": "Boutique",
    "repo": "Reinhart-py/Boutique",
    "description": "Modern online storefront built with React and TypeScript",
    "tags": ["TypeScript", "React", "Frontend"]
  }
]
```

- [ ] **Step 2: Verify `projects.json` is valid JSON format**
Run: `node -e "JSON.parse(require('fs').readFileSync('projects.json'))"`
Expected: Exit code 0 (no output, parses successfully)

---

### Task 2: Create Monochromatic Banner SVGs

**Files:**
- Create: `dark.svg`
- Create: `light.svg`

- [ ] **Step 1: Write `dark.svg` using a beautiful slate-monochromatic style**
Create `dark.svg` containing:
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 400" width="100%" height="100%">
  <rect width="100%" height="100%" fill="#0F172A"/>
  <!-- Grid lines -->
  <path d="M 0 50 L 1200 50 M 0 100 L 1200 100 M 0 150 L 1200 150 M 0 200 L 1200 200 M 0 250 L 1200 250 M 0 300 L 1200 300 M 0 350 L 1200 350" stroke="#1E293B" stroke-width="1" stroke-opacity="0.3"/>
  <path d="M 100 0 L 100 400 M 200 0 L 200 400 M 300 0 L 300 400 M 400 0 L 400 400 M 500 0 L 500 400 M 600 0 L 600 400 M 700 0 L 700 400 M 800 0 L 800 400 M 900 0 L 900 400 M 1000 0 L 1000 400 M 1100 0 L 1100 400" stroke="#1E293B" stroke-width="1" stroke-opacity="0.3"/>
  <!-- Decorative Glow -->
  <circle cx="600" cy="200" r="180" fill="#64748B" opacity="0.1" filter="blur(40px)"/>
  <!-- Title -->
  <text x="600" y="190" text-anchor="middle" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="64" font-weight="800" fill="#F8FAFC" letter-spacing="8">REINHART</text>
  <!-- Subtitle -->
  <text x="600" y="240" text-anchor="middle" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="18" fill="#94A3B8" letter-spacing="4">Full-Stack Engineer | Dev Tools &amp; Automation</text>
  <!-- Terminal Prompt Deco -->
  <text x="40" y="360" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="14" fill="#475569">> reinhart.py --status</text>
  <text x="40" y="380" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="14" fill="#64748B">> active_threads: 6 | uptime: 100%</text>
</svg>
```

- [ ] **Step 2: Write `light.svg` using a clean light-mode slate-monochromatic style**
Create `light.svg` containing:
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 400" width="100%" height="100%">
  <rect width="100%" height="100%" fill="#F8FAFC"/>
  <!-- Grid lines -->
  <path d="M 0 50 L 1200 50 M 0 100 L 1200 100 M 0 150 L 1200 150 M 0 200 L 1200 200 M 0 250 L 1200 250 M 0 300 L 1200 300 M 0 350 L 1200 350" stroke="#E2E8F0" stroke-width="1" stroke-opacity="0.5"/>
  <path d="M 100 0 L 100 400 M 200 0 L 200 400 M 300 0 L 300 400 M 400 0 L 400 400 M 500 0 L 500 400 M 600 0 L 600 400 M 700 0 L 700 400 M 800 0 L 800 400 M 900 0 L 900 400 M 1000 0 L 1000 400 M 1100 0 L 1100 400" stroke="#E2E8F0" stroke-width="1" stroke-opacity="0.5"/>
  <!-- Decorative Glow -->
  <circle cx="600" cy="200" r="180" fill="#94A3B8" opacity="0.1" filter="blur(40px)"/>
  <!-- Title -->
  <text x="600" y="190" text-anchor="middle" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="64" font-weight="800" fill="#0F172A" letter-spacing="8">REINHART</text>
  <!-- Subtitle -->
  <text x="600" y="240" text-anchor="middle" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="18" fill="#475569" letter-spacing="4">Full-Stack Engineer | Dev Tools &amp; Automation</text>
  <!-- Terminal Prompt Deco -->
  <text x="40" y="360" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="14" fill="#94A3B8">> reinhart.py --status</text>
  <text x="40" y="380" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="14" fill="#475569">> active_threads: 6 | uptime: 100%</text>
</svg>
```

---

### Task 3: Set up Scripts and Workflows

**Files:**
- Create: `.github/scripts/fetch_data.py`
- Create: `.github/scripts/generate_projects.py`
- Create: `.github/workflows/projects.yml`
- Create: `.github/workflows/snake.yml`

- [ ] **Step 1: Write `.github/scripts/fetch_data.py`**
Use `fetch_data.py` from arifhaxn. Write to `.github/scripts/fetch_data.py`.
```python
import json, os, sys, urllib.request

TOKEN = os.environ.get("GITHUB_TOKEN", "")

def gh(url):
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {TOKEN}" if TOKEN else "",
        "User-Agent": "projects-panel",
    })
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.load(r)

def main():
    with open("projects.json") as f:
        projects = json.load(f)
    for p in projects:
        repo = p.get("repo", "").strip()
        repo = repo.replace("https://github.com/", "").replace("http://github.com/", "").rstrip("/")
        p["repo"] = repo
        try:
            info = gh(f"https://api.github.com/repos/{repo}")
            p["stars"] = info.get("stargazers_count", 0)
            p["pushed_at"] = info.get("pushed_at")
            if not p.get("description"):
                p["description"] = info.get("description") or ""
            p["languages"] = gh(f"https://api.github.com/repos/{repo}/languages")
        except Exception as e:
            print(f"warn: could not fetch {repo}: {e}", file=sys.stderr)
            p.setdefault("stars", 0)
            p.setdefault("languages", {})
            p.setdefault("pushed_at", None)
    with open("merged.json", "w") as f:
        json.dump(projects, f)
    print(f"merged {len(projects)} projects")

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Write `.github/scripts/generate_projects.py` with Monochromatic palette**
```python
import json, base64, os, sys, math, html
from datetime import datetime, timezone

# ---------------- monochromatic themes ----------------
THEMES = {
    "dark": {
        "BG": "#0F172A", "PANEL": "#1E293B", "PANEL_BAR": "#0F172A",
        "CYAN": "#64748B", "VIOLET": "#94A3B8", "VIOLET2": "#64748B",
        "EMERALD": "#94A3B8", "TEXT": "#F8FAFC", "MUTED": "#94A3B8",
        "DIM": "#475569",
        "STROKE": "rgba(148,163,184,0.28)", "STROKE_HI": "rgba(148,163,184,0.5)",
        "STROKE_LO": "rgba(148,163,184,0.22)", "BARLINE": "rgba(255,255,255,0.08)",
        "RING_BG": "rgba(148,163,184,0.15)", "PILL_BG": "rgba(148,163,184,0.15)",
        "PILL_STROKE": "rgba(148,163,184,0.4)", "MONO_TX": "#F8FAFC",
    },
    "light": {
        "BG": "#F8FAFC", "PANEL": "#FFFFFF", "PANEL_BAR": "#F1F5F9",
        "CYAN": "#475569", "VIOLET": "#64748B", "VIOLET2": "#94A3B8",
        "EMERALD": "#475569", "TEXT": "#0F172A", "MUTED": "#475569",
        "DIM": "#94A3B8",
        "STROKE": "rgba(71,85,105,0.30)", "STROKE_HI": "rgba(71,85,105,0.55)",
        "STROKE_LO": "rgba(71,85,105,0.20)", "BARLINE": "rgba(0,0,0,0.08)",
        "RING_BG": "rgba(100,116,139,0.20)", "PILL_BG": "rgba(100,116,139,0.12)",
        "PILL_STROKE": "rgba(100,116,139,0.4)", "MONO_TX": "#0F172A",
    },
}

# active palette — set by set_theme(); defaults to dark
BG = PANEL = PANEL_BAR = CYAN = VIOLET = VIOLET2 = EMERALD = TEXT = MUTED = DIM = None
STROKE = STROKE_HI = STROKE_LO = BARLINE = RING_BG = PILL_BG = PILL_STROKE = MONO_TX = None
DONUT_COLORS = []

def set_theme(name):
    t = THEMES[name]
    g = globals()
    for k, v in t.items():
        g[k] = v
    g["DONUT_COLORS"] = [t["VIOLET"], t["CYAN"], t["EMERALD"], "#475569", "#64748B", "#94A3B8"]

set_theme("dark")

W        = 1180
CARD_W   = 578
CARD_H   = 168
GAP      = 14
MARGIN   = 5
FONT     = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

def esc(s): return html.escape(str(s), quote=True)

def rel_time(iso):
    if not iso: return "n/a"
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        d = (datetime.now(timezone.utc) - dt)
        if d.days > 365: return f"{d.days//365}y ago"
        if d.days > 30:  return f"{d.days//30}mo ago"
        if d.days > 0:   return f"{d.days}d ago"
        h = d.seconds // 3600
        return f"{h}h ago" if h else "just now"
    except Exception:
        return "n/a"

def wrap_text(s, max_chars, max_lines=2):
    words = s.split()
    lines, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= max_chars:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur); cur = w
            if len(lines) == max_lines: break
    if cur and len(lines) < max_lines: lines.append(cur)
    if len(lines) == max_lines and words and " ".join(lines).count(" ") + 1 < len(words):
        lines[-1] = lines[-1][:max_chars-1].rstrip() + "…"
    return lines

def donut_segments(languages, cx, cy, r, begin):
    total = sum(languages.values()) or 1
    entries = sorted(languages.items(), key=lambda kv: -kv[1])[:4]
    other = total - sum(v for _, v in entries)
    if other > 0: entries.append(("Other", other))
    C = 2 * math.pi * r
    out, legend = [], []
    offset = 0.0
    t = begin
    for i, (lang, v) in enumerate(entries):
        frac = v / total
        seg = frac * C
        col = DONUT_COLORS[i % len(DONUT_COLORS)]
        out.append(
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="9" '
            f'stroke-dasharray="{seg:.2f} {C - seg:.2f}" stroke-dashoffset="{-offset:.2f}" '
            f'transform="rotate(-90 {cx} {cy})" opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" dur="0.01s" begin="{t:.2f}s" fill="freeze"/>'
            f'<animate attributeName="stroke-dasharray" from="0 {C:.2f}" to="{seg:.2f} {C - seg:.2f}" '
            f'dur="0.6s" begin="{t:.2f}s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines="0.3 0 0.2 1"/>'
            f'</circle>')
        legend.append((lang, frac, col))
        offset += seg
        t += 0.18
    return "".join(out), legend

def card(p, x, y, idx):
    b = 0.25 + idx * 0.15
    e = []
    a = e.append
    repo = p.get("repo", "").strip()
    repo = repo.replace("https://github.com/", "").replace("http://github.com/", "")
    repo = repo.rstrip("/")
    href = f"https://github.com/{esc(repo)}"
    a(f'<a href="{href}" target="_blank">')
    a(f'<g opacity="0" transform="translate({x},{y})">')
    a(f'<animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="{b:.2f}s" fill="freeze"/>')

    a(f'<rect width="{CARD_W}" height="{CARD_H}" rx="12" fill="{PANEL}" stroke="{STROKE}">'
      f'<animate attributeName="stroke" values="{STROKE_LO};{STROKE_HI};{STROKE_LO}" '
      f'dur="4.5s" begin="{b+idx*0.7:.2f}s" repeatCount="indefinite"/></rect>')
    a(f'<rect width="{CARD_W}" height="30" rx="12" fill="{PANEL_BAR}"/>')
    a(f'<rect y="18" width="{CARD_W}" height="12" fill="{PANEL_BAR}"/>')
    a(f'<line x1="0" y1="30" x2="{CARD_W}" y2="30" stroke="{BARLINE}"/>')
    a(f'<text x="16" y="19" font-size="10" fill="{MUTED}"><tspan fill="{CYAN}">&#8226;</tspan> {esc(repo)}</text>')

    days = 999
    try:
        dt = datetime.fromisoformat(p.get("pushed_at", "").replace("Z", "+00:00"))
        days = (datetime.now(timezone.utc) - dt).days
    except Exception:
        pass
    if days <= 14:
        a(f'<circle cx="{CARD_W-16}" cy="15" r="3.5" fill="{CYAN}">'
          f'<animate attributeName="opacity" values="1;0.25;1" dur="1.8s" repeatCount="indefinite"/></circle>')
    else:
        a(f'<circle cx="{CARD_W-16}" cy="15" r="3.5" fill="{DIM}"/>')

    initial = esc((p.get("name") or "?")[0].upper())
    float_anim = (f'<animateTransform attributeName="transform" type="translate" '
                  f'values="0 0; 0 -2.5; 0 0" dur="5s" begin="{b+idx*0.5:.2f}s" '
                  f'repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" '
                  f'keySplines="0.4 0 0.6 1;0.4 0 0.6 1"/>')
    a(f'<g>{float_anim}<rect x="16" y="44" width="40" height="40" rx="9" fill="{VIOLET2}" opacity="0.9"/>'
      f'<text x="36" y="71" text-anchor="middle" font-size="20" font-weight="700" fill="{MONO_TX}">{initial}</text></g>')

    name = esc(p.get("name", "unnamed"))
    a(f'<text x="68" y="61" font-size="17" font-weight="700" fill="{TEXT}">{name}'
      f'<tspan fill="{CYAN}">_<animate attributeName="opacity" values="1;0;1" dur="1.2s" '
      f'begin="{b+0.4:.2f}s" repeatCount="indefinite"/></tspan></text>')

    for i, line in enumerate(wrap_text(p.get("description", ""), 52)):
        a(f'<text x="68" y="{80 + i * 16}" font-size="11" fill="{MUTED}">{esc(line)}</text>')

    tx = 68
    for tag in (p.get("tags") or [])[:3]:
        tw = len(tag) * 6.6 + 14
        a(f'<rect x="{tx}" y="118" width="{tw:.0f}" height="17" rx="8.5" fill="{PILL_BG}" stroke="{PILL_STROKE}"/>')
        a(f'<text x="{tx + tw/2:.0f}" y="130" text-anchor="middle" font-size="9.5" fill="{VIOLET}">{esc(tag)}</text>')
        tx += tw + 7

    stars = p.get("stars", 0)
    a(f'<text x="68" y="155" font-size="11" fill="{MUTED}">'
      f'<tspan fill="{CYAN}">&#9733;</tspan> {stars}'
      f'<tspan fill="{DIM}" dx="14">updated {rel_time(p.get("pushed_at"))}</tspan></text>')

    langs = p.get("languages") or {}
    if langs:
        cx, cy, r = CARD_W - 58, CARD_H // 2 + 6, 27
        segs, legend = donut_segments(langs, cx, cy, r, b + 0.3)
        a(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{RING_BG}" stroke-width="9"/>')
        a(segs)
        top = legend[0]
        a(f'<text x="{cx}" y="{cy+4}" text-anchor="middle" font-size="11" font-weight="700" fill="{TEXT}">{top[1]*100:.0f}%</text>')
        dot_x = cx - r - 92
        text_x = dot_x + 9
        ly = cy - 22
        for lang, frac, col in legend[:3]:
            a(f'<circle cx="{dot_x}" cy="{ly}" r="3.5" fill="{col}"/>')
            a(f'<text x="{text_x}" y="{ly+4}" font-size="10" fill="{MUTED}">{esc(lang)} {frac*100:.0f}%</text>')
            ly += 18
    a('</g>')
    a('</a>')
    return "".join(e)

def build(projects, theme="dark"):
    rows = math.ceil(len(projects) / 2)
    H = 56 + rows * (CARD_H + GAP) + MARGIN
    gid = f"acc_{theme}"
    s = []
    a = s.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
      f'font-family="{FONT}" role="img" aria-label="Projects">')
    a(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    a(f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0">'
      f'<stop offset="0" stop-color="{VIOLET2}"><animate attributeName="stop-color" values="{VIOLET2};{CYAN};{EMERALD};{VIOLET2}" dur="10s" repeatCount="indefinite"/></stop>'
      f'<stop offset="1" stop-color="{EMERALD}"><animate attributeName="stop-color" values="{EMERALD};{VIOLET2};{CYAN};{EMERALD}" dur="10s" repeatCount="indefinite"/></stop>'
      '</linearGradient></defs>')
    a(f'<text x="{MARGIN+2}" y="18" font-size="11" letter-spacing="2" fill="{CYAN}">PROJECTS.LIST</text>')
    a(f'<text x="{MARGIN+130}" y="18" font-size="10" fill="{DIM}">./projects.sh --all</text>')
    a(f'<line x1="{MARGIN}" y1="28" x2="{W-MARGIN}" y2="28" stroke="url(#{gid})" stroke-width="1.5" opacity="0.7"/>')
    for i, p in enumerate(projects):
        x = MARGIN + (i % 2) * (CARD_W + GAP + 4)
        y = 42 + (i // 2) * (CARD_H + GAP)
        a(card(p, x, y, i))
    a('</svg>')
    return "".join(s)

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "merged.json"
    outdir = sys.argv[2] if len(sys.argv) > 2 else "."
    with open(src) as f:
        projects = json.load(f)
    for p in projects:
        p["_logo_b64"] = None
    for theme, fname in (("dark", "projects.svg"), ("light", "projects-light.svg")):
        set_theme(theme)
        svg = build(projects, theme)
        path = os.path.join(outdir, fname)
        with open(path, "w") as f:
            f.write(svg)
        print(f"wrote {path}: {theme}, {len(projects)} projects, {len(svg)//1024}KB")
```

- [ ] **Step 3: Write `.github/workflows/projects.yml`**
Create `.github/workflows/projects.yml` with the checkout actions and python scripts execution:
```yaml
name: Generate Projects Panel

on:
  push:
    branches: [main]
    paths:
      - "projects.json"
      - ".github/scripts/generate_projects.py"
      - ".github/scripts/fetch_data.py"
  schedule:
    - cron: "0 */6 * * *"
  workflow_dispatch:

jobs:
  generate:
    permissions:
      contents: write
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Fetch live repo data
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: python3 .github/scripts/fetch_data.py

      - name: Generate projects.svg
        run: |
          mkdir -p out
          python3 .github/scripts/generate_projects.py merged.json out

      - name: Push to projects branch
        uses: crazy-max/ghaction-github-pages@v3.1.0
        with:
          target_branch: projects
          build_dir: out
          commit_message: "Update projects panel [skip ci]"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

- [ ] **Step 4: Write `.github/workflows/snake.yml`**
Create `.github/workflows/snake.yml` to generate the contribution snake SVG:
```yaml
name: Generate Contribution Snake

on:
  schedule:
    - cron: "0 0 * * *"
  workflow_dispatch:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Generate contribution snake
        uses: Platane/snk@v3
        with:
          github_user_name: Reinhart-py
          outputs: |
            dist/snake-light.svg?color_snake=#475569&color_dots=#F1F5F9,#CBD5E1,#94A3B8,#475569,#0F172A
            dist/snake-dark.svg?palette=github-dark&color_snake=#94A3B8&color_dots=#0F172A,#1E293B,#475569,#94A3B8,#F8FAFC
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Push output
        uses: crazy-max/ghaction-github-pages@v3.1.0
        with:
          target_branch: output
          build_dir: dist
          commit_message: "Update contribution snake [skip ci]"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

### Task 4: Write New Profile README

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Overwrite `README.md` with beautiful layout and content**
Combine Reinhart's text content and the interactive stats and SVG elements using a monochromatic design.

Write `README.md` containing:
```markdown
<!-- ===== THEME-AWARE HERO BANNER ===== -->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Reinhart-py/Reinhart-py/main/dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Reinhart-py/Reinhart-py/main/light.svg">
  <img alt="Reinhart" src="https://raw.githubusercontent.com/Reinhart-py/Reinhart-py/main/light.svg">
</picture>

# Reinhart

Full-stack engineer focused on building reliable software, developer tools, automation, and scalable backend systems.

I enjoy solving difficult engineering problems, improving existing products, and helping developers debug, optimize, and ship software faster. My work ranges from modern web applications and mobile apps to bots, APIs, infrastructure, and developer tooling.

---

<!-- ===== GITHUB STATS ===== -->
<div align="center">

<!-- Streak — full width -->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://streak-stats.demolab.com/?user=Reinhart-py&hide_border=true&background=0F172A&stroke=475569&ring=94A3B8&fire=64748B&currStreakLabel=94A3B8&sideLabels=475569&currStreakNum=F8FAFC&sideNums=F8FAFC&dates=475569&titleColor=94A3B8&card_width=1180" />
  <img width="100%" src="https://streak-stats.demolab.com/?user=Reinhart-py&hide_border=true&background=FFFFFF&stroke=E2E8F0&ring=475569&fire=475569&currStreakLabel=475569&sideLabels=475569&currStreakNum=0F172A&sideNums=0F172A&dates=94A3B8&titleColor=475569&card_width=1180" alt="Reinhart's streak" />
</picture>

<br/>

<!-- Stats + Top languages — side by side -->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats-sigma-rosy-28.vercel.app/api?username=Reinhart-py&show_icons=true&count_private=true&include_all_commits=true&hide_rank=true&hide_border=true&title_color=94A3B8&icon_color=64748B&text_color=94A3B8&bg_color=0F172A&card_width=500" />
  <img width="49%" src="https://github-readme-stats-sigma-rosy-28.vercel.app/api?username=Reinhart-py&show_icons=true&count_private=true&include_all_commits=true&hide_rank=true&hide_border=true&title_color=475569&icon_color=94A3B8&text_color=0F172A&bg_color=FFFFFF&card_width=500" alt="Reinhart's GitHub stats" />
</picture>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats-sigma-rosy-28.vercel.app/api/top-langs/?username=Reinhart-py&layout=compact&langs_count=8&hide_border=true&title_color=94A3B8&text_color=94A3B8&bg_color=0F172A&card_width=500" />
  <img width="49%" src="https://github-readme-stats-sigma-rosy-28.vercel.app/api/top-langs/?username=Reinhart-py&layout=compact&langs_count=8&hide_border=true&title_color=475569&text_color=0F172A&bg_color=FFFFFF&card_width=500" alt="Top languages" />
</picture>

</div>

---

<!-- ===== DYNAMIC PROJECTS PANEL ===== -->
<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Reinhart-py/Reinhart-py/projects/projects.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Reinhart-py/Reinhart-py/projects/projects-light.svg">
    <img width="100%" src="https://raw.githubusercontent.com/Reinhart-py/Reinhart-py/projects/projects.svg" alt="Projects" />
  </picture>
</div>

---

<!-- ===== CONTRIBUTION SNAKE ===== -->
<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Reinhart-py/Reinhart-py/output/snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Reinhart-py/Reinhart-py/output/snake-light.svg" />
  <img alt="Snake eating my contributions" src="https://raw.githubusercontent.com/Reinhart-py/Reinhart-py/output/snake-light.svg" />
</picture>
</div>

---

## Technical Stack

<table>
  <tr>
    <td valign="top" width="25%">
      <strong>Frontend</strong><br/>
      • HTML<br/>
      • CSS<br/>
      • JavaScript<br/>
      • TypeScript<br/>
      • React / Next.js<br/>
      • Vue<br/>
      • Tailwind CSS<br/>
      • UI Engineering
    </td>
    <td valign="top" width="25%">
      <strong>Backend</strong><br/>
      • Python<br/>
      • Node.js<br/>
      • Express<br/>
      • REST APIs<br/>
      • PostgreSQL<br/>
      • Supabase / Firebase
    </td>
    <td valign="top" width="25%">
      <strong>Automation &amp; Bots</strong><br/>
      • Telegram Bots<br/>
      • Discord Bots<br/>
      • Web Automation<br/>
      • API Integrations<br/>
      • Workflow Automation
    </td>
    <td valign="top" width="25%">
      <strong>DevOps &amp; Infra</strong><br/>
      • Git<br/>
      • Linux<br/>
      • Docker<br/>
      • Cloudflare<br/>
      • Vercel / Netlify<br/>
      • Railway
    </td>
  </tr>
</table>

## Current Focus
I'm currently focused on building products that combine modern web technologies, automation, and AI to solve real business problems. I enjoy working across the entire stack, from designing user interfaces to building backend architecture and deployment pipelines.

## Contact & Links
- 🌐 [Website](https://reinlabs.netlify.app)
- 📧 [Email](mailto:reinhart96x@gmail.com)
- 💬 [Telegram Main](https://t.me/kiri0507) | [Project Enquiries](https://t.me/m/DLyhxKUhYTdl) | [Support](https://t.me/m/wFtKErccYjQ1)
- 🟢 [WhatsApp](https://wa.me/qr/63S5244F7XQ5G1)
- 🐦 [X (Twitter)](https://twitter.com/Reinhart_py_)
- 📸 [Instagram](https://www.instagram.com/Reinhart.dev/)

---
<p align="center"><i>I believe good software should be simple, maintainable, and built to last. I care more about solving problems than chasing trends.</i></p>
```

---

### Task 5: Push to Github

- [ ] **Step 1: Check git status to see modified and untracked files**
Run: `git status`

- [ ] **Step 2: Add all files and commit**
Run: `git add .`
Run: `git commit -m "feat: design custom monochromatic profile readme with automated workflows"`

- [ ] **Step 3: Push changes to main branch**
Run: `git push origin main`
