const toggle = document.querySelector('.toggle');
const nav = document.querySelector('#site-nav');
if (toggle && nav) {
  const mobile = window.matchMedia('(max-width: 900px)');
  function closeNav() { nav.hidden = mobile.matches; toggle.setAttribute('aria-expanded', 'false'); }
  closeNav();
  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    nav.hidden = !open;
    toggle.setAttribute('aria-expanded', String(open));
  });
  mobile.addEventListener('change', closeNav);
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && mobile.matches && !nav.hidden) { closeNav(); toggle.focus(); }
  });
}
const dialog = document.querySelector('#art-dialog');
let artworkTrigger;
if (dialog) {
  document.querySelectorAll('[data-artwork]').forEach(button => button.addEventListener('click', () => {
    artworkTrigger = button;
    const figure = button.closest('figure');
    const thumb = button.querySelector('img');
    const image = dialog.querySelector('img');
    image.src = button.dataset.full || thumb.src;
    image.alt = thumb.alt;
    dialog.querySelector('h2').textContent = figure.querySelector('h2').textContent;
    dialog.querySelector('p').textContent = figure.querySelector('p').textContent;
    dialog.showModal();
  }));
  dialog.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => artworkTrigger?.focus());
}
