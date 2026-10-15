# ADR 003 — Multitenancy

Estado: adiada e fora do âmbito do site.

Contexto: o menu é um produto SaaS separado, mas o utilizador pediu que seja tratado depois. O site atual serve apenas o Cachupa Rst.

Decisão: não criar tenants, isolamento por restaurante, subscrições ou migrations. Manter configuração do restaurante centralizada para facilitar manutenção, sem a apresentar como multitenancy implementada.

Consequências: nenhum tenantId exigido no contrato v1. A futura integração do SaaS terá análise e contrato próprios. Não importar decisões do SaaS para este site sem confirmação de âmbito.
