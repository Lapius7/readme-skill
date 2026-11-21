<div align="center">

<p align="center"><b>English</b> | <a href="README.ja.md">日本語</a></p>

<h1 align="center">readme-creator</h1>

<h3 align="center">A Claude skill that writes READMEs that look like the well-known repositories.</h3>

<p align="center">Centered banner, colored badges, GitHub Alerts, collapsible tables, and matching English and Japanese versions. Facts first, decoration second.</p>

<p align="center">
  <a href="https://github.com/Lapius7/readme-creator/stargazers"><img alt="Stars" src="https://img.shields.io/github/stars/Lapius7/readme-creator?style=flat-square&color=e3b341&logo=github"></a>
  <a href="https://github.com/Lapius7/readme-creator/commits/main"><img alt="Last commit" src="https://img.shields.io/github/last-commit/Lapius7/readme-creator?style=flat-square&color=3b82f6"></a>
  <a href="https://docs.claude.com/en/docs/claude-code/skills"><img alt="Claude skill" src="https://img.shields.io/badge/Claude-skill-d97757?style=flat-square&logo=anthropic&logoColor=white"></a>
  <a href="https://github.com/python-pillow/Pillow"><img alt="Pillow" src="https://img.shields.io/badge/banner-Pillow-3776ab?style=flat-square&logo=python&logoColor=white"></a>
</p>

<p align="center">
  <a href="#what-it-does">What it does</a> ·
  <a href="#install">Install</a> ·
  <a href="#usage">Usage</a> ·
  <a href="#whats-inside">What's inside</a>
</p>

</div>

---

Ask Claude for "a better README" or "a README with badges and a banner", and this skill sets the structure, the badges, the alerts, and the banner, then checks the result.

## What it does

- **Structure**: language switch, banner, tagline, badges, overview, features, quick start, tools, configuration, safety, development, roadmap, license, in that order.
- **Banner**: a rounded wide image with the project name in large white text, made from a real render or screenshot of the project. `scripts/make-banner.py` does the darkening, rounding, and lettering.
- **Badges**: shields.io `flat-square`, one color and one logo per badge. Only links that exist.
- **Alerts**: `NOTE`, `TIP`, `IMPORTANT`, `WARNING`, `CAUTION`, used where they mean something, with no emoji.
- **English and Japanese**: both versions share one structure. Japanese is proofread with the `yomiyasu` skill.
- **Facts first**: tool names, limits, and settings are checked against the code. What was not tried on a real setup is marked as unverified.

## Install

Put the folder where Claude Code looks for skills.

```sh
git clone https://github.com/Lapius7/readme-creator ~/.claude/skills/readme-creator
```

The banner script needs [uv](https://docs.astral.sh/uv/) and Pillow, which `uv run` fetches on demand.

> [!NOTE]
> The skill refers to the `yomiyasu` skill for Japanese proofreading. It still works without it, but the Japanese text is not proofread.

## Usage

Ask in plain words. Examples:

- "Write a README for this repository."
- "Make the README look better, with badges and a banner."
- "Rename done. Fix the URLs in the README."

To make only the banner:

```sh
uv run --with pillow python scripts/make-banner.py "Project Name" docs/images/hero.png docs/images/banner.png
```

The source image defaults to `docs/images/hero.png`, and the output to `docs/images/banner.png`, relative to the directory you run it in.

## What's inside

| Path | Purpose |
|---|---|
| `SKILL.md` | The instructions Claude follows: steps, structure, banner, badges, alerts, rules. |
| `templates/README.template.md` | A starting README with the centered header, badge row, alerts, and collapsible table. |
| `scripts/make-banner.py` | Makes the rounded banner with the project name. |

> [!IMPORTANT]
> Keep the English and Japanese READMEs in the same structure. Add a section to one, and add it to the other.

## License

No license has been chosen yet.
