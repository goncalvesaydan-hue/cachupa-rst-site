# Registo de Controlo e Evolução do Backend — Cachupa Rst

**Ficheiro:** `documentation/archive/controlo_do_projeto/backend.md`  
**Data de Criação:** 15 de outubro de 2026, 18:30 (GMT+1)  
**Projeto:** Cachupa Rst / Cachupa Restaurante  
**Responsável:** Antigravity / Gemini (frente de Backend, dados, validação, normalização e geração estática)  
**Coordenação Global:** Orca  

---

## 1. Resumo Executivo

Este documento centraliza e regista com detalhe todo o trabalho executado no módulo de **Backend** (`backend/**`) do projeto Cachupa Rst. 

O backend é um motor de processamento e publicação estática desenvolvido em **Python 3 nativo (biblioteca padrão, sem dependências externas)**, em estrito cumprimento com o **Contrato de Integração v1** (`docs/api-contract.md`) e as diretrizes de arquitetura (`docs/backend-rules.md`). 

O backend é responsável por:
1. Ler e consolidar as fontes editoriais (`content/site.json` e `content/pages.json`).
2. Normalizar os dados para o modelo do Contrato v1 (geração de links de WhatsApp e email codificados, expurgo de rascunhos e filtros de privacidade).
3. Validar rigorosamente o modelo com distinção clara entre **Pré-visualização** (avisos para campos não preenchidos) e **Produção** (bloqueio rígido contra dados em falta).
4. Gerar o site estático completo de forma atómica e determinística, consumindo o motor `render_site` do frontend e exportando para pastas isoladas e seguras (`backend/dist/preview/` e `backend/dist/production/`).

---

## 2. Cronologia Detalhada das Intervenções

### 2.1. Estado Herdado e Auditoria ao Trabalho Prévio (15 de outubro de 2026 — 17:50)
* **Contexto:** Foi realizada uma auditoria exaustiva à implementação preliminar deixada no backend pelo agente Claude.
* **Diagnóstico das Falhas Críticas Identificadas:**
  1. *Inversão de Pipeline no `main.py`:* O código executava a validação antes da normalização. Como `content/site.json` estava no formato original mínimo, a execução abortava imediatamente com erros em cascata sem nunca alcançar a normalização.
  2. *Contradição Lógica entre Normalizador e Validador:* O normalizador inicializava páginas em falta com `title: ''`, mas o validador exigia obrigatoriamente string não vazia, fazendo com que o modelo normalizado falhasse na sua própria validação.
  3. *Incompatibilidade de Ambiente no `package.json`:* Foram configurados comandos com `python` em vez de `python3` (gerando erro `command not found` no macOS) e colocadas dependências de pip (`pytest`, `flake8`) em `devDependencies` do npm.
  4. *Suite de Testes Quebrada:* `test_backend.py` continha erros de importação (`ModuleNotFoundError`) e mocks defeituosos, falhando na execução.
  5. *Ausência de Geração Estática Integrada:* O gerador apenas imprimia JSON e não consumia o renderizador `render_site` do frontend.
  6. *Documentação Inexistente:* O ficheiro `docs/handoffs/backend.md` estava vazio.

---

### 2.2. Reestruturação e Implementação Integral (15 de outubro de 2026 — 18:00 a 18:15)
Por instrução direta do utilizador (*"faz isso tudo entao"*), o módulo de backend foi completamente reescrito e consolidado:

1. **`backend/src/data_loader.py`:**
   * Leitura segura e estritamente passiva de `content/site.json` e `content/pages.json`.
   * Criação da exceção controlada `ContentError` com indicação de linha e coluna em caso de erro de sintaxe.
   * Criação de `content/pages.json` com o conteúdo das páginas editoriais preservado fielmente da pré-visualização.

2. **`backend/src/normalizer.py`:**
   * Implementação de pipeline puro (não muta a fonte original).
   * Normalização rigorosa sem fabricação de dados falsos: campos ausentes tornam-se `null` ou `[]`.
   * Geração automática de ligações seguras e codificadas:
     * `phoneHref`: formato `tel:+351...` derivado de dígitos válidos.
     * `whatsappHref`: formato `https://wa.me/<número>?text=<mensagem_codificada>`.
     * `emailHref`: formato `mailto:<email>?subject=<assunto_codificado>`.
   * Expurgo estrito de campos privados (`whatsappNumber`, `whatsappMessage`, `emailSubject`, etc.) e de rascunhos (apenas obras com `published: true` chegam ao modelo público).

3. **`backend/src/validator.py`:**
   * Validação granular com identificação do caminho completo do nó (`field_path`) e motivo.
   * Separação estrita de ambientes:
     * **Modo Preview:** Campos de contacto ou morada em falta emitem avisos informativos, permitindo a saída 0.
     * **Modo Produção:** Campos em falta são classificados como erros fatais (saída 1), impedindo publicações incompletas.
   * Validação de segurança: rejeição de esquemas perigosos (`javascript:`, `http://` não seguro, caminhos de escape `..` em imagens).
   * Verificação de integridade referencial: referências a IDs de imagens, obras e variantes.

4. **`backend/src/generator.py` (Novo Módulo):**
   * Orquestração da geração estática chamando diretamente `render_site(model)` de `frontend/src/render.py`.
   * Geração atómica: o site é construído numa pasta temporária de *staging* e só é movido para o destino após validação completa e sem erros.
   * Proteção de destinos: recusa terminantemente escrever fora de `backend/dist/` ou apagar pastas desconhecidas que não contenham o marcador `.cachupa-build`.
   * Cópia seletiva de imagens: apenas ficheiros WebP efetivamente referenciados no modelo são copiados para a distribuição pública.
   * Injeção de `robots.txt` restritivo (`Disallow: /`) no modo de pré-visualização.

5. **`backend/src/main.py`:**
   * Interface CLI completa via `argparse`:
     * `validate [--mode preview|production] [--content DIR]`
     * `model [--mode preview|production] [--content DIR]`
     * `build --out DIR [--mode preview|production] [--content DIR]`
   * Códigos de saída consistentes: `0` (sucesso), `1` (erro de validação/build), `2` (erro fatal de I/O ou caminho).

6. **`backend/tools/check.py` (Linter Nativo):**
   * Verificação sintática via módulo `ast` de Python e `json.loads` sem qualquer dependência externa de pacotes pip.

7. **`backend/package.json`:**
   * Configuração de scripts npm executando `python3` nativo e apontando para a pasta local.
   * Eliminação total de referências espúrias a `pytest` e `flake8` no npm.

---

## 3. Inventário Técnico Atual de Ficheiros do Backend

| Ficheiro | Linhas | Função |
|---|---|---|
| `backend/src/data_loader.py` | 44 | Carregamento resiliente de dados editoriais |
| `backend/src/normalizer.py` | 321 | Normalização de dados para o Contrato v1 e sanitização |
| `backend/src/validator.py` | 441 | Validação exaustiva e contextual (Preview vs Produção) |
| `backend/src/generator.py` | 134 | Geração estática atómica e segura consumindo o frontend |
| `backend/src/main.py` | 82 | Ponto de entrada CLI e orquestrador do pipeline |
| `backend/tools/check.py` | 33 | Verificador sintático e linter nativo |
| `backend/package.json` | 16 | Manifesto com comandos operacionais padronizados |
| `backend/README.md` | 46 | Manual de instruções e documentação técnica de comandos |
| `content/pages.json` | 150 | Textos das 7 páginas editoriais do site |
| `docs/handoffs/backend.md` | 45 | Registo formal de handoff da equipa |

### Ficheiros de Teste
| Ficheiro | Linhas | Testes | Cobertura |
|---|---|---|---|
| `backend/tests/support.py` | 50 | - | Fixtures e modelos completos para testes |
| `backend/tests/test_normalizer.py` | 114 | 11 | Loader, encoding de links, expurgo de rascunhos, imutabilidade |
| `backend/tests/test_validator.py` | 148 | 15 | Regras de contrato, horários, URLs, imagens, segurança |
| `backend/tests/test_generator.py` | 138 | 12 | Builds atómicos, segurança de caminhos, CLI e determinismo |

---

## 4. Evidência de Testes e Validações

Execução dos comandos de validação global na raiz do projeto:

1. **Suite de Testes Unitários do Backend:**
   ```sh
   npm --prefix backend test
   ```
   *Resultado:* `Ran 38 tests in 0.078s — OK` (38 testes aprovados a 100%).

2. **Linter do Backend:**
   ```sh
   npm --prefix backend run lint
   ```
   *Resultado:* `10 ficheiros Python e 2 JSON de conteúdo: sintaxe válida.`

3. **Validação do Conteúdo em Pré-visualização:**
   ```sh
   npm --prefix backend run validate
   ```
   *Resultado:* `pré-visualização: 0 erro(s), 5 aviso(s)` (saída `0`).

4. **Validação do Conteúdo em Produção:**
   ```sh
   npm --prefix backend run validate:production
   ```
   *Resultado:* `produção: 5 erro(s), 1 aviso(s)` (saída `1`, bloqueia honestamente a publicação até contactos reais serem inseridos).

5. **Geração Estática Isolada:**
   ```sh
   npm --prefix backend run build:preview
   ```
   *Resultado:* `7 páginas e 15 recursos gerados em backend/dist/preview/`.  
   *Auditoria comparativa:* Páginas HTML geradas pelo backend foram comparadas byte a byte com as do frontend (`cmp -s`), confirmando **100% de paridade**.

6. **Validação Global de Toda a Codebase (Scripts de Integração):**
   ```sh
   bash scripts/test-all.sh
   bash scripts/lint-all.sh
   ```
   *Resultado:* Ambos os scripts terminaram com código `0` e aprovação em todos os módulos (Frontend + Backend).

---

## 5. Como Executar os Comandos do Backend

A partir da raiz do projeto:

* **Correr todos os testes:**  
  `npm --prefix backend test`
* **Verificar sintaxe:**  
  `npm --prefix backend run lint`
* **Validar conteúdo:**  
  `npm --prefix backend run validate`
* **Gerar modelo JSON consolidado:**  
  `npm --prefix backend run model`
* **Compilar o site estático completo:**  
  `npm --prefix backend run build:preview`

