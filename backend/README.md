# Backend — Gemini

Prepara os dados e gera o site estático. Não é um servidor: sem reservas, autenticação, base de dados ou API. `prisma/` continua reservado e vazio. Regras: [backend-rules](../docs/backend-rules.md); contrato: [api-contract](../docs/api-contract.md) v1.

## Requisitos

Python 3.11+ (biblioteca padrão). Sem dependências externas; `npm` é usado só como atalho de scripts.

## Comandos

A partir da raiz do projeto:

| Comando | Efeito |
|---|---|
| `npm --prefix backend test` | 38 testes (`unittest`) em pastas temporárias |
| `npm --prefix backend run lint` | Sintaxe de `src/`, `tests/`, `tools/` e `content/*.json` |
| `npm --prefix backend run validate` | Valida em modo pré-visualização (avisos, saída 0) |
| `npm --prefix backend run validate:production` | Valida para publicação (falha se faltar conteúdo) |
| `npm --prefix backend run model` | Imprime o modelo público v1 em JSON |
| `npm --prefix backend run build:preview` | Gera o site em `backend/dist/preview/` |
| `npm --prefix backend run build:production` | Gera em `backend/dist/production/` só se a validação de produção passar |

Forma geral: `python3 backend/src/main.py <validate|model|build> [--mode preview|production] [--content DIR] [--out DIR]`.

Códigos de saída: `0` sucesso; `1` validação ou geração falhou; `2` conteúdo ilegível ou destino recusado.

## Fluxo

```text
content/site.json + content/pages.json
  → data_loader  (leitura, sem escrita)
  → normalizer   (modelo v1: links tel/wa.me/mailto codificados, remove rascunhos e campos privados)
  → validator    (erros com caminho do campo; produção = erros, pré-visualização = avisos)
  → generator    (frontend/src/render.py → pasta de saída explícita)
```

- **Fontes:** `content/site.json` (formato legado, ainda lido por `scripts/build.py`) e `content/pages.json` (textos das páginas, por chave do contrato). Campos privados aceites na fonte: `phone`, `whatsappNumber`, `whatsappMessage`, `email`, `emailSubject`, `directionsUrl`, `published`. Nunca chegam ao modelo público.
- **Normalização:** não inventa valores. Desconhecido → `null`/`[]`; tipos errados passam para o validador reportar. Obras sem `published: true` e imagens não referenciadas são removidas.
- **Geração:** usa `render_site(model)` do frontend sem o alterar. Copia `frontend/public/` exceto `assets/photos/` e `assets/images/`, das quais só copia os ficheiros referenciados. Em pré-visualização escreve `robots.txt` com `Disallow: /`.
- **Segurança da saída:** dentro do projeto só aceita `backend/dist/…`; recusa a raiz e pastas que a contenham; nunca apaga uma pasta não vazia sem a marca `.cachupa-build`; gera numa pasta temporária e só substitui no fim.
