# ADR 001 — Stack

Estado: base atual preservada; migração modular pendente.

Contexto: existe site estático em HTML/CSS/JS com gerador Python. O utilizador definiu estrutura frontend/backend e três papéis, mas não escolheu um novo framework.

Decisão: manter essa base até a Orca aprovar uma alteração justificada. `package.json` é um manifesto de coordenação, não prova de aplicação Node. O backend prepara conteúdos e gera saída estática.

Consequências: separar templates do Python embutido; escolher mecanismo de renderização em coordenação. Não instalar React, Next, Express ou Prisma por inferência. Qualquer mudança deve explicar necessidade, custo de migração, impacto no contrato, testes e recuperação.
