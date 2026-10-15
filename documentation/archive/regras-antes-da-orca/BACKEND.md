# Agente backend — conteúdo, geração e publicação

## Missão

Preparar a infraestrutura técnica do site Cachupa Rst, permitindo ao Codex construir o frontend em paralelo. O âmbito atual é um site estático com reservas por WhatsApp e email por ligação. Não existe requisito de servidor de reservas.

## Ler antes de começar

1. `00-REGRAS/REGRAS-DOS-AGENTES.md`.
2. `00-REGRAS/ESTRUTURA-DO-SITE.md`.
3. `00-REGRAS/CONTRATO-DE-DADOS.md`.
4. Este documento e o estado de entrega mais recente do frontend, se existir.

## Ficheiros sob tua responsabilidade

- `backend/`: normalização de conteúdo, validação, geração, processamento de imagens e testes técnicos.
- `content/`: fontes editoriais, configuração e inventário dos recursos.
- `deployment/`: configuração de alojamento e publicação; não publicar sem instrução do utilizador.
- `00-REGRAS/STATUS-BACKEND.md`: registo da tua entrega.

Durante a transição, `scripts/build.py` e `content/site.json` pertencem ao backend. O script atual mistura apresentação e geração: o primeiro trabalho é separá-las sem sobrepor a edição do frontend.

## Entregas

- Validador e normalizador para o modelo do contrato v1.
- Fontes de conteúdo centralizadas; não duplicar contactos em cada página.
- Geração de links WhatsApp, mailto e tel, com validação e codificação adequadas.
- Geração estática que consuma os templates do frontend e escreva numa pasta de saída explícita.
- Pipeline de imagens: derivados, dimensões, manifesto e conservação dos originais.
- Validação de publicação que rejeite dados essenciais em falta e conteúdo de demonstração exposto como real.
- Configuração técnica de HTTPS, cache, 404, redirecionamentos, robots e sitemap quando o alojamento/domínio forem conhecidos.
- Testes de dados, links, publicação e ausência de ficheiros privados na saída.

## Limites

Não criar sistema de reservas, contas, painel administrativo, base de dados, API do WhatsApp ou integração do Notion. O menu e o SaaS estão fora desta fase. Não inventar número, email, horários, história ou informação das obras.

Não editar CSS, JavaScript de interface, templates ou composição visual. Não alterar o contrato sem revisão do frontend.

## Primeira fase

1. Preservar a base atual e inventariar entradas/saídas do gerador.
2. Introduzir uma opção de saída explícita para não sobrescrever as páginas que o outro agente está a rever.
3. Separar a geração da apresentação, em coordenação com o frontend.
4. Implementar o contrato e produzir dados de pré-visualização sem contactos fictícios.
5. Entregar comandos documentados e testados; só então substituir o fluxo antigo na integração.

## Conclusão da entrega

Atualizar o teu ficheiro de estado com: ficheiros alterados, versão do contrato, comandos exatos, testes, dados em falta, limitações e instruções de integração. Distinguir configuração preparada de serviço realmente publicado.
