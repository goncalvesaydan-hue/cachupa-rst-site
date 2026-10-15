'use strict';
const toggle = document.querySelector('.nav-toggle');
const nav = document.querySelector('#site-nav');
if (toggle && nav) {
  const mobile = matchMedia('(max-width: 900px)');
  toggle.hidden = false;
  const close = () => { nav.hidden = mobile.matches; toggle.setAttribute('aria-expanded', 'false'); };
  close();
  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    toggle.setAttribute('aria-expanded', String(open)); nav.hidden = !open;
  });
  mobile.addEventListener('change', close);
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && mobile.matches && !nav.hidden) { close(); toggle.focus(); }
  });
}

for (const button of document.querySelectorAll('[data-copy-email]')) {
  button.hidden = false;
  button.addEventListener('click', async () => {
    const status = document.querySelector('#copy-status');
    try {
      if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(button.dataset.copyEmail);
      status.textContent = 'Email copiado.';
    } catch {
      status.textContent = 'Não foi possível copiar. Selecione o endereço de email apresentado e copie-o manualmente.';
    }
  });
}

const images = document.querySelectorAll('.media img');
for (const img of images) {
  const fail = () => img.closest('.media').classList.add('has-error');
  img.addEventListener('error', fail);
  if (img.complete && !img.naturalWidth) fail();
}

const dialog = document.querySelector('#art-dialog');
const triggers = [...document.querySelectorAll('[data-artwork]')];
if (dialog && typeof dialog.showModal === 'function') {
  const image = dialog.querySelector('img');
  const imageBox = dialog.querySelector('.dialog-image');
  const previous = dialog.querySelector('[data-art-prev]');
  const next = dialog.querySelector('[data-art-next]');
  let index = 0;
  let opener;
  let scrollPosition = 0;
  const show = value => {
    index = value;
    const trigger = triggers[index];
    const card = trigger.closest('.art-card');
    imageBox.classList.remove('has-error');
    image.alt = trigger.querySelector('img')?.alt || '';
    image.src = trigger.href;
    dialog.querySelector('#art-title').textContent = card.querySelector('h3').textContent;
    for (const field of ['meta', 'description', 'credit']) {
      dialog.querySelector(`[data-art-${field}]`).textContent = card.querySelector(`.art-${field}`).textContent;
    }
    dialog.querySelector('#art-position').textContent = `Obra ${index + 1} de ${triggers.length}`;
    previous.setAttribute('aria-disabled', String(index === 0));
    next.setAttribute('aria-disabled', String(index === triggers.length - 1));
  };
  image.addEventListener('error', () => imageBox.classList.add('has-error'));
  triggers.forEach((trigger, value) => trigger.addEventListener('click', event => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    opener = trigger; scrollPosition = window.scrollY;
    show(value);
    document.body.classList.add('dialog-open');
    dialog.showModal();
  }));
  previous.addEventListener('click', () => { if (index > 0) show(index - 1); });
  next.addEventListener('click', () => { if (index < triggers.length - 1) show(index + 1); });
  dialog.querySelector('[data-art-close]').addEventListener('click', () => dialog.close());
  dialog.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft' && index > 0) { event.preventDefault(); show(index - 1); }
    if (event.key === 'ArrowRight' && index < triggers.length - 1) { event.preventDefault(); show(index + 1); }
  });
  dialog.addEventListener('close', () => {
    document.body.classList.remove('dialog-open');
    opener?.focus({preventScroll:true});
    window.scrollTo({top:scrollPosition,behavior:'instant'});
  });
}

const helper = document.querySelector('#booking-helper');
if (helper) {
  helper.hidden = false;
  let people = '2 pessoas';
  let meal = 'Almoço';
  const waButtons = document.querySelectorAll('a[href*="wa.me"]');
  const updateWaLinks = () => {
    for (const a of waButtons) {
      try {
        const url = new URL(a.href);
        const text = `Olá! Gostaria de pedir uma reserva para ${people} (${meal}) no Cachupa Rst.`;
        url.searchParams.set('text', text);
        a.href = url.toString();
      } catch {
        // Fallback for relative or static URLs
      }
    }
  };
  helper.querySelectorAll('[data-people]').forEach(btn => {
    btn.addEventListener('click', () => {
      helper.querySelectorAll('[data-people]').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      people = btn.dataset.people === 'grupo' ? 'um grupo' : `${btn.dataset.people} pessoas`;
      updateWaLinks();
    });
  });
  helper.querySelectorAll('[data-meal]').forEach(btn => {
    btn.addEventListener('click', () => {
      helper.querySelectorAll('[data-meal]').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      meal = btn.dataset.meal;
      updateWaLinks();
    });
  });
  if (waButtons.length > 0) {
    updateWaLinks();
  }
}
