# Guia do Backend — Claude Code (Cachupa Rst)

> **Contexto de Equipa e Divisão de Papéis:**
> - **Antigravity (Eu):** Responsável exclusivo pelo **Frontend** (`frontend/**`, templates `render.py`, CSS, JS interativo, layouts responsivos, acessibilidade e fixtures de design).
> - **Claude Code (Tu):** Responsável exclusivo pelo **Backend** (`backend/**`, gestão e validação de dados em `content/**`, pipeline de geração e publicação).
> - **Regra de fronteira:** O Claude Code **não altera** ficheiros em `frontend/**` (estilos, templates e scripts). Toda a integração entre frontend e backend é feita estritamente através do contrato canónico `docs/api-contract.md` e da interface `render_site(model)` de `frontend/src/render.py`.

---

## 1. O que é o Backend neste Projeto?

O site **Cachupa Rst** é um site institucional, fotográfico e de conversão estático para um restaurante cabo-verdiano centrado na cachupa tradicional e numa galeria cultural de pintura cabo-verdiana.

### O que o Backend É:
- Um pipeline robusto e atómico em **Python 3.11+ (standard library)**, sem dependências externas ou frameworks pesados.
- Responsável por carregar o conteúdo de `content/site.json` e `content/pages.json`.
- Responsável por **normalizar** os dados para o modelo canónico **Contrato v1** (`docs/api-contract.md`), montando links seguros de WhatsApp (`https://wa.me/...?text=...`), `mailto:` e `tel:`, e expurgando rascunhos.
- Responsável por **validar** minuciosamente os dados em dois modos distintos:
  - **`preview`:** Avisos honestos de campos em falta, saída `0` (permite testar localmente mesmo sem dados finais).
  - **`production`:** Erros impeditivos, saída `1` (bloqueia o build se faltarem contactos, morada, horários ou cidade).
- Responsável por **gerar a distribuição estática** (em `backend/dist/preview` ou `backend/dist/production`), chamando `render_site(model)` do frontend e copiando de forma segura apenas os recursos públicos e fotografias efectivamente referenciados.

### O que o Backend NÃO É (Limites Estritos):
- **NÃO é um servidor online com banco de dados.** Não há Prisma, PostgreSQL, MySQL ou SQLite. A pasta `backend/prisma/` está propositadamente vazia e congelada.
- **NÃO há autenticação, login de clientes ou multitenancy.**
- **NÃO há servidor de reservas.** As reservas são feitas por conversão direta via link do WhatsApp e email.
- **NÃO há SaaS ou sincronização com Notion nesta fase.** O módulo em `menu/` está congelado para fases posteriores.

---

## 2. Estado Atual do Backend (O que já está implementado e a funcionar)

A arquitetura do backend em `backend/src/` já está construída, com **38 testes automatizados a passar com 100% de sucesso**:

1. [`backend/src/data_loader.py`](file:///Users/aydangoncalves/Desktop/Restaurante%20Cachupa/Site/backend/src/data_loader.py):
   - Lê `content/site.json` e `content/pages.json` e unifica as fontes de dados sem as corromper.
2. [`backend/src/normalizer.py`](file:///Users/aydangoncalves/Desktop/Restaurante%20Cachupa/Site/backend/src/normalizer.py):
   - Mapeia para o schema v1 do contrato (`docs/api-contract.md`).
   - Constrói URLs codificados (`wa.me` com mensagem sanitizada, `mailto:` com assunto, `tel:`).
   - Remove rascunhos (`published: false`), limpa IDs de secções inválidos e descarta imagens não referenciadas.
   - Garante que campos privados da fonte não chegam ao modelo público.
3. [`backend/src/validator.py`](file:///Users/aydangoncalves/Desktop/Restaurante%20Cachupa/Site/backend/src/validator.py):
   - Validação detalhada com caminho do campo (JSON Pointer).
   - Valida existência física dos ficheiros de imagem em `frontend/public/`.
   - Valida sintaxe de horários, regras de `closesNextDay` e coerência display/href.
   - Emite avisos em `preview` e erros impeditivos em `production`.
4. [`backend/src/generator.py`](file:///Users/aydangoncalves/Desktop/Restaurante%20Cachupa/Site/backend/src/generator.py):
   - Gera o site estático através de `frontend.src.render.render_site(model)`.
   - Gera primeiro numa pasta temporária e substitui de forma atómica.
   - Protegido por marcador `.cachupa-build` para impedir sobreposição acidental de diretórios alheios.
   - Injeta `robots.txt` com `Disallow: /` no modo preview.
5. [`backend/src/main.py`](file:///Users/aydangoncalves/Desktop/Restaurante%20Cachupa/Site/backend/src/main.py):
   - Ponto de entrada CLI para comandos de validação, inspeção do modelo e build.

---

## 3. Qual vai ser o teu trabalho como Backend (Claude Code)

As tuas tarefas principais para levar o site a produção são:

### Tarefa 1: Alimentação e Validação dos Dados Reais de Produção
- **Ficheiros:** `content/site.json` e `content/pages.json`.
- **Objetivo:** O validador de produção (`npm --prefix backend run validate:production`) falha atualmente com 5 erros porque os seguintes dados estão como `null`:
  1. `restaurant.city` (ex: "Lisboa")
  2. `restaurant.address` (ex: morada completa)
  3. `restaurant.hours` (dias da semana 1-7, horários de abertura/fecho em formato `HH:MM`, `closesNextDay` se aplicável)
  4. `restaurant.contacts.whatsappNumber` (número real com indicativo, ex: `351912345678`)
  5. `restaurant.contacts.email` (email real de contacto)
- **Ação:** Assim que o utilizador fornecer estes dados, deves atualizar os ficheiros de conteúdo e garantir que `npm --prefix backend run validate:production` termina com código `0` e zero erros.

### Tarefa 2: Dados do Artista e Catálogo de Obras da Galeria
- **Ficheiros:** `content/site.json`.
- **Objetivo:** Atualmente, a galeria exibe o estado "A exposição está a ser preparada" porque não há artista nem obras publicadas.
- **Ação:**
  - Quando os dados forem fornecidos, preencher `artist`: `{"name": "...", "bio": "...", "website": "...", "portrait": "id_foto"}`.
  - Preencher a lista `artworks` com as obras autorizadas:
    ```json
    {
      "id": "obra-01",
      "title": "Título real da obra",
      "year": 2024,
      "technique": "Óleo sobre tela",
      "dimensions": "80 × 120 cm",
      "imageId": "quadro-01",
      "fullImageId": "quadro-01-detail",
      "order": 1,
      "published": true
    }
    ```
  - As fotografias WebP dos quadros já existem em `frontend/public/assets/photos/` (`quadro-01-1600.webp`, `quadro-01-detail.webp`, etc.). O backend deve garantir que os IDs mapeiam corretamente para os ficheiros físicos.

### Tarefa 3: Pipeline e Ferramentas de Otimização de Imagens
- **Pasta:** `backend/tools/`
- **Objetivo:** Se o restaurante adicionar novas fotografias brutas no futuro (JPG/PNG/HEIC), criar um utilitário em Python (`backend/tools/optimize_images.py` ou similar) para:
  - Gerar as variantes responsivas WebP (480w, 960w, 1200w, 1600w).
  - Obter dimensões reais (`width`, `height`).
  - Atualizar o dicionário `images` no JSON com caminhos e dimensões sem intervenção manual propensa a erros.

### Tarefa 4: Configuração de Publicação / Deployment
- **Objetivo:** Preparar a saída para o alojamento definitivo (ex: Cloudflare Pages, Netlify, Vercel ou GitHub Pages).
- **Ação:**
  - Configurar `baseUrl` (ex: `https://cachupa-rst.pt`) quando o domínio estiver definido.
  - Gerar e verificar o build final de produção via:
    `npm --prefix backend run build:production` (gerado em `backend/dist/production`).
  - Criar ficheiros de suporte de alojamento estático se necessário (ex: regras de cache para `/assets/*` e rotas de erro 404).

### Tarefa 5: Transição e Limpeza da Raiz Legada
- **Objetivo:** O projeto ainda tem ficheiros legados soltos na raiz (`index.html`, `scripts/build.py`, etc.).
- **Ação:**
  - Uma vez validado o build de produção, coordenar com o utilizador e a orquestração do projeto a substituição segura ou limpeza dos scripts legados, assegurando que os novos builds de produção alimentam a raiz ou o diretório de publicação definitivo.

---

## 4. Comandos Essenciais do Backend

Executar a partir da raiz do repositório:

| Ação | Comando |
|---|---|
| **Executar testes unitários** | `npm --prefix backend test` |
| **Verificar sintaxe (linting)** | `npm --prefix backend run lint` |
| **Validar dados (Modo Preview)** | `npm --prefix backend run validate` |
| **Validar dados (Modo Produção)** | `npm --prefix backend run validate:production` |
| **Inspecionar modelo gerado (JSON)**| `npm --prefix backend run model` |
| **Gerar build de preview** | `npm --prefix backend run build:preview` |
| **Gerar build de produção** | `npm --prefix backend run build:production` |
| **Verificação global do repositório** | `bash scripts/test-all.sh` e `bash scripts/lint-all.sh` |

---

## 5. Regras de Colaboração com o Antigravity (Frontend)

1. **Propriedade dos Ficheiros:**
   - **Claude Code:** `backend/**`, `content/**`, `docs/handoffs/backend.md`.
   - **Antigravity:** `frontend/**`, `docs/handoffs/frontend.md`, `visuals/**`.
2. **Contrato de API (`docs/api-contract.md`):**
   - É a única fonte de verdade partilhada entre nós.
   - Qualquer necessidade de novos campos ou alterações estruturais de dados deve ser discutida antes de ser aplicada.
3. **Registo de Entregas:**
   - Sempre que concluíres uma etapa de backend, atualiza `docs/handoffs/backend.md` com os comandos executados, testes realizados e eventuais pendências.

