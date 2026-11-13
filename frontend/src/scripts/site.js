'use strict';

const menuButton = document.querySelector('.menu-button');
const nav = document.querySelector('#site-nav');
if (menuButton && nav) {
  document.body.classList.add('js-nav');
  menuButton.hidden = false;

  const setMenuOpen = open => {
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
    nav.classList.toggle('is-open', open);
    if (open) {
      nav.querySelector('a')?.focus();
    }
  };

  menuButton.addEventListener('click', () => {
    const open = menuButton.getAttribute('aria-expanded') !== 'true';
    setMenuOpen(open);
  });

  nav.addEventListener('click', event => {
    if (event.target.closest('a') && menuButton.getAttribute('aria-expanded') === 'true') {
      setMenuOpen(false);
    }
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth > 850 && menuButton.getAttribute('aria-expanded') === 'true') {
      setMenuOpen(false);
    }
  });

  document.addEventListener('keydown', event => {
    if (menuButton.getAttribute('aria-expanded') !== 'true') return;
    if (event.key === 'Escape') {
      setMenuOpen(false);
      menuButton.focus();
      return;
    }
    if (event.key !== 'Tab' || window.innerWidth > 850) return;
    const focusable = [...nav.querySelectorAll('a[href]'), menuButton]
      .filter(el => !el.hidden && el.getClientRects().length > 0);
    if (!focusable.length) return;
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });

  document.addEventListener('click', event => {
    if (
      menuButton.getAttribute('aria-expanded') === 'true' &&
      !nav.contains(event.target) &&
      !menuButton.contains(event.target)
    ) {
      setMenuOpen(false);
    }
  });
}

for (const button of document.querySelectorAll('[data-copy-email]')) {
  button.hidden = false;
  const originalLabel = button.textContent;
  button.addEventListener('click', async () => {
    const status = document.querySelector('#copy-status');
    try {
      if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(button.dataset.copyEmail);
      if (status) status.textContent = 'Email copiado.';
      button.textContent = 'Email copiado';
      setTimeout(() => { button.textContent = originalLabel; }, 2200);
    } catch {
      if (status) {
        status.textContent = 'Não foi possível copiar. Selecione o endereço de email apresentado e copie-o manualmente.';
      }
    }
  });
}

for (const img of document.querySelectorAll('.media img')) {
  const fail = () => img.closest('.media')?.classList.add('has-error');
  img.addEventListener('error', fail);
  if (img.complete && !img.naturalWidth) fail();
}

const dialog = document.querySelector('#art-dialog');
const triggers = [...document.querySelectorAll('[data-artwork]')];
if (dialog && typeof dialog.showModal === 'function' && triggers.length > 0) {
  const modalImg = dialog.querySelector('.modal-frame img');
  const modalFrame = dialog.querySelector('.modal-frame');
  const prevBtn = dialog.querySelector('[data-art-prev]');
  const nextBtn = dialog.querySelector('[data-art-next]');
  const closeBtn = dialog.querySelector('[data-art-close]');
  const posEl = dialog.querySelector('#art-position');
  const titleEl = dialog.querySelector('#art-title');
  const techEl = dialog.querySelector('[data-art-technique]');
  const descEl = dialog.querySelector('[data-art-description]');
  const metaEl = dialog.querySelector('[data-art-meta]');

  let index = 0;
  let opener = null;

  const show = nextIndex => {
    index = (nextIndex + triggers.length) % triggers.length;
    const trigger = triggers[index];
    const card = trigger.closest('.art-card, .artwork');
    modalFrame.classList.remove('has-error');
    modalImg.alt = trigger.querySelector('img')?.alt || '';
    modalImg.src = trigger.href;

    const title = card?.querySelector('.art-title-source')?.textContent
      || card?.querySelector('.art-meta strong')?.textContent
      || '';
    const technique = card?.querySelector('.art-technique')?.textContent || '';
    const description = card?.querySelector('.art-description')?.textContent || '';
    const meta = card?.querySelector('.art-meta-line')?.textContent
      || card?.querySelector('.art-credit')?.textContent
      || '';

    if (titleEl) titleEl.textContent = title;
    if (techEl) {
      techEl.textContent = technique;
      techEl.hidden = !technique;
    }
    if (descEl) {
      descEl.textContent = description;
      descEl.hidden = !description;
    }
    if (metaEl) {
      metaEl.textContent = meta;
      metaEl.hidden = !meta;
    }
    if (posEl) {
      const current = String(index + 1).padStart(2, '0');
      const total = String(triggers.length).padStart(2, '0');
      posEl.textContent = `${current} / ${total}`;
    }
    const single = triggers.length <= 1;
    if (prevBtn) prevBtn.disabled = single;
    if (nextBtn) nextBtn.disabled = single;
  };

  modalImg.addEventListener('error', () => modalFrame.classList.add('has-error'));

  triggers.forEach((trigger, idx) => {
    trigger.addEventListener('click', event => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      opener = trigger;
      show(idx);
      dialog.showModal();
    });
  });

  prevBtn?.addEventListener('click', () => {
    if (triggers.length > 1) show(index - 1);
  });
  nextBtn?.addEventListener('click', () => {
    if (triggers.length > 1) show(index + 1);
  });
  closeBtn?.addEventListener('click', () => dialog.close());

  if (!('closedBy' in HTMLDialogElement.prototype)) {
    dialog.addEventListener('click', event => {
      if (event.target !== dialog) return;
      const rect = dialog.getBoundingClientRect();
      const isDialogContent = (
        rect.top <= event.clientY &&
        event.clientY <= rect.top + rect.height &&
        rect.left <= event.clientX &&
        event.clientX <= rect.left + rect.width
      );
      if (isDialogContent) return;
      dialog.close();
    });
  }

  dialog.addEventListener('keydown', event => {
    if (triggers.length <= 1) return;
    if (event.key === 'ArrowLeft') {
      event.preventDefault();
      show(index - 1);
    } else if (event.key === 'ArrowRight') {
      event.preventDefault();
      show(index + 1);
    }
  });

  dialog.addEventListener('close', () => {
    opener?.focus({ preventScroll: true });
  });
}
