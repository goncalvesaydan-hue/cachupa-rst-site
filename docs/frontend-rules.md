# Frontend — Codex

## Missão

Construir o site visual definido em `site-specification.md`. A Orca coordena; o Gemini prepara os dados e a geração. Ler `AGENTS.md`, arquitetura, contrato, workflow e testes antes de implementar.

## Propriedade

`frontend/**`, `visuals/**`, `docs/handoffs/frontend.md`; na transição, `assets/site.css` e `assets/site.js`. Não editar backend, fontes de conteúdo ou scripts partilhados sem atribuição da Orca.

## Entregas

- Templates e componentes em `frontend/src/`, recursos em `frontend/public/`.
- Página inicial dominada por fotografia; páginas Casa, Galeria, Reservas, Contactos, Privacidade e 404.
- Navegação mobile, imagens responsivas, detalhe de obras e cópia de email.
- Links WhatsApp/mailto vindos do contrato; nenhuma simulação de reserva enviada.
- Fixtures v1 para trabalhar sem bloquear no backend, identificadas e excluídas da produção.
- Testes e capturas do resultado real.

## Primeira tarefa a coordenar

Extrair apresentação do gerador antigo para templates sem editar `scripts/build.py`, que pertence ao Gemini. Acordar com a Orca o mecanismo de renderização antes de adotar sintaxe de templates ou novas dependências.

## Qualidade

Mobile desde 320 px, teclado, estados sem dados, contraste e ausência de scroll indevido. Fotografias reais quando disponíveis; quadros completos. Não transformar o menu adiado em tarefa desta fase.

## Handoff

Registar implementação e evidência em `docs/handoffs/frontend.md`; propor mudanças ao contrato à Orca. Não declarar backend pronto apenas porque a fixture funciona.
