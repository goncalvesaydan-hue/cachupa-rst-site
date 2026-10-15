# Regras comuns — Cachupa Rst

## Equipa e autoridade

- **Orca:** coordenação, distribuição de tarefas, contratos, decisões, integração e estado global.
- **Codex:** frontend, UX/UI, templates, estilos e interações.
- **Gemini:** backend, dados, validação, geração e infraestrutura de publicação.

As instruções do utilizador prevalecem. A Orca coordena dentro do âmbito autorizado; não converte propostas em requisitos nem assume aprovação de publicação. Não iniciar outros agentes só pela existência destes documentos.

## Leitura obrigatória

`README.md`, `docs/orca-briefing.md`, `docs/architecture.md`, `docs/api-contract.md`, `docs/workflow.md`, `docs/coding-standards.md`, `docs/testing.md` e regras da função. Consultar `docs/site-specification.md` para o produto. Os ficheiros em `documentation/archive/` são históricos.

## Propriedade dos ficheiros

| Responsável | Caminhos |
|---|---|
| Codex | `frontend/**`, `docs/handoffs/frontend.md`, `visuals/**` |
| Gemini | `backend/**`, `docs/handoffs/backend.md` |
| Orca | `docs/**` exceto handoffs dos agentes, README, AGENTS, GEMINI, `.env.example`, `.gitignore`, scripts partilhados e integração |

Exceções de transição: Codex mantém `assets/site.css` e `assets/site.js`; Gemini mantém `content/**` e `scripts/build.py`. Não editar páginas geradas manualmente. `menu/**` está congelado nesta fase. A Orca atribui qualquer caminho ainda sem dono antes de uma edição concorrente.

Este turno de reorganização documental é autorizado diretamente pelo utilizador e prepara os ficheiros dos três papéis. Nas próximas tarefas, Codex mantém o âmbito de frontend.

## Colaboração

Não sobrescrever, apagar ou reformatar o trabalho do outro agente. Não alterar contratos nem dependências partilhadas unilateralmente. Não fazer reset, checkout, stash, clean ou troca de ramo sobre o trabalho alheio.

Preferir worktrees/checkouts separados de um repositório do projeto, após confirmar a raiz Git. A estrutura não implica que esse repositório já exista. No mesmo checkout, respeitar estritamente propriedade e reserva de ficheiros definida pela Orca.

O frontend trabalha com fixtures do contrato, o backend com validadores do mesmo contrato. Só a Orca integra na saída conjunta; cada agente usa saída e porta próprias. Registar entregas conforme `docs/workflow.md`.

## Limites do produto

Site visual; reservas por WhatsApp e email por mailto. Sem servidor de reservas, autenticação, banco de dados ou SaaS nesta fase. A pasta `prisma/` não autoriza implementar esses elementos. Não modificar o menu ou o Notion.

Não inventar imagens, obras, contactos, ingredientes, preços ou história. Não colocar segredos no frontend. Nenhum clique externo equivale a envio ou confirmação de reserva.
