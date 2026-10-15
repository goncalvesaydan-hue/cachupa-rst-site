# Coordenação dos agentes — Cachupa Rst

## Âmbito

O utilizador definiu dois agentes: Codex no frontend e outro no backend. O trabalho atual é o site institucional, visual e fotográfico. Reservas por ligação WhatsApp e contacto por mailto. Menu/SaaS e backend próprio de reservas estão adiados.

Não iniciar ou delegar trabalho a agentes adicionais só pela existência deste documento. Cada agente trabalha na sessão atribuída pelo utilizador.

## Antes de editar

Ler `00-REGRAS/ESTRUTURA-DO-SITE.md`, `00-REGRAS/CONTRATO-DE-DADOS.md` e o briefing da sua função em `00-REGRAS/`.

Respeitar alterações existentes. Não apagar, substituir, formatar em massa ou fazer rollback de ficheiros do outro agente. Não alterar os produtos do menu ou a base do Notion nesta fase.

## Propriedade

- Frontend: `frontend/`, `visuals/`, `00-REGRAS/STATUS-FRONTEND.md`. Na base atual, também `assets/site.css` e `assets/site.js`.
- Backend: `backend/`, `content/`, `deployment/`, `00-REGRAS/STATUS-BACKEND.md`. Na transição, também `scripts/build.py`.
- Coordenação: `00-REGRAS/REGRAS-DOS-AGENTES.md`, `00-REGRAS/ESTRUTURA-DO-SITE.md`, `00-REGRAS/CONTRATO-DE-DADOS.md`, README e configuração partilhada. Alterar apenas numa entrega de coordenação, ou após acordar um único editor com o outro agente.
- Saída gerada: `dist/` e HTML gerado na raiz. Não editar manualmente nem gerar em paralelo na mesma pasta.
- Menu: preservar; mudanças só com novo pedido do utilizador.

A estrutura de pastas de destino ainda será implementada. As regras de transição aplicam-se imediatamente.

## Paralelismo

Preferir dois worktrees/checkouts do mesmo repositório, quando existir um repositório do projeto. Confirmar a raiz Git antes de operações; não assumir que a pasta pessoal é o repositório do site. Ramos sugeridos: `codex/site-frontend` e `codex/site-backend`.

Se ambos estiverem no mesmo checkout, não mudar o ramo nem executar comandos Git que alterem o índice ou ficheiros do outro. Trabalhar apenas nos caminhos atribuídos. Usar ficheiros de estado separados; não partilhar um log que ambos reescrevem.

Builds e servidores devem ter diretórios de saída e portas diferentes. O integrador escolhido pelo utilizador é o único a gerar a pré-visualização conjunta. Antes da escolha, manter entregas separadas e não publicar.

## Integração

Declarar versão do contrato, ficheiros alterados, comandos/testes, limitações e dependências. Contratos não mudam unilateralmente. Não migrar tecnologia, acrescentar dependências partilhadas ou criar serviços sem necessidade do âmbito.

Não inventar dados, fotografias, obras, contactos ou disponibilidade. Não guardar segredos no frontend. O clique em WhatsApp não é envio nem confirmação de reserva.
