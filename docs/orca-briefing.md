# Orca — contexto completo e guia de coordenação

## Missão

Coordenar o Codex no frontend e o Gemini no backend até existir um site coerente e verificável. Manter uma visão única de produto, contratos, tarefas, dependências e integração. Não substituir o requisito atual por uma arquitetura SaaS genérica.

## Contexto do utilizador

O restaurante chama-se Cachupa Rst / Cachupa Restaurante, é de cultura cabo-verdiana e tem a cachupa como especialidade. O utilizador quer personalidade, menos aparência de template e uma experiência mais visual. Tem fotografias de pratos, do espaço e dos quadros; a pasta ainda será partilhada. A logo e uma proposta de identidade já existem.

Reservas serão feitas por WhatsApp e haverá link de email. Não há formulário de reserva próprio no âmbito atual. A confirmação acontece na conversa com a equipa. Os contactos reais ainda faltam.

O site inclui uma galeria dedicada aos quadros de um pintor cabo-verdiano. Nome, biografia e fichas ainda não foram entregues. Exposição é o pressuposto; venda não foi autorizada.

## Menu e Notion

Existe um módulo de menu adaptado à marca na pasta `menu/`, com 22 produtos de demonstração e quatro idiomas. Não corresponde ainda à carta real. O utilizador adiou o trabalho do menu; preservar código, imagens e dados.

Existe também uma base Notion “Produtos — Menu Cachupa Rst”, dentro de “Cachupa Rst — Preparação do menu online”. Na última revisão havia 86 produtos. Foram organizados por categorias e revistos ortograficamente sem alterar preços/quantidades. Não há sincronização automática. Não importar nem editar nesta fase.

Página: https://app.notion.com/p/3f4a10a852fe811a8dbacae2b1fa687a

Base: https://app.notion.com/p/ce151b40cc354427b14ed81516d14f37

## Recursos locais

Raiz do projeto: `Desktop/Restaurante Cachupa/Site` na pasta pessoal do utilizador.

Na pasta do restaurante existem `Logo/`, `Identidade Visual/`, PDFs da proposta e ficheiros SVG. As fontes de apoio são Big Shoulders, Work Sans e Nothing You Could Do, com licenças locais. A logo original não deve ser reconstruída com essas fontes.

Paleta: azul `#006C9A`, vermelho `#DD1A2A`, amarelo `#FFED00`, branco, texto `#12323C` e apoio `#F5F1E8`.

## Estado verificável no início desta organização

| Elemento | Estado |
|---|---|
| Site na raiz | Pré-visualização estática funcional |
| Gerador | Python `scripts/build.py`, com HTML embutido |
| Estilos/interações | `assets/site.css`, `assets/site.js` |
| Conteúdo | `content/site.json`, muitos valores ainda null |
| Rotas | Início, casa, galeria, reservas, contactos, privacidade e 404 |
| Galeria | Estado vazio e código de ampliação preparado; obras reais ausentes |
| Reservas | Página de preparação; código legado ainda prevê telefone, não o novo fluxo final de WhatsApp |
| Menu | Integrado à pré-visualização, identificado como demonstração |
| `frontend/` e `backend/` | Estrutura de destino preparada, aplicação ainda não migrada |
| `package.json` | Manifestos privados vazios, sem framework instalado |
| `backend/prisma/` | Reserva de pasta; não há modelo de dados ou migrations |
| `.env.example` | Documental; o código atual não o lê |
| Produção | Não publicada; domínio/alojamento ainda por definir |

Verificações anteriores: nove testes do menu passaram; páginas verificadas a 320 px sem overflow; navegação móvel e regresso do menu funcionaram. Essas verificações são históricas e não substituem testes após a migração. A galeria com quadros reais e o WhatsApp final ainda não foram validados.

## Responsabilidade da Orca

1. Ler decisões e manter o âmbito.
2. Atribuir tarefas com ficheiros permitidos e critérios de conclusão.
3. Garantir que os dois agentes usam a mesma versão do contrato.
4. Resolver dependências e reservar edição dos ficheiros partilhados.
5. Rever entregas e integrar sem sobrescrever mudanças.
6. Executar verificação conjunta e registar pendências.
7. Manter o utilizador informado com distinção entre pronto, simulado e pendente.

A Orca é dona dos documentos canónicos e scripts de coordenação. Os agentes são donos dos seus módulos e handoffs. Ajustes fora dessa propriedade precisam de atribuição explícita, não necessariamente de uma nova pergunta ao utilizador.

## Sequência inicial recomendada

### Frente do Gemini

- Acrescentar saída configurável ao gerador, sem alterar o visual.
- Preparar validação/normalização do contrato v1.
- Coordenar a extração dos templates com o Codex.
- Preparar links WhatsApp/mailto, sem números fictícios.

### Frente do Codex

- Preparar a arquitetura dos templates e fixtures v1 dentro de `frontend/`.
- Separar os recursos de marca da dependência do menu.
- Construir layouts fotográficos e estados acessíveis.
- Aguardar imagens reais para enquadramentos finais, sem bloquear componentes.

### Primeiro marco conjunto

Gerar as páginas a partir de templates do frontend e dados normalizados pelo backend, com saída isolada. Confirmar que as rotas existentes continuam utilizáveis antes de eliminar qualquer caminho legado.

## Dados em falta

Pasta de imagens, número WhatsApp, email, morada, cidade, horários, história validada, informações do artista e obras, domínio e alojamento. Não confundir ausência de dados com falha de programação. Fazer progresso com fixtures marcadas e listar os campos que bloqueiam publicação.

## Não fazer

Não implementar auth, Prisma, multitenancy, API WhatsApp, pagamentos ou admin só porque aparecem como possibilidades no desenho de pastas. Não apresentar a demo do menu como carta real. Não atribuir datas, técnica ou dimensões às obras por inferência. Não publicar sem instrução do utilizador.

## Manutenção deste briefing

Atualizar o estado após cada integração com data, evidência e ligações para handoffs. Resolver qualquer contradição documental antes de distribuir nova tarefa. A especificação de produto é `site-specification.md`; os contratos são `api-contract.md`; decisões técnicas têm registos em `decisions/`.
