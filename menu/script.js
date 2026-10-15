'use strict';

const UI_COPY = {
    pt: {
        locale: 'pt-PT', menu: 'Puxe uma cadeira.', intro: 'Veja o que vai para a mesa.', cuisine: 'Cozinha cabo-verdiana', welcome: 'Sente-se.',
        language: 'Idioma', categories: 'Categorias', skip: 'Saltar para os pratos',
        detailHint: 'Selecione um prato para saber mais', dishDetails: 'O prato em detalhe',
        ingredients: 'Ingredientes principais', allergens: 'Alergénios e intolerâncias',
        allergyNote: 'Tem alguma alergia ou intolerância? Fale com a nossa equipa antes de escolher.',
        allergyDetail: 'Para conhecer os alergénios e possíveis contaminações cruzadas deste prato, consulte a nossa equipa.',
        back: 'Voltar ao menu', close: 'Fechar detalhe', dishes: 'pratos', details: 'Ver detalhes de',
        tags: { V: 'Vegetariano', GF: 'Sem glúten' },
        sections: ['Para começar e partilhar.', 'Sabores do mar, à nossa maneira.', 'Cortes e preparações com carácter.', 'Um final doce, sem pressa.']
    },
    en: {
        locale: 'en-GB', menu: 'Pull up a chair.', intro: 'See what’s on the menu.', cuisine: 'Cape Verdean cuisine', welcome: 'Make yourself at home.',
        language: 'Language', categories: 'Categories', skip: 'Skip to dishes',
        detailHint: 'Select a dish to discover more', dishDetails: 'About this dish',
        ingredients: 'Main ingredients', allergens: 'Allergens and intolerances',
        allergyNote: 'Any allergies or intolerances? Please speak to our team before choosing.',
        allergyDetail: 'Please ask our team about allergens and possible cross-contact for this dish.',
        back: 'Back to menu', close: 'Close details', dishes: 'dishes', details: 'View details for',
        tags: { V: 'Vegetarian', GF: 'Gluten-free' },
        sections: ['To begin and to share.', 'Flavours of the sea, our way.', 'Carefully prepared cuts.', 'A sweet finish. Take your time.']
    },
    es: {
        locale: 'es-ES', menu: 'Tome asiento.', intro: 'Descubra lo que hay en la mesa.', cuisine: 'Cocina caboverdiana', welcome: 'Siéntase en casa.',
        language: 'Idioma', categories: 'Categorías', skip: 'Ir a los platos',
        detailHint: 'Seleccione un plato para saber más', dishDetails: 'El plato en detalle',
        ingredients: 'Ingredientes principales', allergens: 'Alérgenos e intolerancias',
        allergyNote: '¿Tiene alguna alergia o intolerancia? Hable con nuestro equipo antes de elegir.',
        allergyDetail: 'Consulte a nuestro equipo sobre los alérgenos y la posible contaminación cruzada de este plato.',
        back: 'Volver al menú', close: 'Cerrar detalles', dishes: 'platos', details: 'Ver detalles de',
        tags: { V: 'Vegetariano', GF: 'Sin gluten' },
        sections: ['Para empezar y compartir.', 'Sabores del mar, a nuestra manera.', 'Cortes preparados con cuidado.', 'Un final dulce, sin prisa.']
    },
    fr: {
        locale: 'fr-FR', menu: 'Prenez place.', intro: 'Découvrez ce qui est au menu.', cuisine: 'Cuisine cap-verdienne', welcome: 'Installez-vous.',
        language: 'Langue', categories: 'Catégories', skip: 'Aller aux plats',
        detailHint: 'Sélectionnez un plat pour en savoir plus', dishDetails: 'Le plat en détail',
        ingredients: 'Ingrédients principaux', allergens: 'Allergènes et intolérances',
        allergyNote: 'Une allergie ou une intolérance ? Parlez-en à notre équipe avant de choisir.',
        allergyDetail: 'Consultez notre équipe pour connaître les allergènes et les risques de contamination croisée de ce plat.',
        back: 'Retour au menu', close: 'Fermer les détails', dishes: 'plats', details: 'Voir les détails de',
        tags: { V: 'Végétarien', GF: 'Sans gluten' },
        sections: ['Pour commencer et partager.', 'Les saveurs de la mer, à notre façon.', 'Des viandes préparées avec soin.', 'Une fin en douceur, sans se presser.']
    }
};

function preferredLanguage() {
    try {
        const saved = localStorage.getItem('cachupa_menu_lang');
        if (Object.hasOwn(UI_COPY, saved)) return saved;
    } catch { /* The menu also works when storage is unavailable. */ }
    return (navigator.languages || [navigator.language]).map(value => value.split('-')[0])
        .find(value => Object.hasOwn(UI_COPY, value)) || 'pt';
}

let language = preferredLanguage();
let categoryId = MENU_DATA[language].sections[0].id;
let detailTrigger = null;
let scrollPosition = 0;
const dialog = document.getElementById('detail-sheet');
const byId = id => document.getElementById(id);
const escapeHTML = value => String(value).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char]));
const priceLabel = price => new Intl.NumberFormat(UI_COPY[language].locale, { style: 'currency', currency: 'EUR' }).format(Number(price));
const tagsHTML = item => item.tags.map(tag => `<span class="diet-tag">${escapeHTML(UI_COPY[language].tags[tag] || tag)}</span>`).join('');

function renderMenu() {
    const copy = UI_COPY[language];
    document.documentElement.lang = copy.locale;
    byId('language').value = language;
    byId('language').setAttribute('aria-label', copy.language);
    document.querySelectorAll('[data-copy]').forEach(element => { element.textContent = copy[element.dataset.copy]; });
    byId('close-detail').setAttribute('aria-label', copy.close);
    const navigation = byId('cat-nav');
    navigation.setAttribute('aria-label', copy.categories);
    navigation.innerHTML = MENU_DATA[language].sections.map(section => `
        <button type="button" class="category-button" data-category="${escapeHTML(section.id)}" aria-controls="category-section" aria-current="${section.id === categoryId}">${escapeHTML(section.name)}</button>
    `).join('');
    renderCategory();
}

function renderCategory(announce = false) {
    const data = MENU_DATA[language];
    const section = data.sections.find(section => section.id === categoryId) || data.sections[0];
    categoryId = section.id;
    byId('category-title').textContent = section.name;
    byId('category-description').textContent = UI_COPY[language].sections[data.sections.indexOf(section)];
    byId('category-count').textContent = `${section.items.length} ${UI_COPY[language].dishes}`;
    byId('category-image').src = section.image;
    byId('items-list').innerHTML = section.items.map(item => `
        <li><button type="button" class="item-row" data-item="${escapeHTML(item.id)}" aria-haspopup="dialog" aria-label="${escapeHTML(`${UI_COPY[language].details} ${item.name}, ${priceLabel(item.price)}`)}">
            <img class="item-thumbnail" src="${escapeHTML(item.image)}" alt="" width="92" height="92" loading="lazy" decoding="async">
            <span class="item-main">
                <span class="item-heading"><span class="item-name">${escapeHTML(item.name)}</span><span class="item-price">${escapeHTML(priceLabel(item.price))}</span></span>
                <span class="item-desc">${escapeHTML(item.ingredients.join(', '))}</span>
                <span class="item-tags">${tagsHTML(item)}</span>
            </span>
            <span class="row-arrow" aria-hidden="true">›</span>
        </button></li>
    `).join('');
    document.querySelectorAll('[data-category]').forEach(button => button.setAttribute('aria-current', String(button.dataset.category === categoryId)));
    if (announce) byId('menu-status').textContent = `${section.name}: ${section.items.length} ${UI_COPY[language].dishes}`;
}

function selectCategory(id, trigger) {
    if (id === categoryId) return;
    categoryId = id;
    renderCategory(true);
    // Retain the focused category while returning the dish list to its beginning.
    window.scrollTo({ top: 0, behavior: 'instant' });
    trigger?.scrollIntoView({ block: 'nearest', inline: 'nearest' });
}

function showDetail(id, trigger) {
    const section = MENU_DATA[language].sections.find(section => section.items.some(item => item.id === id));
    const item = section?.items.find(item => item.id === id);
    if (!item || dialog.open) return;
    detailTrigger = trigger;
    byId('detail-title').textContent = item.name;
    byId('detail-price').textContent = priceLabel(item.price);
    byId('detail-desc').textContent = item.desc;
    byId('detail-category').textContent = section.name;
    byId('detail-img').src = item.image;
    byId('detail-img').alt = item.name;
    byId('detail-tags').innerHTML = tagsHTML(item);
    byId('detail-ingredients').innerHTML = item.ingredients.map(ingredient => `<li>${escapeHTML(ingredient)}</li>`).join('');
    scrollPosition = window.scrollY;
    document.body.style.position = 'fixed';
    document.body.style.top = `-${scrollPosition}px`;
    document.body.style.width = '100%';
    dialog.showModal();
    dialog.scrollTop = 0;
    byId('close-detail').focus({ preventScroll: true });
}

function closeDetail() { if (dialog.open) dialog.close(); }

dialog.addEventListener('close', () => {
    document.body.style.position = '';
    document.body.style.top = '';
    document.body.style.width = '';
    window.scrollTo({ top: scrollPosition, behavior: 'instant' });
    detailTrigger?.focus({ preventScroll: true });
    detailTrigger = null;
});

// Only dismiss a backdrop click that both starts and ends outside the panel.
let backdropPress = false;
const outsideDialog = event => {
    const box = dialog.getBoundingClientRect();
    return event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom;
};
dialog.addEventListener('pointerdown', event => { backdropPress = event.target === dialog && outsideDialog(event); });
dialog.addEventListener('click', event => {
    if (backdropPress && event.target === dialog && outsideDialog(event)) closeDetail();
    backdropPress = false;
});
byId('close-detail').addEventListener('click', closeDetail);
byId('back-to-menu').addEventListener('click', closeDetail);
byId('language').addEventListener('change', event => {
    if (!Object.hasOwn(UI_COPY, event.target.value)) return;
    language = event.target.value;
    try { localStorage.setItem('cachupa_menu_lang', language); } catch { /* Keep the in-memory selection. */ }
    renderMenu();
    byId('menu-status').textContent = `${byId('category-title').textContent}: ${byId('category-count').textContent}`;
});
byId('cat-nav').addEventListener('click', event => {
    const button = event.target.closest('[data-category]');
    if (button) selectCategory(button.dataset.category, button);
});
byId('cat-nav').addEventListener('keydown', event => {
    const buttons = [...document.querySelectorAll('[data-category]')];
    const index = buttons.indexOf(document.activeElement);
    if (index < 0 || !['ArrowRight', 'ArrowLeft', 'Home', 'End'].includes(event.key)) return;
    event.preventDefault();
    const next = event.key === 'Home' ? 0 : event.key === 'End' ? buttons.length - 1 : (index + (event.key === 'ArrowRight' ? 1 : -1) + buttons.length) % buttons.length;
    buttons[next].focus();
    selectCategory(buttons[next].dataset.category, buttons[next]);
});
byId('items-list').addEventListener('click', event => {
    const button = event.target.closest('[data-item]');
    if (button) showDetail(button.dataset.item, button);
});
renderMenu();
