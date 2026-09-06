(() => {
  const root = document.querySelector('[data-portfolio-one]');
  const config = window.PortfolioOne?.config || {};
  const effects = {
    noise(enabled = config.effects?.noise !== false) {
      root?.classList.toggle('po-noise-off', !enabled);
    },
    orbital(enabled = config.effects?.orbital !== false) {
      document.querySelectorAll('.orb').forEach((node) => {
        node.classList.toggle('po-effect-off', !enabled);
      });
    },
    marquee(enabled = config.effects?.marquee !== false) {
      document.querySelectorAll('.marquee-track').forEach((node) => {
        node.classList.toggle('po-effect-off', !enabled);
      });
    },
    init(overrides = {}) {
      const options = { ...config.effects, ...overrides };
      this.noise(options.noise);
      this.orbital(options.orbital);
      this.marquee(options.marquee);
    }
  };
  window.PortfolioOne = window.PortfolioOne || {};
  window.PortfolioOne.effects = effects;
  effects.init();
})();
