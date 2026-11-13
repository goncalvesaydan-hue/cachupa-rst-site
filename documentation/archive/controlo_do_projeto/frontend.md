# Registo de Controlo e Evolução do Frontend — Cachupa Rst

**Ficheiro:** `documentation/archive/controlo_do_projeto/frontend.md`  
**Data de Criação:** 15 de outubro de 2026, 12:48 (GMT+1)  
**Projeto:** Cachupa Rst / Cachupa Restaurante  
**Responsável:** Antigravity / Gemini (frente de Frontend assumida por instrução direta do utilizador, sucedendo ao trabalho inicial previsto para o ChatGPT / Codex)  
**Coordenação Global:** Orca  

---

## 1. Resumo Executivo

Este documento centraliza e regista com detalhe todo o trabalho executado na frente de **Frontend** do projeto Cachupa Rst, garantindo rastreabilidade absoluta de alterações, decisões de UX/UI, ficheiros modificados, testes realizados e estado de prontidão.

O frontend é uma aplicação estática construída com **HTML semântico, CSS moderno e JavaScript nativo**, com renderização estática em **Python** via `render_site(model) -> dict[str, str]`, cumprindo estritamente o **Contrato de Integração v1** (`docs/api-contract.md`). Não depende de frameworks externos pesados (React, Vue, Tailwind, etc.) nem de servidores aplicacionais em tempo de execução.

---

## 2. Cronologia Detalhada das Intervenções

### 2.1. Estado Herdado (14 de outubro de 2026)
* O frontend contava com uma primeira implementação funcional com 7 rotas (`/`, `/a-nossa-casa/`, `/galeria/`, `/reservas/`, `/contactos/`, `/privacidade/`, `/404.html`).
* Foram triadas 429 imagens a partir do volume `/Volumes/Aydan/CACHUPA RESTAURANTE/` e integradas 10 fotografias reais exportadas em formato WebP responsivo (`480px`, `960px`, `1600px` e versões de detalhe) na pasta `frontend/public/assets/photos/`.
* A fixture `frontend/fixtures/preview.json` encontrava-se preenchida com as referências a essas 10 imagens.

---

### 2.2. Assunção da Função e Auditoria Global (15 de outubro de 2026 — 12:05)
* **Instrução do Utilizador:** Assumir o desenvolvimento de frontend que estava previsto para o ChatGPT/Codex.
* **Leitura Canónica Obrigatória:** Leitura e validação das regras em `AGENTS.md`, `README.md`, `docs/orca-briefing.md`, `docs/architecture.md`, `docs/api-contract.md`, `docs/site-specification.md`, `docs/workflow.md`, `docs/coding-standards.md` e `docs/testing.md`.
* **Auditoria de UX/UI Realizada:**
  1. *Cabeçalho:* Identificado um remendo retangular branco rígido à volta do logótipo sobre o fundo creme (`#F5F1E8`).
  2. *Hero (Página Inicial):* Conflito de ações entre dois botões de "Reservas" imediatos (um vermelho no cabeçalho e outro amarelo no hero).
  3. *Apresentação Gastronómica:* Fotografia da taça de cachupa com corte retangular rígido sobre fundo azul cobalto, sem calor visual ou relevo.
  4. *Faixa de Marca:* Faixa amarela (`#FFED00`) com saturação pura e contraste excessivo contra o azul.
  5. *Modal da Galeria:* Botões clássicos de formulário cinzento ("Fechar", "Anterior", "Seguinte") num diálogo que pedia uma experiência mais artística.
  6. *Conversão de Reservas:* O fluxo de reservas apenas encaminhava para um chat em branco no WhatsApp sem texto inicial preenchido.

---

### 2.3. Implementação dos Refinamentos de UI/UX (15 de outubro de 2026 — 12:15 a 12:20)
* **Ficheiros Modificados:**
  * `frontend/src/styles/site.css`
  * `frontend/src/render.py`
  * `frontend/src/scripts/site.js`
  * `docs/handoffs/frontend.md`
* **Melhorias Aplicadas:**
  1. **Cabeçalho Unificado e Fixo (`sticky`):** Fundo branco limpo (`#FFFFFF`) com linha divisória subtil (`rgba(18,50,60,0.08)`); o logótipo assenta de forma transparente e contínua, eliminando o retângulo artificial.
  2. **Hierarquia de Ações:** O botão principal do Hero passou a ter o rótulo caloroso **"Reservar mesa"** (em vez de duplicar o "Reservas" do menu).
  3. **Apetite Visual e Profundidade:** A taça de cachupa no Hero recebeu cantos orgânicos suavizados (`border-radius: 12px`), sombra de elevação natural (`box-shadow: 0 24px 48px -12px rgba(0,0,0,0.35)`) e micro-interação de hover.
  4. **Faixa Cultural Refinada:** Tipografia em maiúsculas com tracking equilibrado (`letter-spacing: 0.04em`), estrelas com opacidade `0.6` e linhas delimitadoras ténues.
  5. **Rodapé:** Palavra decorativa `"Cachupa."` transformada em marca d'água arquitetural (opacidade `0.22`), deixando os links úteis legíveis e em destaque.
  6. **Assistente Interativo de Reserva (WhatsApp):**
     * Na página `/reservas/`, foi adicionado um componente visual nativo:
       * Seletor de Pessoas: `2 pessoas` | `4 pessoas` | `6 pessoas` | `Grupo`
       * Seletor de Refeição: `Almoço` | `Jantar`
     * Ao clicar nas opções, o JavaScript atualiza em tempo real o link do WhatsApp para:
       `https://wa.me/...?text=Ol%C3%A1!%20Gostaria%20de%20pedir%20uma%20reserva%20para%204%20pessoas%20(Jantar)...`
     * Funciona 100% no cliente (sem servidores ou base de dados), aumentando drasticamente a conveniência do utilizador e a taxa de conversão.
  7. **Modal Artístico da Galeria:** Diálogo `<dialog>` com cantos arredondados (`border-radius: 12px`), fundo com desfoque suave (`backdrop-filter: blur(4px)`), botões refinados de fecho estilo cápsula e paginação de obras.

---

### 2.4. Remoção Temporária de Todas as Imagens (15 de outubro de 2026 — 12:25)
* **Instrução do Utilizador:** *"retira todas as imagens por agora do site"*.
* **Ações Executadas:**
  1. **Salvaguarda Preventiva:**
     * Criado backup integral do modelo com as 10 fotografias em `frontend/fixtures/preview-with-photos.json`.
     * Mantido o inventário detalhado de imagens e hashes em `frontend/fixtures/photo-selection.json`.
     * Mantidos os ficheiros WebP reais intactos em `frontend/public/assets/photos/` para reintegração rápida no futuro.
  2. **Limpeza do Modelo Ativo (`frontend/fixtures/preview.json`):**
     * `images: {}`
     * `artworks: []`
     * `heroImageId: null` em todas as rotas.
     * `imageIds: []` e `artworkIds: []` em todas as secções editoriais.
  3. **Desativação de Placeholders no Renderizador (`frontend/src/render.py`):**
     * A função `placeholder()` foi alterada para devolver string vazia `''`, impedindo a injeção de grafismos SVG provisórios de panelas e grãos no lugar das fotos.
     * O site entrou automaticamente no modo **puramente editorial/tipográfico** (`.text-only`), mantendo a grelha centrada e harmoniosa até 800px.
     * Na página da Galeria, o estado vazio *"A exposição está a ser preparada"* surge de forma elegante sem tags `<img>` ou imagens partidas.
     * **Única imagem presente no site:** O logótipo oficial da marca no cabeçalho.

---

### 2.5. Encerramento do Servidor Local (15 de outubro de 2026 — 14:16)
* **Instrução do Utilizador:** *"fecha porta local host"*.
* **Ação Executada:**
  * Identificado o processo Python em escuta na porta TCP `18952` (PID 92454).
  * Processo terminado com sucesso e verificado via `lsof -i :18952`.
  * Portas `18952` e `18951` confirmadas livres.

---

### 2.6. Reabertura do Servidor Local de Pré-visualização (15 de outubro de 2026 — 19:37)
* **Instrução do Utilizador:** *"abre a porta"*.
* **Ação Executada:**
  * Executado `npm --prefix frontend run dev` em segundo plano (`python3 tools/preview.py --serve`).
  * 7 páginas regeneradas com sucesso em `frontend/dist/`.
  * Servidor HTTP local ativo e em escuta na porta TCP `18952` (PID 82571).
  * Endereço operacional: **http://127.0.0.1:18952/**.

---

## 3. Inventário Técnico Atual de Ficheiros

| Ficheiro | Função | Estado |
|---|---|---|
| `frontend/src/render.py` | Motor de renderização estático Python (Contrato v1) | Atualizado com booking helper e modo sem imagens |
| `frontend/src/styles/site.css` | Folha de estilos completa, responsiva (320px–1440px) | Atualizada com cabeçalho sticky, botões, modal e helper |
| `frontend/src/scripts/site.js` | JavaScript nativo (menu, cópia email, dialog, booking) | Atualizado com lógica dinâmica para o WhatsApp |
| `frontend/src/templates/base.html` | Template base HTML5 | Estável, acessível, semântico |
| `frontend/fixtures/preview.json` | Modelo JSON ativo para preview local | Sem imagens (`images: {}`, `artworks: []`) |
| `frontend/fixtures/preview-with-photos.json` | Backup do modelo com fotografias reais | Preservado para restauro futuro |
| `frontend/fixtures/photo-selection.json` | Inventário de fotografias, hashes e variantes | Preservado |
| `frontend/public/assets/brand/` | Logo oficial em SVG e fontes locais OFL | Preservado e funcional |
| `frontend/public/assets/photos/` | Ficheiros WebP gerados das 10 fotografias reais | Preservados em disco |
| `frontend/tools/preview.py` | Compilador de preview e servidor HTTP local (18952) | Operacional |
| `frontend/tools/check.py` | Linter de sintaxe Python, JSON e JS | Operacional |
| `frontend/tests/test_render.py` | Suite de 8 testes unitários | 100% aprovados |
| `docs/handoffs/frontend.md` | Registo de entrega canónico da equipa | Atualizado com as entregas de 15 de outubro |

---

## 4. Evidência de Testes e Validações

Comandos executados no terminal e resultados obtidos em 15 de outubro de 2026:

1. **Testes Unitários:**
   ```sh
   npm --prefix frontend test
   ```
   *Resultado:* `Ran 8 tests in 0.002s — OK` (rotas, imutabilidade, sanitização de URLs, escaping, horários pós-meia-noite, ausência de contactos inventados e banner de preview).

2. **Verificação de Sintaxe e Linter:**
   ```sh
   npm --prefix frontend run lint
   ```
   *Resultado:* `Python, JSON e JavaScript: sintaxe válida.`

3. **Geração Estática da Pré-visualização:**
   ```sh
   npm --prefix frontend run build:preview
   ```
   *Resultado:* `7 páginas geradas em frontend/dist` (`index.html`, `a-nossa-casa`, `galeria`, `reservas`, `contactos`, `privacidade`, `404.html`).

4. **Auditoria de Tags `<img>`:**
   *Confirmado que a única tag `<img>` em todas as 7 páginas HTML é o logótipo oficial do cabeçalho.*

---

## 5. Como Executar a Pré-visualização Local

Para arrancar o servidor de desenvolvimento do frontend e inspecionar a versão atual:

```sh
npm --prefix frontend run dev
```
*Endereço:* **http://127.0.0.1:18952/**

---

## 6. Procedimento de Restauro das Fotografias (Quando Solicitado)

Se e quando o utilizador pretender reativar as fotografias reais:
1. Copiar `frontend/fixtures/preview-with-photos.json` para `frontend/fixtures/preview.json`.
2. Restaurar a definição de `placeholder()` em `frontend/src/render.py` caso pretenda grafismos de apoio.
3. Executar `npm --prefix frontend run build:preview`.

