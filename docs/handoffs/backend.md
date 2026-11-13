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
