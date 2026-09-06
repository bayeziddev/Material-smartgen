const menuButton = document.querySelector('.menu-toggle');
const nav = document.querySelector('.nav');

menuButton?.addEventListener('click', () => {
  const open = nav.classList.toggle('is-open');
  menuButton.setAttribute('aria-expanded', String(open));
});

document.querySelectorAll('.nav a').forEach((link) => {
  link.addEventListener('click', () => {
    nav.classList.remove('is-open');
    menuButton?.setAttribute('aria-expanded', 'false');
  });
});

// Mark the theme's default reveal targets. Consumer projects can add the same
// attribute to injected markup and call the public runtime again.
document.querySelectorAll('.hero-kicker, .hero-copy, .hero-art, .hero-meta, .section-heading, .work-card, .capability-list > div, .steps > div, .facts > div, .contact-inner').forEach((node) => node.setAttribute('data-reveal', ''));

// The theme runtime owns motion/effects. Projects can call these APIs again
// after injecting custom sections or changing their config.
window.PortfolioOne?.motion?.reveal();
window.PortfolioOne?.effects?.init();
