# Cachupa Rst — Estrutura completa do site

Documento de referência para construir o MVP do restaurante e integrar o menu online como um módulo do SaaS.

**Data:** 9 de outubro de 2026  
**Atualização:** 13 de outubro de 2026 — galeria de um pintor cabo-verdiano  
**Estado:** estrutura proposta para implementação. A base estática das páginas públicas e a integração do menu estão implementadas nesta pasta. Os conteúdos finais, o backend e a publicação de produção continuam pendentes.

## 1. Objetivo

Apresentar o Cachupa Rst, a sua ligação à cultura cabo-verdiana e a cachupa como especialidade. Permitir conhecer os pratos, consultar preços, pedir uma reserva e encontrar o restaurante.

O site deve funcionar bem no telemóvel, tanto para quem chega através de pesquisa ou redes sociais como para quem abre o menu por um QR code à mesa.

### Decisões já estabelecidas

- Nome e logo: Cachupa Rst / Cachupa Restaurante, usando a logo fornecida.
- Identidade cabo-verdiana, com a cachupa em destaque.
- Seis páginas principais: Início, Menu, A nossa casa, Galeria, Reservas e Contactos.
- A Galeria é dedicada exclusivamente aos quadros de um pintor cabo-verdiano. Nome do artista e obras a fornecer.
- O menu abre dentro do mesmo site, numa página própria.
- O menu é um produto reutilizável do SaaS, com configuração própria para cada restaurante.
- A cópia adaptada ao Cachupa está em `menu/`. O projeto original permanece independente.
- Produtos, nomes, preços e imagens atuais são os da demonstração original, mantidos por pedido do utilizador.

### Propostas técnicas deste documento

Rotas, endpoints, tabelas e organização futura de código descritos abaixo são propostas. Não representam funcionalidades já implementadas nem uma escolha definitiva de framework ou fornecedor.

## 2. Mapa de páginas

```text
Site Cachupa Rst
│
├── /                         Início
├── /menu/                    Menu online
│   ├── Categorias
│   ├── Lista de produtos
│   └── Detalhe do produto
├── /a-nossa-casa/             História, equipa e espaço
├── /galeria/                 Quadros do pintor cabo-verdiano
│   └── Detalhe de cada obra
├── /reservas/                Pedido de reserva
├── /contactos/               Localização, horários e contactos
│
├── /privacidade/             Informação sobre tratamento de dados
└── /404                      Página não encontrada

Área de gestão do SaaS        Separada da navegação pública
├── Autenticação
├── Restaurante e identidade
├── Categorias e produtos
├── Fotografias e traduções
└── Revisão e publicação

Gestão das reservas           Área protegida, se incluída no MVP
```

O endereço da área de gestão depende da arquitetura do SaaS. Pode existir num domínio próprio; não precisa de aparecer no menu de navegação do restaurante.

## 3. Estrutura partilhada

### Cabeçalho

- Logo com ligação à página inicial.
- Ligações: Início, Menu, A nossa casa, Galeria e Contactos.
- Botão principal: **Reservar mesa**.
- No telemóvel, navegação compacta acessível por botão, com indicação de aberto/fechado e fecho por Escape.
- Na página do menu, usar uma versão compacta: logo, regresso ao site e idioma; categorias abaixo. Evitar dois cabeçalhos fixos sobrepostos.

### Rodapé

- Nome do restaurante e descrição curta.
- Morada, telefone e horários confirmados.
- Redes sociais reais.
- Ligações para Menu, Galeria, Reservas, Contactos e Privacidade.
- Restante informação legal aplicável à operação, a confirmar antes da publicação.

### Regras gerais

- Uma ação principal clara por área.
- Texto legível, contraste adequado, foco visível e navegação por teclado.
- Fotografias responsivas, dimensões reservadas e carregamento diferido abaixo da primeira área visível.
- Respeitar a preferência por movimento reduzido.
- Formulários com rótulos, mensagens de erro junto dos campos e confirmação inequívoca.
- Manter o idioma escolhido quando o utilizador navega entre áreas que tenham tradução.

## 4. Página inicial — `/`

### Ordem dos blocos

| Bloco | Conteúdo | Ação |
|---|---|---|
| Apresentação | Logo, frase curta, cozinha cabo-verdiana, cidade e fotografia real da cachupa | Ver menu / Reservar mesa |
| Especialidade | Cachupa da casa: descrição, porção e particularidades confirmadas | Ver o prato no menu |
| Pratos em destaque | Até três produtos aprovados, com fotografia e preço | Abrir o respetivo detalhe |
| A nossa casa | Breve história e fotografia da equipa ou do espaço | Conhecer a casa |
| Ambiente | Pequena seleção de fotografias reais | Ver o espaço |
| Arte cabo-verdiana | Até três quadros, com título e nome do pintor | Visitar a galeria |
| Avaliações, quando existirem | Testemunhos reais com origem identificada | Consultar a origem, se aplicável |
| Planear a visita | Horários, morada e contactos | Reservar / Como chegar |

### Comportamento

- **Ver menu** abre `/menu/` no mesmo separador.
- **Reservar mesa** abre `/reservas/`.
- Os destaques devem usar a mesma fonte de produtos do menu para evitar preços diferentes entre páginas.
- Não publicar afirmações, avaliações, receitas, horários ou contactos inventados.
- A frase proposta “Hoje há cachupa” só deve aparecer quando a disponibilidade do prato a justificar.

## 5. Menu online — `/menu/`

### Implementação existente

```text
menu/
├── index.html                Estrutura da página e do detalhe
├── style.css                 Apresentação da versão Cachupa
├── script.js                 Idiomas, categorias e interações
├── data.js                   Produtos e traduções de demonstração
├── assets_2/                 Fotografias atualmente utilizadas
├── brand/
│   ├── logo.svg
│   └── fonts/                Fontes locais e licenças
├── tests/                    Testes existentes
├── documentation/
└── visuals/                  Diagramas e capturas
```

A cópia também conserva pastas auxiliares do projeto de origem. A implantação deverá publicar apenas os ficheiros necessários à aplicação.

### Experiência do visitante

```text
Homepage ou QR code
        ↓
    /menu/
        ↓
Escolher categoria
        ↓
Comparar pratos e preços
        ↓
Abrir detalhe
        ↓
Fechar e regressar à posição anterior
```

### Lista de produtos

- Nome, fotografia, preço e resumo dos ingredientes.
- Informação alimentar apenas quando validada pelo restaurante.
- Variante ou porção quando fizer diferença na escolha.
- Produtos indisponíveis identificados ou ocultados segundo uma regra definida pela equipa.
- Categorias reais e ordenáveis. As categorias atuais continuam a ser as da demonstração.

### Detalhe do produto

- Fotografia maior.
- Nome, descrição e preço.
- Ingredientes, acompanhamentos e porção.
- Variantes e extras, se existirem.
- Informação confirmada sobre alergénios.
- Botão para fechar e voltar ao menu.
- Em desktop: janela modal. Em mobile: painel inferior.
- Manter o foco dentro do detalhe e devolvê-lo ao produto ao fechar.

### Idiomas

O menu atual suporta português, inglês, espanhol e francês. A preferência é guardada localmente com a chave `cachupa_menu_lang`.

No backend futuro, guardar preço, imagens e disponibilidade uma única vez por produto. Guardar separadamente os textos traduzidos. Uma tradução em falta deve ter uma alternativa definida, sem bloquear o menu.

### Integração com o site

- Manter `/menu/` no domínio do restaurante, com a mesma identidade visual.
- Preferir um módulo ou página integrada. Um iframe não é necessário para esta primeira versão.
- Garantir que estilos e identificadores do menu não interferem com o restante site.
- Adaptar o scroll de troca de categoria ao cabeçalho final.
- Acrescentar uma ligação clara de regresso ao site.
- Evolução recomendada: URL partilhável por produto, por exemplo `/menu/?produto=ID`, com comportamento consistente do botão Voltar do navegador. Ainda não implementado.
- Não duplicar a lógica do SaaS para cada restaurante: separar apresentação, configuração e dados.

### Fora do primeiro MVP

Carrinho, pagamento, pedidos à mesa, cozinha, entregas próprias e gestão de stock não fazem parte do âmbito inicial. O menu serve para consulta. Se houver takeaway, pode existir uma ligação para o canal real usado pelo restaurante.

## 6. A nossa casa — `/a-nossa-casa/`

### Conteúdo

1. Fotografia da equipa ou do espaço.
2. História do restaurante, escrita a partir das palavras dos responsáveis.
3. Ligação à cultura cabo-verdiana.
4. Lugar da cachupa na cozinha da casa.
5. Apresentação das pessoas e do ambiente.
6. Convite para consultar o menu ou reservar.

Evitar transformar esta página numa história genérica sobre Cabo Verde. O centro são as pessoas, a cozinha e a experiência deste restaurante.

## 6A. Galeria — `/galeria/`

**Decisão confirmada:** o site terá uma área dedicada apenas aos quadros de um pintor cabo-verdiano. A estrutura abaixo é uma proposta para essa área. Não misturar as obras com fotografias de pratos, da equipa ou do espaço.

### Conteúdo e ordem

1. **Apresentação:** nome do pintor, título da galeria e um texto curto sobre a sua ligação a Cabo Verde e ao restaurante, com informação fornecida pelo artista.
2. **Quadros:** grelha com imagem completa, título e ano, quando conhecidos. Técnica e dimensões podem aparecer no detalhe.
3. **Sobre o artista:** biografia breve e ligação para o seu site ou perfil oficial, se fornecidos.

### Direção visual

- Fundo claro e discreto, com bastante espaço entre as obras.
- Manter as cores da marca na navegação e nos pequenos detalhes; as pinturas são o elemento principal.
- Preservar a proporção original de cada quadro, sem cortes, filtros de cor ou texto sobreposto à pintura.
- Uma coluna em ecrãs pequenos e duas ou três em ecrãs maiores, adaptando à proporção das obras.
- Evitar carrossel automático. Para uma coleção pequena, uma grelha simples é suficiente.

### Interação e acessibilidade

```text
Início ou navegação → Galeria → Escolher quadro
                                   ↓
                         Imagem ampliada e ficha
                                   ↓
                         Fechar e voltar à grelha
```

- Cada quadro abre um diálogo acessível com imagem ampliada, título, autoria, ano, técnica e dimensões disponíveis.
- Fechar por botão visível ou Escape; manter o foco no diálogo e devolvê-lo à obra ao fechar.
- Incluir texto alternativo descritivo de cada pintura; não depender apenas da cor ou de efeitos ao passar o rato.
- Usar imagens responsivas e carregar a versão de maior resolução apenas quando necessária.
- No MVP, a galeria serve para exposição. Preços, compra, encomendas ou pedidos sobre obras só entram se esse objetivo for confirmado.

### Conteúdo necessário

- Nome artístico e biografia aprovada pelo pintor.
- Fotografias das obras, títulos e informação técnica disponível.
- Ordem de apresentação e obras em destaque na página inicial.
- Créditos das imagens e autorização para publicação das obras e fotografias.
- Não inventar títulos, datas, interpretações, prémios ou histórias do artista; omitir campos ainda desconhecidos.

### Publicação e gestão

- Manter os quadros numa coleção própria, separada dos produtos do menu e da base de produtos no Notion.
- No MVP, pode ser um ficheiro de dados com publicação controlada; um painel exclusivo não é necessário.
- Se for integrada no backend, só as obras publicadas são públicas. Aplicar as mesmas permissões por restaurante às imagens e aos registos.

## 7. Reservas — `/reservas/`

### Formulário

| Campo | Regra proposta |
|---|---|
| Nome | Obrigatório |
| Contacto | Obrigatório; telefone ou email válido |
| Data | Obrigatória; sem datas passadas |
| Hora | Obrigatória; dentro dos períodos definidos pela equipa |
| Pessoas | Obrigatório; limite de grupo configurável |
| Observações | Opcional; comprimento limitado |

Mostrar informação de privacidade junto do envio. Não associar o pedido a comunicações de marketing.

### Fluxo

```text
Preencher → Validar → Enviar → Registar no servidor
                                      ↓
                             Mostrar pedido recebido
                                      ↓
                               Notificar a equipa
                                      ↓
                      Confirmar ou propor alternativa
```

**Pedido recebido não significa reserva confirmada.** A mensagem deve explicar que a equipa verificará a disponibilidade.

### Backend mínimo

- Validar novamente todos os campos no servidor.
- Usar o fuso horário e os horários reais do restaurante.
- Guardar o pedido antes de mostrar sucesso.
- Evitar duplicação em reenvios com uma chave de idempotência.
- Limitar pedidos abusivos e usar proteção antisspam proporcional.
- Enviar notificações por um canal configurado; tratar falhas e permitir nova tentativa.
- Restringir a consulta de dados de clientes à equipa autorizada.

### Estados

`Pendente → Confirmada / Alternativa proposta / Recusada / Cancelada`

Se a primeira entrega usar apenas telefone ou WhatsApp, apresentar esses botões explicitamente e não mostrar um formulário sem processamento real.

## 8. Contactos — `/contactos/`

- Morada completa.
- Horários reais e dias de encerramento.
- Telefone clicável.
- Email e WhatsApp, se utilizados pela equipa.
- Ligação para direções; mapa incorporado apenas se trouxer utilidade.
- Informações confirmadas sobre estacionamento, transportes e acessibilidade.
- Contacto para grupos ou eventos apenas se esses serviços existirem.

## 9. Identidade visual

### Cores

| Papel | Cor |
|---|---|
| Azul principal | `#006C9A` |
| Vermelho de destaque | `#DD1A2A` |
| Amarelo | `#FFED00` |
| Branco | `#FFFFFF` |
| Texto escuro | `#12323C` |
| Papel de apoio | `#F5F1E8` |

### Tipografia

- **Big Shoulders Bold:** títulos e chamadas.
- **Work Sans Regular/Bold:** leitura, preços, formulários e navegação.
- **Nothing You Could Do:** apontamentos curtos, sem informação essencial.

Usar os ficheiros locais e manter as licenças incluídas. A logo é o SVG fornecido, não uma composição com estas fontes.

### Direção de interface

- Dar destaque à comida e à marca, com espaço para respirar.
- Reservar o vermelho para ações e pequenos apontamentos.
- Usar amarelo com contraste suficiente, sobretudo sobre azul.
- Evitar repetir cartões, símbolos ou animações sem função.
- As fotografias reais substituem progressivamente o conteúdo de demonstração.

## 10. Arquitetura técnica proposta

```text
Visitante
   ↓
Site público do restaurante
   ├── Páginas de apresentação
   ├── Galeria de quadros ───→ Coleção de obras publicadas
   ├── Módulo de menu ───────→ API de conteúdo publicado
   └── Formulário de reserva → API de reservas
                                     ↓
                         Dados e notificações protegidos

Equipa autorizada
   ↓
Painel de gestão do SaaS
   ↓
Autenticação + permissões por restaurante
   ↓
Produtos / categorias / traduções / imagens / publicação
```

### Responsabilidades

| Camada | Responsabilidade |
|---|---|
| Site público | Apresentação, navegação e formulários |
| Módulo de menu | Mostrar categorias, produtos e detalhe |
| Galeria | Mostrar obras, ficha do artista e detalhe ampliado |
| API pública | Entregar apenas conteúdo publicado |
| API administrativa | Validar alterações e aplicar permissões |
| Base de dados | Dados estruturados e associação ao restaurante |
| Armazenamento de imagens | Guardar ficheiros, gerar tamanhos e entregar imagens |
| Notificações | Avisar a equipa sobre reservas e acompanhar falhas |

Não é necessário reescrever o menu num framework para validar o MVP. A escolha de stack deve respeitar a arquitetura do SaaS, caso exista noutro projeto. Esta pasta não contém essa arquitetura.

### Evolução em duas etapas

1. **MVP de um restaurante:** páginas públicas, menu adaptado, dados reais e pedidos de reserva operacionais. O conteúdo pode ser publicado como ficheiros estáticos gerados a partir de uma fonte controlada.
2. **SaaS com gestão autónoma:** painel autenticado, dados por restaurante, fluxo de publicação e manutenção central do módulo.

Não depender de uma chamada ao Notion a cada abertura do menu. Publicar uma versão validada e estável dos dados, servida pelo site ou API.

## 11. Modelo de dados proposto

| Entidade | Campos principais |
|---|---|
| Restaurante | ID, slug, nome, domínio, moeda, fuso horário, contactos, morada, horários |
| Tema | Restaurante, logo, cores, fontes e opções de apresentação |
| Categoria | ID, restaurante, ordem, ativa/publicada |
| Tradução de categoria | Categoria, idioma, nome e descrição |
| Produto | ID, restaurante, categoria, preço base, moeda, ordem, destaque, disponibilidade, estado editorial |
| Tradução de produto | Produto, idioma, nome, descrição, ingredientes e acompanhamentos |
| Variante | ID, produto, nome/porção, preço e disponibilidade |
| Extra | ID, restaurante, nome e preço; associação aos produtos permitidos |
| Informação alimentar | Produto, informação confirmada, responsável e data de validação |
| Imagem | ID, restaurante, localização do ficheiro, dimensões e texto alternativo |
| Imagem de produto | Produto, imagem, ordem e indicação de principal |
| Publicação | Restaurante, versão, estado, data e responsável pela publicação |
| Artista | ID, restaurante, nome artístico, biografia e ligações oficiais |
| Obra | ID, restaurante, artista, título, ano, técnica, dimensões, imagem, texto alternativo, créditos, ordem, destaque e estado editorial |
| Reserva | ID, restaurante, nome, contacto, data/hora, pessoas, observações e estado |
| Acesso | Utilizador, restaurante e papel/permissões |

### Regras de dados

- Guardar dinheiro em unidades mínimas inteiras e associar a moeda; não depender de cálculos com números decimais de precisão limitada.
- Distinguir disponibilidade comercial de estado editorial. Um produto aprovado pode estar temporariamente indisponível.
- Campo alimentar vazio significa informação por recolher, não ausência de alergénios.
- Validar que categorias, produtos, variantes e ficheiros associados pertencem ao mesmo restaurante.
- Os dados públicos não devem incluir notas internas, contactos de clientes ou rascunhos.

## 12. Endpoints indicativos

Os nomes abaixo orientam a implementação; não existem ainda neste projeto.

| Método e rota | Finalidade |
|---|---|
| `GET /api/public/restaurants/:slug` | Informação pública e tema |
| `GET /api/public/restaurants/:slug/menu?lang=pt` | Menu publicado e respetiva versão |
| `GET /api/public/restaurants/:slug/gallery` | Artista e obras publicadas; opcional se a galeria for servida como conteúdo estático |
| `POST /api/public/restaurants/:slug/reservations` | Criar pedido de reserva |
| `GET /api/admin/restaurants/:id/products` | Listar produtos para gestão |
| `POST /api/admin/restaurants/:id/products` | Criar produto |
| `PATCH /api/admin/restaurants/:id/products/:productId` | Editar produto |
| `POST /api/admin/restaurants/:id/media` | Carregar imagem validada |
| `POST /api/admin/restaurants/:id/publish` | Publicar uma versão validada |

O servidor deve verificar o acesso ao restaurante em cada operação administrativa. Receber um ID ou slug do cliente não constitui autorização. O mesmo cuidado aplica-se a ficheiros, caches e tarefas de processamento.

## 13. Ligação à base do Notion

### Recursos criados

- [Preparação do menu online](https://app.notion.com/p/3f4a10a852fe811a8dbacae2b1fa687a)
- [Produtos — Menu Cachupa Rst](https://app.notion.com/p/ce151b40cc354427b14ed81516d14f37)

A base do Notion serve inicialmente para recolher e validar conteúdo durante a visita ao restaurante. A base contém 86 produtos na revisão de 13 de outubro de 2026. Estes dados ainda não foram importados para o menu do site.

### Correspondência principal

| Notion | Destino no menu |
|---|---|
| Produto | Nome apresentado |
| Categoria | Categoria do menu |
| Família do produto | Agrupamento de variantes |
| Variante / porção | Tamanho, dose ou versão |
| Preço + Moeda | Valor mostrado ao cliente |
| Descrição para o menu | Descrição pública |
| Ingredientes | Ingredientes apresentados |
| Acompanhamentos incluídos | Complementos incluídos |
| Extras e respetivos preços | Extras, a estruturar na importação |
| Alergénios + Informação alimentar validada | Informação alimentar confirmada |
| Disponibilidade + Dias / horários | Condições de venda |
| Fotografias | Imagens permanentes do produto |
| Destaque + Ordem no menu | Apresentação e ordenação |
| Estado | Elegibilidade para publicação |
| Código | Identificador de origem para futuras atualizações |

### Publicação do conteúdo

```text
Recolher no Notion
      ↓
Validar com a equipa
      ↓
Exportar/importar com identificadores estáveis
      ↓
Preparar imagens e traduções
      ↓
Pré-visualizar
      ↓
Publicar uma versão do menu
```

Não usar URLs temporários dos anexos como endereço definitivo de imagens do site. Durante a importação, copiar os ficheiros autorizados para armazenamento próprio e guardar as referências permanentes.

Aprovar uma linha no Notion não publica automaticamente o menu: essa integração ainda não existe.

## 14. Estrutura futura de pastas

```text
Site/
├── ESTRUTURA-DO-SITE.md       Este documento
├── menu/                     Cópia existente e funcional
│
├── [a criar] páginas públicas
├── [a criar] galeria e coleção de obras
├── [a criar] componentes partilhados
├── [a criar] estilos e tokens de marca
├── [a criar] API / funções de servidor
├── [a criar] esquema e migrações de dados
├── [a criar] integração/importação do Notion
└── [a criar] testes de integração e fluxos
```

Os nomes concretos dependem da stack escolhida. Não mover nem substituir o menu original em `Documents/menu-luxury-ref`.

## 15. Estados de interface a prever

| Situação | Resposta esperada |
|---|---|
| Menu a carregar | Indicação breve, mantendo a estrutura estável |
| Categoria sem produtos | Mensagem clara e acesso às restantes categorias |
| Menu indisponível | Explicação e alternativa de contacto; sem inventar preços |
| Imagem em falta | Apresentação legível do produto sem imagem quebrada |
| Galeria sem obras publicadas | Mensagem discreta; não mostrar quadros fictícios nem destaques vazios na página inicial |
| Imagem de obra indisponível | Manter título e autoria legíveis, com indicação de imagem indisponível |
| Tradução em falta | Texto no idioma alternativo definido |
| Formulário inválido | Erros junto dos campos, preservando o que foi preenchido |
| Reserva em envio | Evitar múltiplos envios e anunciar o estado |
| Reserva recebida | Explicar que aguarda confirmação da equipa |
| Falha de envio | Permitir tentar novamente ou contactar o restaurante |
| Página não encontrada | Ligação à página inicial e ao menu |

## 16. Critérios de aceitação do MVP

- [ ] As seis páginas principais estão acessíveis e ligadas entre si.
- [ ] O menu abre em `/menu/`, no mesmo domínio.
- [ ] A galeria abre em `/galeria/` e tem acesso pela navegação e pela página inicial.
- [ ] As pinturas mantêm a proporção original e o detalhe funciona com toque e teclado.
- [ ] Autoria, créditos e autorização de publicação das obras estão confirmados.
- [ ] Logo, cores e fontes correspondem à identidade definida.
- [ ] Os produtos reais foram validados e substituem os de demonstração antes do lançamento público.
- [ ] Os preços dos destaques e do menu vêm da mesma fonte.
- [ ] Variantes e porções são compreensíveis.
- [ ] Existe regresso claro do menu para o site.
- [ ] Não há scroll horizontal indesejado a 320 e 390 px.
- [ ] O detalhe funciona com toque e teclado; o foco e o scroll são recuperados.
- [ ] Os idiomas publicados têm conteúdo completo ou alternativa explícita.
- [ ] Morada, contactos, horários e disponibilidade estão confirmados.
- [ ] O pedido de reserva é recebido realmente pela equipa, com mensagens de estado corretas.
- [ ] Segredos e credenciais não são expostos no navegador.
- [ ] Dados de clientes e ferramentas administrativas têm acesso restrito.
- [ ] No SaaS, um utilizador não consegue ler ou alterar dados privados de outro restaurante, mesmo manipulando IDs.
- [ ] As imagens estão dimensionadas e os erros de carregamento têm tratamento.
- [ ] Títulos, descrições de página, favicon e imagem de partilha estão configurados.
- [ ] A informação de privacidade corresponde aos serviços e dados efetivamente utilizados.
- [ ] Foram testados os fluxos principais em navegadores atuais e dispositivos móveis reais.

## 17. Ordem de implementação

1. **Confirmar o conteúdo:** produtos, fotografias, cidade, morada, horários, contactos, história e materiais do pintor.
2. **Construir a estrutura pública:** cabeçalho, rodapé, páginas, galeria de quadros e navegação.
3. **Integrar o menu existente:** entrada em `/menu/`, regresso ao site e identidade consistente.
4. **Definir a publicação dos dados:** importação controlada do Notion ou ligação ao backend do SaaS.
5. **Implementar reservas:** processamento, persistência, notificações e confirmação manual.
6. **Validar UX/UI:** mobile, teclado, idiomas, imagens e estados de erro.
7. **Preparar publicação:** domínio, HTTPS, configuração de produção e verificação final do conteúdo.
8. **Evoluir a gestão SaaS:** autonomia por restaurante, publicação versionada e operações de manutenção.

## 18. Limites do que já está pronto

| Elemento | Estado conhecido |
|---|---|
| Logo fornecida | Disponível |
| Proposta de identidade e manual | Disponível em PDF e SVG |
| Pasta do site | Criada |
| Menu adaptado ao Cachupa | Criado e verificado; dados de demonstração mantidos |
| Original do menu | Preservado na pasta de origem |
| Base de produtos no Notion | Criada para recolha e validação |
| Galeria do pintor cabo-verdiano | Página e modelo de obras implementados; artista e obras por fornecer |
| Páginas públicas | Base estática implementada; conteúdos reais e revisão final pendentes |
| Backend, administração e isolamento entre restaurantes | Não presentes nesta pasta |
| Ligação automática ao Notion | Por implementar |
| Reservas reais | Por implementar |
| Domínio e publicação de produção | Por definir |

