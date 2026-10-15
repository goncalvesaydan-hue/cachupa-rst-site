# Arquitetura

## Decisão atual

Preservar HTML, CSS e JavaScript no navegador e geração estática Python até existir motivo concreto para mudar. O desenho de pastas fornecido pelo utilizador não escolhe React, Next, Express, Prisma ou um fornecedor. Ver [001-stack](decisions/001-stack.md).

## Fronteiras

```text
content (fonte editorial)
        ↓
Gemini / backend: validação + normalização + imagens
        ↓ modelo v1
Codex / frontend: templates + CSS + JS + marca
        ↓ geração coordenada
saída pública → alojamento → visitante
                              ├─ WhatsApp
                              ├─ mailto
                              └─ direções
```

Frontend controla apresentação; backend controla preparação de dados e recursos. Orca controla contrato e integração. Não existe dependência de uma API remota para visualizar o conteúdo.

## Estrutura de destino

- `frontend/src/`: templates, componentes, estilos e interações; a subdivisão será definida pelo Codex e documentada.
- `frontend/public/`: marca e recursos públicos do frontend.
- `backend/src/`: validação, normalização, processamento e geração; organização interna entregue pelo Gemini.
- `backend/tests/`: testes técnicos.
- `backend/prisma/`: vazio, reservado; qualquer adoção exige decisão futura.
- `docs/`: referências canónicas; `docs/handoffs/`: entregas individuais.
- `scripts/`: comandos partilhados mantidos pela Orca.

Os módulos têm manifestos privados, não aplicações executáveis já migradas. Só acrescentar dependências justificadas e documentar runtime, versão mínima e lockfile ao introduzi-las.

## Migração sem perda

1. Inventariar a base e registar estado do trabalho dos dois agentes.
2. Gemini introduz saída explícita no gerador, preservando a pré-visualização na raiz.
3. Codex extrai a apresentação para `frontend/src/` sem editar o gerador do Gemini.
4. Gemini adapta renderização e dados ao contrato.
5. Orca gera numa pasta isolada, verifica rotas, imagens e fluxos.
6. Só remover caminhos legados depois de confirmar que não são usados e existe recuperação.

Na transição: `assets/site.css` e `assets/site.js` são do Codex; `scripts/build.py` e `content/` são do Gemini. HTML na raiz é saída gerada, não fonte editável. O menu não é migrado nesta fase.

## Operação

Produção servirá apenas saída pública, com HTTPS, cache e 404. Scripts, originais, documentação e credenciais não entram no deploy. O `.env.example` ainda não é consumido. Não depender de diretórios absolutos do computador no código final. Base URL e contactos devem vir de configuração validada.

## Evolução

Qualquer API futura exige contrato de endpoints, autenticação se aplicável, estados de erro e testes antes da integração. O atual `api-contract.md` é deliberadamente um contrato de conteúdo de build, não uma API implementada.
