# Handoff — backend

## Entrega — 15 de outubro de 2026, 18:05

- **Data e tarefa:** 15/10/2026. Correção e conclusão da primeira entrega técnica do backend: validação, normalização e geração isolada do contrato v1. Substitui a versão anterior não registada, que falhava em execução (validava antes de normalizar, normalizador e validador contraditórios, testes e scripts quebrados).
- **Responsável:** Gemini (backend), por instrução direta do utilizador.
- **Versão do contrato:** v1 (`docs/api-contract.md`), sem alterações.
- **Ficheiros alterados:**
  - `backend/src/data_loader.py`, `normalizer.py`, `validator.py`, `main.py` (reescritos)
  - `backend/src/generator.py` (novo)
  - `backend/tests/support.py`, `test_normalizer.py`, `test_validator.py`, `test_generator.py` (novos; `test_backend.py` removido)
  - `backend/tools/check.py` (novo), `backend/package.json`, `backend/README.md`
  - `content/pages.json` (novo; textos copiados sem alteração de `frontend/fixtures/preview.json`)
- **Comandos executados e resultados:**
  - `npm --prefix backend test` → 38 testes, OK
  - `npm --prefix backend run lint` → sintaxe válida
  - `npm --prefix backend run validate` → 0 erros, 5 avisos (cidade, morada, horários, WhatsApp, email), saída 0
  - `npm --prefix backend run validate:production` → 5 erros com os mesmos campos, saída 1 (esperado)
  - `npm --prefix backend run build:preview` → 7 páginas e 15 recursos em `backend/dist/preview/`; HTML, CSS e JS idênticos byte a byte ao `npm --prefix frontend run build:preview`
  - `bash scripts/test-all.sh` → 0; `bash scripts/lint-all.sh` → 0
- **Funcionalidades implementadas:**
  - Normalização da fonte para o modelo v1 sem fabricar valores; derivação de `tel:`, `https://wa.me/…?text=` e `mailto:…?subject=` com codificação de caracteres especiais.
  - Remoção de rascunhos (só `published: true` é público), dos seus IDs nas secções e de imagens não referenciadas; campos privados da fonte não chegam ao modelo.
  - Validação com caminho do campo e motivo: esquema, campos desconhecidos, referências (imagens, obras, mobileImageId), IDs de secção, horários (incluindo `closesNextDay`), esquemas de URL, coerência texto/ligação, existência dos ficheiros de imagem, menu de demonstração.
  - Pré-visualização: requisitos de publicação como avisos. Produção: os mesmos como erros.
  - Geração com `render_site` do frontend para uma pasta explícita, atómica e protegida; só as fotografias referenciadas são copiadas; `robots.txt` bloqueante em pré-visualização.
- **Limitações e dados em falta:**
  - Produção bloqueada até existirem cidade, morada, horários, WhatsApp e email confirmados em `content/site.json`.
  - `site.baseUrl` nulo (sem domínio): aviso em produção, sem URL canónico.
  - Sem artista nem obras publicadas; a galeria mostra o estado vazio.
  - Derivados de imagem (redimensionamento) ainda não implementados; usam-se os WebP já existentes em `frontend/public/assets/photos/`.
  - Configuração de alojamento não preparada.
- **Dependências:** Python 3.11+ (biblioteca padrão). Depende da interface `render_site(model) -> {caminho: html}` de `frontend/src/render.py` e de `frontend/src/styles/site.css`, `frontend/src/scripts/site.js` e `frontend/public/`.
- **Instruções de integração:**
  - A Orca decide se `content/pages.json` passa a ser a fonte oficial dos textos e se a fixture do frontend deve ser derivada de `npm --prefix backend run model`.
  - O ficheiro `.cachupa-build` na raiz da saída é a marca que autoriza o gerador a substituir a pasta; o alojamento pode ignorá-lo.
  - `scripts/build.py` (legado) continua intacto e a ler `content/site.json`; não foi executado.

## Entrega — 13 de novembro de 2026 (Preparação de produção, menu e conteúdo oficial)

- **Responsável:** Gemini (backend/conteúdo/publicação) + coordenação solicitada pelo utilizador para lançamento completo.
- **Alterações implementadas:**
  - `backend/src/validator.py`: em `contacts()`, a produção exige pelo menos um canal direto válido (`phoneHref`, `whatsappHref` ou `emailHref`), emitindo avisos para `whatsappHref`/`emailHref` ausentes quando o telefone está confirmado. Em `navigation()`, `menuEnabled: true` deixa de ser bloqueado em produção por corresponder ao catálogo aprovado em `/menu/`.
  - `backend/src/generator.py` e `backend/src/main.py`: quando `navigation.menuEnabled` é verdadeiro, `_write()` copia os ficheiros públicos de `menu/` (`index.html`, `style.css`, `data.js`, `script.js` e `brand/`) para `<destino>/menu/`, mantendo `menu/README.md`, `menu/tests/`, `assets/` e `assets_2/` fora da saída e preservando a contagem das `7 páginas` institucionais no CLI.
  - `content/site.json` e `content/pages.json`: sincronizados integralmente com os dados verificados de `frontend/fixtures/preview.json` (Barreiro, horários `11:00–23:00`, telefone `963 572 411`, Google Maps, biografia/retrato de Lito Silva, `artworks: []`, `menuEnabled: true` e textos editoriais).
  - `backend/tests/test_validator.py` e `backend/tests/test_generator.py`: atualizados para validar o conteúdo real em produção, bloquear fontes incompletas sem canais/horários/morada e confirmar a cópia pública seletiva de `menu/`.
  - **Sincronização da raiz publicada para GitHub Pages:** build de produção gerado em `backend/dist/production/` e sincronizado para a raiz (`index.html`, `404.html`, `a-nossa-casa/index.html`, `contactos/index.html`, `galeria/index.html`, `privacidade/index.html`, `reservas/index.html`, `assets/site.css`, `assets/site.js`, `assets/brand/*`), juntamente com `.nojekyll`.
- **Verificação executada (após última edição):**
  - `python3 backend/src/main.py validate --mode production` → saída `0` (`produção: 0 erro(s), 3 aviso(s)`: `site.baseUrl`, `whatsappHref`, `emailHref`).
  - `python3 backend/src/main.py build --mode production --out backend/dist/production` → `7 páginas e 52 recursos gerados`.
  - `bash scripts/lint-all.sh` → saída `0`; `bash scripts/test-all.sh` → backend `39 tests OK`, frontend `17 tests OK`.

## Entrega — 13 de novembro de 2026 (Auditoria geral: `scripts/build.py`, Ruff/Mypy e workspace)

- **Alterações implementadas (`scripts/build.py`, `backend/src/**`, `.vscode/settings.json`):**
  - `scripts/build.py`: substituído o gerador legado partido (`KeyError: 'preview'`) por um wrapper que delega em `backend/src/` (`load_content`, `normalize_content`, `validate_model`, `build_site`) e sincroniza a raiz publicada (`index.html`, `404.html`, 5 subpáginas, `assets/site.css`, `assets/site.js`, `assets/brand/*`, fotos ativas e `.nojekyll`).
  - `backend/src/main.py` e `backend/src/validator.py`: removidos 4 `# noqa: E402` obsoletos (`RUF100`) e simplificado o condicional em `contacts()` (`SIM102`).
  - `.vscode/settings.json`: configurados `search.exclude`, `files.watcherExclude` (excluindo `backend/dist`, `frontend/dist`, `__pycache__`, `node_modules`) , `js/ts.tsserver.experimental.enableProjectDiagnostics: false` (nome atual da antiga chave `typescript.*`, para silenciar diagnósticos dos ficheiros de referência Figma Make em `Cachupa Rst/` sem os remover) e `python.analysis.extraPaths: ["backend/src", "frontend/src"]` para o Pylance resolver os imports de `scripts/build.py` e `frontend/tests/test_render.py` (`reportMissingImports`).

## Entrega — 13 de novembro de 2026 (Publicação na Vercel sem ficheiros internos)

- **Contexto verificado:** o repositório público tem `homepage: https://cachupa-rst-site.vercel.app` e `has_pages: false`, ou seja, o alojamento real é a Vercel (sem build, a servir a raiz do repositório). Online, `/docs/handoffs/backend.md`, `/CACHUPA-RST-AI-MASTER-BRIEF.md` e `/backend/src/main.py` respondiam `200`.
- **Alteração implementada:** novo `.vercelignore` em modo de lista de permissões: ignora tudo (`/*`) e reinclui apenas as 7 páginas geradas, `404.html`, `assets/` e, em `menu/`, só `index.html`, `style.css`, `script.js`, `data.js` e `brand/`. Também exclui `**/*.md`, `**/*.py`, `__pycache__/`, `.DS_Store` e `.env*`.
- **Verificação executada:** simulação local dos ficheiros enviados (106 ficheiros, 18 MB, contra 577 no repositório) servida em `http://127.0.0.1:3099`: páginas, `/menu/`, `litosilva.jpg` e `logo-clean.svg` → `200`; `/docs/…`, `/CACHUPA-RST-AI-MASTER-BRIEF.md`, `/backend/src/main.py`, `/content/site.json`, `/menu/README.md`, `/menu/documentation/`, `/AGENTS.md`, `/.env.example` → `404`. `audit_final.mjs` → `24/24` sem problemas, 0 erros de consola e 0 erros HTTP.

## Entrega — 13 de novembro de 2026 (WhatsApp e email oficiais nos dados e validação)

- **Alterações implementadas (`content/site.json`, `content/pages.json`, `backend/tests/test_validator.py`, `backend/tests/test_generator.py`):**
  - `content/site.json`: definidos `whatsappDisplay` (`"963 572 411"`), `whatsappHref` (`"https://wa.me/351963572411"`), `emailDisplay` (`"geral@restaurantecachupa.com"`) e `emailHref` (`"mailto:geral@restaurantecachupa.com"`).
  - `content/pages.json`: atualizados os textos de `reservations` (`description`, `intro`) e `privacy` para refletir reservas/contactos via WhatsApp (`963 572 411`), telefone e email (`geral@restaurantecachupa.com`).
  - `backend/tests/test_validator.py` e `backend/tests/test_generator.py`: atualizados os testes sobre os dados reais agora completos (zero avisos em preview; apenas `site.baseUrl` em produção).
- **Verificação executada:** `python3 scripts/build.py`, `bash scripts/lint-all.sh`, `bash scripts/test-all.sh` (`39/39` backend + `17/17` frontend).

## Entrega — 13 de novembro de 2026 (Pré-mensagem nos links de WhatsApp e Email)

- **Alteração implementada (`content/site.json`):** adicionados parâmetros `?text=...` em `whatsappHref` e `?subject=...&body=...` em `emailHref` com modelo de pedido de reserva (`Data`, `Hora`, `Número de pessoas`, `Nome` e `Telefone` no email).
- **Verificação executada:** `python3 scripts/build.py`, `bash scripts/lint-all.sh`, `bash scripts/test-all.sh` (`39/39` backend + `17/17` frontend).
