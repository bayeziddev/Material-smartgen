# [Material-smartgen](https://bayeziddev.github.io/Material-smartgen/)
<div align="center">

# SmartGen Showcase

**A zero-dependency, Python-native static site generator for premium design portfolios, UI kits, and material showcases.**

[![Live Showcase](https://img.shields.io/badge/showcase-live-4A3AE3?style=flat-square)](https://bayeziddev.github.io/Material-smartgen/)
[![PyPI ready](https://img.shields.io/badge/install-pip-C2660D?style=flat-square)](#installation)
[![License: MIT](https://img.shields.io/badge/license-MIT-0B8F6B?style=flat-square)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-4A3AE3?style=flat-square)](requirements.txt)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-C2660D?style=flat-square)](showcase/community/contributing.md)

[**Live Showcase**](https://bayeziddev.github.io/Material-smartgen/) · [Quick Start](#quick-start) · [Report an Issue](https://github.com/bayeziddev/Material-smartgen/issues)

</div>

---

## What is SmartGen Showcase?

**SmartGen Showcase** is an open-source **Python static site generator** built specifically for **designers, agencies, and template creators**. It is a `pip install`-able platform to host portfolios, UI kits, and digital assets with three deliberate differences:

- **Zero third-party front-end dependency.** No icon fonts, no UI framework, no CDN calls required by default. Every pixel in the premium theme is highly optimized.
- **One toolchain, one config file.** `smartgen-showcase init / serve / build` covers scaffolding, a live-reload dev server, and static output. Navigation, theme palette, and site metadata all live in a single `smartgen.yml`.
- **Markdown-first, no lock-in.** Every showcase page or case study is a plain `.md` file with YAML front matter. 

If you're searching for a lightweight platform to showcase your digital agency's work, web templates, or design materials that deploys straight to **GitHub Pages**, this repo is built exactly for that.

---

## Table of Contents

| # | Section | What's there |
|---|---|---|
| A | [What is SmartGen Showcase?](#what-is-smartgen-showcase) | Project summary and philosophy |
| B | [Live Demo](#live-demo) | See it running |
| C | [Installation](#installation) | `pip install` and requirements |
| D | [Quick Start](#quick-start) | Your first project in 3 commands |
| E | [Configuration (`smartgen.yml`)](#configuration-smartgenyml) | Site metadata, nav, theme palette |
| F | [CLI Reference](#cli-reference) | `init`, `serve`, `build` |
| G | [Deployment (GitHub Pages)](#deployment-github-pages) | Correct Pages setup, `.nojekyll`, `CNAME` |
| H | [License & Contact](#license) | MIT, Connect with Bayezid |

---

## Live Demo

The platform you're reading about is built with SmartGen Showcase:

**→ [bayeziddev.github.io/Material-smartgen](https://bayeziddev.github.io/Material-smartgen/)**

## Installation

```bash
pip install -r requirements.txt
pip install -e .