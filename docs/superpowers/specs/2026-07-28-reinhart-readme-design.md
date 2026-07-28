# Reinhart's Custom GitHub Profile README Design Specification

This design specification outlines the creation of a custom GitHub profile README for **Reinhart-py** using a clean, minimalist monochromatic theme. It adapts the automated workflows and layouts of the arifhaxn template while tailoring the content, styling, and repositories specifically for Reinhart.

## Design Details

### 1. Minimalist Monochromatic Theme
All visual assets (banner SVGs, projects SVG panels, stats/streak cards) will use a consistent monochromatic palette:
- **Dark Mode Background**: `#0F172A` (Slate 900)
- **Dark Mode Panels**: `#1E293B` (Slate 800)
- **Dark Mode Accents/Highlight**: `#64748B` / `#94A3B8`
- **Light Mode Background**: `#F8FAFC` (Slate 50)
- **Light Mode Panels**: `#FFFFFF` (White)
- **Light Mode Accents/Highlight**: `#94A3B8` / `#475569`

### 2. Custom Theme-Aware Hero Banner
We will generate two SVG files:
- `dark.svg`: A developer-themed terminal vector illustration displaying "REINHART" as the primary title and "Full-Stack Engineer | Developer Tools & Automation" as the subtitle, styled using dark slate tones.
- `light.svg`: The light-mode equivalent of the terminal vector illustration.

Both will be served dynamically via the `<picture>` tag in the README to adapt to the user's browser theme setting.

### 3. Featured Projects Configuration
A `projects.json` file will contain metadata for Reinhart's 6 selected repositories:
1. `Orange-carrier`
2. `flipbook`
3. `Crow`
4. `Ella`
5. `ESA`
6. `Boutique`

### 4. Automated Workflows
We will set up two GitHub Actions:
- **Projects SVG Generation (`.github/workflows/projects.yml`)**: Daily fetches of repository metadata (stars, languages) using a Python script, rendering `projects.svg` and `projects-light.svg` to a secondary branch.
- **Contribution Snake Animation (`.github/workflows/snake.yml`)**: Generates the grid of contribution snake eating commits.

---
