# Backend — Gemini

## Missão

Implementar a preparação técnica de dados, validação, geração e recursos para o site. Orca coordena; Codex controla a apresentação. O backend atual é de preparação/publicação, não um serviço de reservas.

## Propriedade

`backend/**`, `docs/handoffs/backend.md`; na transição, `content/**` e `scripts/build.py`. Scripts partilhados e decisões são da Orca. Não editar frontend ou menu.

## Entregas

- Validador e normalizador do contrato v1.
- Geração com destino explícito que consuma templates do frontend.
- Links WhatsApp, mailto e tel validados e codificados.
- Derivados de imagens e manifesto; originais preservados.
- Validação distinta de preview/produção, sem rascunhos na saída pública.
- Testes de entradas inválidas, referências, geração e publicação.
- Propostas de configuração de alojamento para a Orca integrar.

## Primeira tarefa a coordenar

Separar a geração da apresentação. Começar por permitir saída isolada sem modificar o visual. Acordar a interface do renderizador com o Codex e a Orca; não escolher um framework unilateralmente.

## Não incluído

Auth, Prisma, migrations, multitenancy, API de reservas, API WhatsApp, pagamentos, admin, sincronização Notion e alterações do SaaS. A pasta `prisma/` não é um requisito de implementação. Novos requisitos precisam de decisão registada.

## Handoff

Entregar comandos reproduzíveis, contrato usado, testes e limites em `docs/handoffs/backend.md`. Não afirmar que uma configuração de deploy preparada significa site publicado.
