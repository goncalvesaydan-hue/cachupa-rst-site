const test = require('node:test');
const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const { resolve } = require('node:path');
const vm = require('node:vm');
const root = resolve(__dirname, '..');
const data = vm.runInNewContext(readFileSync(resolve(root, 'data.js'), 'utf8') + '; MENU_DATA');
const script = readFileSync(resolve(root, 'script.js'), 'utf8');
const preferenceCode = script.slice(0, script.indexOf('let language = preferredLanguage()'));

const reference = data.pt.sections.flatMap(section => section.items);
const expectedSectionCounts = [['Bebidas', 51], ['Entradas', 13], ['Outros pratos', 9], ['Sobremesa', 6]];
const expectedCachupas = [
    ['CR-68', 'Cachupa tradicional', 12.5],
    ['CR-69', 'Cachupa guisada', 13],
    ['CR-70', 'Cachupa vegetariana', 12.5],
    ['CR-71', 'Cachupa de carne bovina', 15],
    ['CR-72', 'Cachupa de bacalhau', 15],
    ['CR-73', 'Cachupa de polvo', 15],
    ['CR-74', 'Cachupa de gambas', 15],
    ['CR-75', 'Cachupa de búzio', 15]
];

test('catalog products retain source prices and portions, with Cachupas in Outros pratos', () => {
    assert.equal(reference.length, 79);
    assert.equal(new Set(reference.map(item => item.id)).size, 79);
    assert.deepEqual(Array.from(data.pt.sections, section => [section.id, section.items.length]), expectedSectionCounts);
    for (const pendingCode of Array.from({ length: 7 }, (_, index) => `CR-${index + 61}`)) {
        assert.ok(!reference.some(item => item.id === pendingCode), `${pendingCode} must remain unpublished`);
    }
    const cachupaIds = new Set(expectedCachupas.map(([id]) => id));
    const cachupas = Array.from(reference).filter(item => cachupaIds.has(item.id));
    assert.deepEqual(
        cachupas.map(({ id, name, price, category }) => [id, name, price, category]),
        expectedCachupas.map(([id, name, price]) => [id, name, price, 'Outros pratos'])
    );
    for (const item of reference) {
        assert.match(item.id, /^CR-\d+$/);
        assert.ok(item.name.trim());
        assert.ok(Number.isFinite(item.price) && item.price > 0);
        assert.ok(item.portion === null || item.portion.trim());
        assert.equal(item.image, null);
        assert.equal(item.desc, '');
        assert.deepEqual(Array.from(item.ingredients), []);
        assert.deepEqual(Array.from(item.tags), []);
    }
});

for (const [language, menu] of Object.entries(data)) {
    test(`${language}: translated category labels retain the same product catalog`, () => {
        const items = menu.sections.flatMap(section => section.items);
        assert.equal(items.length, 79);
        assert.deepEqual(Array.from(menu.sections, section => section.id), Array.from(data.pt.sections, section => section.id));
        assert.deepEqual(
            items.map(({ id, name, price, portion }) => [id, name, price, portion]),
            reference.map(({ id, name, price, portion }) => [id, name, price, portion])
        );
        for (const section of menu.sections) {
            assert.equal(section.name, menu.categories[menu.sections.indexOf(section)]);
            assert.equal(section.image, null);
        }
    });
}

function preference(saved, languages, denied = false) {
    return vm.runInNewContext(preferenceCode + '; preferredLanguage()', {
        localStorage: { getItem() { if (denied) throw Error('Storage blocked'); return saved; } },
        navigator: { languages }
    });
}
test('saved language takes precedence over browser language', () => assert.equal(preference('fr', ['en-US']), 'fr'));
test('regional browser languages resolve to supported translations', () => assert.equal(preference(null, ['de-DE', 'es-MX']), 'es'));
test('invalid saved language is ignored', () => assert.equal(preference('invalid', ['en-US']), 'en'));
test('blocked storage does not prevent opening the menu', () => assert.equal(preference(null, ['fr-FR'], true), 'fr'));
test('unsupported languages fall back to Portuguese', () => assert.equal(preference(null, ['de-DE']), 'pt'));
