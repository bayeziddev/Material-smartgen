(() => {
  const root = document.querySelector('[data-portfolio-one]');
  const inlineConfig = root?.dataset.portfolioConfig;
  const parse = (value) => {
    if (!value) return {};
    try { return JSON.parse(value); } catch { return {}; }
  };

  const defaults = {
    palette: {},
    motion: { reveal: true, hero: true, parallax: false },
    effects: { noise: true, orbital: true, marquee: true },
    content: {}
  };

  const config = {
    ...defaults,
    ...parse(inlineConfig),
    palette: { ...defaults.palette, ...parse(inlineConfig).palette },
    motion: { ...defaults.motion, ...parse(inlineConfig).motion },
    effects: { ...defaults.effects, ...parse(inlineConfig).effects },
    content: { ...defaults.content, ...parse(inlineConfig).content }
  };

  Object.entries(config.palette).forEach(([key, value]) => {
    root?.style.setProperty(`--po-${key}`, value);
  });

  window.PortfolioOne = window.PortfolioOne || {};
  window.PortfolioOne.config = config;
  window.PortfolioOne.content = {
    apply(values = config.content) {
      Object.entries(values).forEach(([key, value]) => {
        document.querySelectorAll(`[data-content="${key}"]`).forEach((node) => {
          node.textContent = value;
        });
      });
    }
  };
  window.PortfolioOne.content.apply();
})();
