# ADR 002 — Autenticação

Estado: não necessária no âmbito atual.

Contexto: site público; reservas externas por WhatsApp; email via mailto. Não há painel ou contas requeridos.

Decisão: não implementar login, sessões, JWT ou armazenamento de credenciais. Acesso à hospedagem e eventual pré-visualização privada são configuração operacional, não autenticação de clientes.

Consequências: nenhuma chave de WhatsApp ou email necessária para links. Se surgir admin, a Orca abre nova decisão com papéis, autorização, modelo de ameaças e requisitos antes de implementar. `noindex` não protege informação privada.
