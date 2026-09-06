(() => {
  const config = window.PortfolioOne?.config || {};
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const motion = {
    reveal(enabled = config.motion?.reveal !== false) {
      const targets = document.querySelectorAll('[data-reveal]');
      if (!enabled || reduced || !('IntersectionObserver' in window)) {
        targets.forEach((node) => node.classList.add('is-visible'));
        return;
      }
      targets.forEach((node, index) => {
        node.style.transitionDelay = `${Math.min(index * 45, 280)}ms`;
      });
      const observer = new IntersectionObserver((entries, instance) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add('is-visible');
          instance.unobserve(entry.target);
        });
      }, { threshold: .14 });
      targets.forEach((node) => observer.observe(node));
    },
    parallax(enabled = config.motion?.parallax === true) {
      if (!enabled || reduced) return;
      const art = document.querySelector('.hero-art');
      if (!art) return;
      art.addEventListener('pointermove', (event) => {
        const rect = art.getBoundingClientRect();
        const x = (event.clientX - rect.left) / rect.width - .5;
        const y = (event.clientY - rect.top) / rect.height - .5;
        art.style.setProperty('--po-mx', `${x * 10}px`);
        art.style.setProperty('--po-my', `${y * 10}px`);
      });
      art.addEventListener('pointerleave', () => {
        art.style.setProperty('--po-mx', '0px');
        art.style.setProperty('--po-my', '0px');
      });
    },
    init(overrides = {}) {
      const options = { ...config.motion, ...overrides };
      this.reveal(options.reveal);
      this.parallax(options.parallax);
    }
  };
  window.PortfolioOne = window.PortfolioOne || {};
  window.PortfolioOne.motion = motion;
  motion.init();
})();
