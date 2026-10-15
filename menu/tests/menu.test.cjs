const test = require('node:test');
const assert = require('node:assert/strict');
const { readFileSync, existsSync } = require('node:fs');
const { resolve } = require('node:path');
const vm = require('node:vm');
const root = resolve(__dirname, '..');
const data = vm.runInNewContext(readFileSync(resolve(root, 'data.js'), 'utf8') + '; MENU_DATA');
const script = readFileSync(resolve(root, 'script.js'), 'utf8');
const preferenceCode = script.slice(0, script.indexOf('let language = preferredLanguage()'));

for (const [language, menu] of Object.entries(data)) {
    test(`${language}: all 22 dishes, categories, prices and image files are consistent`, () => {
        const reference = data.pt.sections.flatMap(section => section.items);
        const items = menu.sections.flatMap(section => section.items);
        assert.equal(items.length, 22);
        assert.equal(new Set(items.map(item => item.id)).size, 22);
        assert.deepEqual(Array.from(menu.sections, section => section.id), Array.from(data.pt.sections, section => section.id));
        for (const section of menu.sections) {
            assert.ok(existsSync(resolve(root, section.image)));
            assert.equal(section.name, menu.categories[menu.sections.indexOf(section)]);
            for (const item of section.items) {
                const original = reference.find(source => source.id === item.id);
                assert.ok(original, `${language}: unexpected dish ${item.id}`);
                assert.equal(item.price, original.price);
                assert.equal(item.image, original.image);
                assert.ok(existsSync(resolve(root, item.image)));
                assert.ok(item.name && item.desc && item.ingredients.length);
                assert.ok(item.tags.every(tag => ['V', 'GF'].includes(tag)));
            }
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
