# Portfolio One Smartgen Plugin

Portfolio One is a reusable, white-label Smartgen theme. It is not intended to be edited directly for every project. Copy the theme into a project, point Smartgen at the theme manifest, and keep project changes in the config and extension stylesheet.

## Install

Copy `protfolio-one/` into the consuming project as `themes/protfolio-one/`, then add this to `smartgen.yml`:

```yaml
theme:
  name: protfolio-one
  manifest: themes/protfolio-one/theme.yml
  config: themes/protfolio-one/runtime/theme.config.yml

portfolio_one:
  enabled: true
  extension_css: themes/protfolio-one/styles/extensions.css
```

The theme loads assets in this order: `styles.css`, `styles/tokens.css`, `styles/extensions.css`, `runtime/config.js`, `runtime/effects.js`, `runtime/motion.js`, and finally `script.js`. Core styles provide the layout; tokens provide the design system; extensions are for project-specific CSS; runtime modules provide behavior.

## Configure content and colors

Use `runtime/theme.config.yml` for project-level values. The runtime maps palette keys to CSS variables with the `--po-` prefix. For example, `palette.signal` becomes `--po-signal`. Content values are applied to elements marked with matching `data-content` attributes.

```yaml
palette:
  signal: "#E3FF5D"
  cobalt: "#5F6BFF"
content:
  brand: "Northstar Studio"
  hero.title: "Make the complex"
  hero.titleAccent: "feel obvious."
  hero.description: "A short, specific description of your studio."
```

For a small standalone page, the same values can be passed inline:

```html
<body data-portfolio-one data-portfolio-config='{"palette":{"signal":"#E3FF5D"},"motion":{"parallax":false}}'>
```

## Add sections without editing core markup

Portfolio One exposes slot markers for `hero.before`, `hero.after`, `work.before`, `work.after`, `contact.before`, and `contact.after`. A project integration can inject markup into the corresponding `.po-slot[data-slot-target="..."]` element, or render content around those slots from a Smartgen template.

## Control motion and effects

The public runtime namespace is `window.PortfolioOne`:

```js
window.PortfolioOne.effects.init({
  noise: false,
  orbital: true,
  marquee: false
});

window.PortfolioOne.motion.init({
  reveal: true,
  parallax: false
});
```

The runtime always respects `prefers-reduced-motion: reduce`. A project can disable motion globally in YAML with `motion.reveal: false` and `motion.parallax: false`, or disable individual visual effects through the effects configuration.

## Extend CSS safely

Put project overrides in `styles/extensions.css`, which is loaded after the core stylesheet and tokens. Use the `[data-portfolio-one]` scope so your rules do not leak into other Smartgen themes:

```css
[data-portfolio-one="agency"] {
  --po-signal: #f2b7ff;
  --po-cobalt: #4027e8;
}

[data-portfolio-one="agency"] .work-card {
  border-radius: 18px;
}
```

Do not edit `styles.css` for ordinary branding changes. Updating the theme becomes safe because core files can be replaced while extension code remains project-owned.

## Smartgen integration contract

The theme manifest is `theme.yml`. Its `assets`, `hooks`, and `slots` keys are the stable contract for loaders and plugins. A future Smartgen theme loader can read this manifest to copy assets, merge CSS, register runtime scripts, and expose slot rendering without knowing the theme’s internal file layout.
