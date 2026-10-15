# Cachupa Rst — Estrutura e especificação completa do site

**Versão:** 3.0  
**Data:** 13 de outubro de 2026  
**Projeto:** Cachupa Rst / Cachupa Restaurante  
**Fase:** definição do site institucional e da experiência visual; execução por Codex e Gemini, coordenada pela Orca  
**Formato:** documento de trabalho editável em Markdown

Este documento substitui a estrutura anterior. A decisão mais recente é concentrar o trabalho no site, deixar o menu online para uma fase posterior e encaminhar as reservas para o WhatsApp. O contacto por email será feito através de uma ligação para o programa de correio do visitante.

A base estática do site já existe. Este documento descreve o resultado a construir, não afirma que todas as funcionalidades abaixo estejam implementadas. O documento anterior foi guardado em `documentation/archive/ESTRUTURA-antes-de-reservas-whatsapp.md`.

---

## Organização do trabalho

Orca coordena, Codex implementa o frontend e Gemini o backend. As regras canónicas estão em [workflow](workflow.md), [arquitetura](architecture.md), [contrato](api-contract.md) e [briefing da Orca](orca-briefing.md). Esta especificação descreve o produto. Em questões de organização, estes documentos substituem as versões anteriores.

## 1. Visão do projeto

O site deve apresentar um restaurante cabo-verdiano cuja especialidade é a cachupa. A experiência deve fazer o visitante conhecer a comida, sentir o ambiente do espaço, descobrir a ligação à pintura cabo-verdiana e encontrar rapidamente uma forma de visitar ou contactar o restaurante.

A fotografia passa a ser o principal elemento visual. A marca, a tipografia e os textos devem dar contexto às imagens. A página inicial atual, com grande destaque tipográfico e repetição da logo, é apenas uma base: será reformulada quando as imagens forem disponibilizadas.

### 1.1 Decisões confirmadas

| Tema | Decisão |
|---|---|
| Identidade | Cachupa Rst, usando a logo fornecida e a identidade já desenvolvida |
| Cultura | Cabo Verde, com a cachupa em destaque |
| Linguagem visual | Site predominantemente visual, com fotografias reais |
| Imagens | O utilizador tem imagens de pratos, espaço, quadros e restantes áreas; pasta a partilhar |
| Reservas | Encaminhamento para WhatsApp |
| Email | Ligação direta para email |
| Arte | Área dedicada aos quadros de um pintor cabo-verdiano |
| Menu online | Trabalho adiado; preservar o módulo existente |
| Venda de quadros | Não confirmada; considerar exposição nesta fase |
| Publicação | Não realizada; domínio e alojamento por definir |

### 1.2 Propostas deste documento

A ordem dos blocos, os layouts, os nomes internos de componentes e o modelo de dados são propostas de implementação. Podem ser ajustados depois de analisar as imagens. Não alterar decisões confirmadas por conveniência técnica.

### 1.3 Objetivos do visitante

1. Perceber que restaurante é, que cozinha serve e onde fica.
2. Ver os pratos e reconhecer a cachupa como especialidade.
3. Conhecer o espaço antes da visita.
4. Pedir uma reserva através do WhatsApp.
5. Consultar horários e abrir direções.
6. Conhecer as obras e o pintor.
7. Contactar o restaurante por email.

### 1.4 Objetivos do restaurante

- Apresentar uma identidade própria e reconhecível.
- Transformar interesse em conversas de reserva e visitas.
- Reduzir dúvidas sobre localização, horários e contacto.
- Valorizar a cozinha e a cultura cabo-verdianas.
- Ter conteúdo simples de atualizar, sem duplicação desnecessária.

---

## 2. Âmbito desta fase

### Incluído

- Página inicial com apresentação fotográfica.
- Página sobre o restaurante, a equipa e o espaço.
- Galeria de obras e apresentação do pintor.
- Página de reservas com encaminhamento para WhatsApp.
- Página de contactos com email, WhatsApp, telefone e direções quando confirmados.
- Cabeçalho, navegação móvel e rodapé comuns.
- Informação de privacidade correspondente à implementação real.
- Página de erro 404.
- Organização e otimização das imagens.
- Acessibilidade, desempenho e metadados de pesquisa e partilha.
- Configuração central de contactos, horários e conteúdos.

### Adiado

- Alteração do design ou dos dados do menu online.
- Importação e sincronização dos produtos do Notion.
- Administração do SaaS e separação de dados entre restaurantes.
- Sistema próprio de reservas, disponibilidade de mesas e confirmação automática.
- Pagamentos, carrinho, encomendas e entregas.
- Loja de quadros, preços de obras e checkout.
- Contas de visitantes e newsletter.

A pasta `menu/` continua preservada. Não mostrar o catálogo de demonstração como carta real numa publicação pública. Enquanto não estiver pronto, esconder o acesso público ou apresentar um aviso claro; manter acesso de pré-visualização para revisão interna.

---

## 3. Arquitetura de informação

### 3.1 Mapa do site

```text
Cachupa Rst
│
├── Início                       /
│   ├── Fotografia principal e apresentação
│   ├── Cachupa e cozinha
│   ├── Espaço e ambiente
│   ├── Arte cabo-verdiana
│   └── Convite à visita
│
├── A nossa casa                  /a-nossa-casa/
│   ├── História
│   ├── Pessoas e cozinha
│   └── Fotografias do espaço
│
├── Galeria                       /galeria/
│   ├── Apresentação do pintor
│   ├── Grelha de quadros
│   └── Detalhe ampliado de cada obra
│
├── Reservas                      /reservas/
│   └── Abrir conversa no WhatsApp
│
├── Contactos                     /contactos/
│   ├── Morada e horários
│   ├── WhatsApp, email e telefone
│   └── Direções
│
├── Privacidade                   /privacidade/
├── Página não encontrada         /404.html
│
└── Menu online — fase posterior  /menu/
```

### 3.2 Navegação principal

**Proposta nesta fase:** Início · A nossa casa · Galeria · Contactos · botão “Reservar por WhatsApp”.

O botão principal abre diretamente o WhatsApp. A página `/reservas/` continua acessível no rodapé e nos contextos onde seja útil explicar o processo. Assim, quem já decidiu reservar não precisa de passar por uma página intermédia.

Quando o menu estiver pronto, acrescentar “Menu” à navegação. Nenhuma ligação deve conduzir a uma demonstração sem identificação.

### 3.3 Hierarquia das ações

| Prioridade | Ação | Utilização |
|---|---|---|
| Principal | Reservar por WhatsApp | Cabeçalho, final da página inicial, contactos e reservas |
| Secundária | Conhecer a casa | Apresentação inicial e secções sobre o espaço |
| Secundária | Ver os quadros | Destaque da galeria |
| Utilitária | Como chegar | Contactos e informação de visita |
| Utilitária | Enviar email | Contactos, reservas e rodapé |
| Futura | Ver menu | Apenas quando o menu real estiver pronto |

Evitar mais de duas ações concorrentes na mesma área. Nem todas as secções precisam de um botão.

---

## 4. UX — percursos e comportamento

### 4.1 Primeiro contacto

```text
Pesquisa / redes sociais / ligação direta
                  ↓
      Fotografia + nome + tipo de cozinha
                  ↓
     Conhecer comida, espaço e localização
                  ↓
       Reservar por WhatsApp / Como chegar
```

O primeiro ecrã deve transmitir identidade, comida e uma ação clara. Depois de confirmada, a cidade deve aparecer cedo no percurso, sem obrigar a procurar a morada no rodapé.

### 4.2 Reserva

```text
Clicar em “Reservar por WhatsApp”
                ↓
Abrir WhatsApp com uma mensagem por enviar
                ↓
Visitante completa os dados e envia a mensagem
                ↓
Equipa responde e confirma a disponibilidade
```

O clique não equivale a envio nem a reserva confirmada. O site não recebe o conteúdo da conversa e não deve mostrar “Reserva concluída”.

### 4.3 Email

```text
Clicar em “Enviar email”
            ↓
Abrir aplicação de correio com destinatário e assunto
            ↓
Visitante escreve e envia
```

O endereço deve permanecer visível e selecionável. Disponibilizar “Copiar email” como alternativa, com confirmação acessível de cópia e tratamento de falha. Se não existir programa de correio configurado, o visitante consegue usar o endereço noutro serviço.

### 4.4 Descoberta da arte

```text
Destaque na página inicial ou navegação
                 ↓
              Galeria
                 ↓
         Escolher uma pintura
                 ↓
     Ver imagem completa e ficha
                 ↓
 Fechar e regressar à mesma posição
```

### 4.5 Regras de interação

- Manter o comportamento habitual de links e do botão Voltar do navegador.
- Identificar ligações externas, sobretudo quando abrem uma aplicação.
- Não abrir janelas de reserva automaticamente.
- Não bloquear o scroll com efeitos de apresentação.
- Preservar posição e foco ao fechar o detalhe de uma obra.
- Não depender de hover para mostrar informação essencial.
- Evitar pop-ups promocionais, música automática e carrosséis automáticos.
- Se faltarem contactos, mostrar um estado honesto de preparação na pré-visualização; bloquear publicação final até completar os campos essenciais.

---

## 5. UI — direção visual

### 5.1 Conceito

**Fotografia real, comida em primeiro plano e espaço para a cultura.**

A personalidade deve vir dos pratos, das pessoas, do espaço e da pintura. A marca liga essas imagens entre si. Evitar uma sucessão de cartões iguais, grandes áreas vazias preenchidas por slogans ou a repetição da logo como substituto da fotografia.

### 5.2 Paleta

| Cor | Valor | Papel |
|---|---|---|
| Azul da marca | `#006C9A` | Navegação, secções institucionais e detalhes |
| Vermelho | `#DD1A2A` | Ações principais e apontamentos |
| Amarelo | `#FFED00` | Acentos pequenos e contrastes sobre azul |
| Branco | `#FFFFFF` | Área de leitura e fundo da galeria |
| Papel | `#F5F1E8` | Apoio pontual a secções editoriais |
| Texto escuro | `#12323C` | Texto sobre fundos claros |

Não usar todas as cores com a mesma intensidade em cada secção. Validar contraste das combinações reais, incluindo texto sobre fotografia. Amarelo sobre branco não serve para texto essencial.

### 5.3 Tipografia

| Fonte | Utilização |
|---|---|
| Big Shoulders Bold | Títulos e chamadas curtas |
| Work Sans Regular | Texto, legendas e navegação |
| Work Sans Bold | Botões e informação que exige destaque |
| Nothing You Could Do | Apontamento curto e ocasional |

Usar ficheiros locais e conservar as licenças existentes. A logo fornecida mantém-se como imagem vetorial; não a reconstruir com fontes de apoio.

Escala de referência, ajustável às fotografias e ao comprimento dos textos:

- Título principal: aproximadamente 64–112 px em desktop e 42–64 px em mobile.
- Títulos de secção: 40–64 px em desktop e 32–42 px em mobile.
- Texto: 16–18 px, entrelinha confortável.
- Legendas: 14–16 px; evitar texto demasiado pequeno sobre imagens.
- Limitar blocos de leitura a cerca de 60–70 caracteres por linha.

### 5.4 Composição

- Fotografias grandes com função clara, alternando enquadramentos de detalhe e ambiente.
- Texto alinhado à esquerda na maioria das secções.
- Alternar imagem à esquerda e à direita quando isso ajudar o ritmo da leitura.
- Reservar branco em torno dos quadros para que a identidade do restaurante não concorra com a obra.
- Usar cantos e sombras com moderação; não aplicar um tratamento de “cartão” a cada fotografia.
- As secções podem ter profundidades diferentes; não forçar a mesma altura em todo o site.

### 5.5 Movimento

- Transições discretas em botões, navegação e abertura de detalhes.
- Sem animações repetitivas a cada scroll.
- Sem parallax obrigatório ou vídeos automáticos como dependência do primeiro ecrã.
- Respeitar `prefers-reduced-motion`.

---

## 6. Página inicial

### 6.1 Objetivo

Apresentar a experiência do restaurante através de imagens e conduzir naturalmente à visita.

### 6.2 Estrutura proposta

| Bloco | Imagem | Texto | Ação |
|---|---|---|---|
| Apresentação | A melhor fotografia de cachupa, mesa ou espaço, escolhida após analisar a pasta | Nome, cozinha cabo-verdiana, cidade e uma frase curta | Reservar por WhatsApp / Conhecer a casa |
| A cachupa | Prato principal em destaque e, se útil, um detalhe | A especialidade e as suas particularidades confirmadas | Opcional; ligação ao menu apenas numa fase posterior |
| A cozinha | Duas ou três fotografias complementares | Legendas curtas com nomes reais dos pratos | Sem botão obrigatório |
| A casa | Fotografia ampla do interior ou da mesa | Atmosfera e convite a conhecer o espaço | Conhecer a casa |
| O pintor e os quadros | Uma obra completa ou uma seleção de duas a três obras | Nome do artista e introdução breve | Ver os quadros |
| Visita | Imagem do espaço, entrada ou mesa | Morada resumida e horários essenciais | Reservar por WhatsApp / Como chegar |

### 6.3 Wireframe de desktop

```text
┌────────────────────────────────────────────────────────────┐
│ Logo       A nossa casa   Galeria   Contactos    WhatsApp   │
├────────────────────────────────────────────────────────────┤
│                                                            │
│             Fotografia principal em grande                 │
│                                                            │
│  Título curto                                              │
│  Cozinha cabo-verdiana + cidade                             │
│  [Reservar por WhatsApp] [Conhecer a casa]                   │
├─────────────────────────────┬──────────────────────────────┤
│ Fotografia da cachupa       │ A especialidade da casa       │
│                             │ Texto breve                  │
├─────────────────────────────┴──────────────────────────────┤
│ Fotografias da cozinha, com legendas                        │
├──────────────────────────┬─────────────────────────────────┤
│ Conhecer o restaurante    │ Fotografia ampla do espaço      │
├──────────────────────────┴─────────────────────────────────┤
│ Nome do pintor       Obras completas, sem cortes            │
│                     [Ver os quadros]                       │
├────────────────────────────────────────────────────────────┤
│ Visite-nos       Horários / morada       [WhatsApp]         │
├────────────────────────────────────────────────────────────┤
│ Rodapé com contactos, email e navegação                     │
└────────────────────────────────────────────────────────────┘
```

### 6.4 Primeiro ecrã

Escolher entre fotografia com texto sobreposto ou uma composição dividida, consoante a imagem permita leitura. Não decidir o recorte final sem ver os ficheiros.

Se o texto ficar sobre a fotografia, usar uma área visualmente tranquila e uma camada de contraste discreta. Em mobile, aceitar texto abaixo da imagem quando isso proteger o enquadramento e a leitura.

### 6.5 Conteúdo

- Texto curto e concreto, escrito a partir da informação real do restaurante.
- Sem avaliações fictícias, prémios, datas de fundação ou citações inventadas.
- Sem preços na página inicial nesta fase, evitando divergências com o futuro menu.
- Distinguir uma fotografia ilustrativa da carta de um prato atualmente disponível.
- Não atribuir ingredientes, técnicas ou porções apenas com base na aparência de uma imagem.

---

## 7. A nossa casa — `/a-nossa-casa/`

### Objetivo

Mostrar o espaço, as pessoas e a ligação do restaurante à cultura cabo-verdiana.

### Ordem proposta

1. Fotografia ampla do espaço e apresentação curta.
2. História do restaurante em dois ou três parágrafos, validada pelos responsáveis.
3. Equipa e cozinha, se houver fotografias e autorização para apresentação.
4. Galeria do ambiente: interior, mesas, detalhes e exterior.
5. Ligação entre a casa e o trabalho do pintor, com ligação à galeria.
6. Convite para reservar por WhatsApp.

### Regras

- Mostrar fotografias complementares; não repetir cinco enquadramentos praticamente iguais.
- Usar legendas quando ajudarem a perceber o espaço.
- Fotografias do ambiente podem abrir em ampliação, se houver utilidade real.
- A galeria do espaço pertence a esta página; a página “Galeria” fica reservada às obras.
- Não usar uma narrativa turística genérica como substituto da história do restaurante.

---

## 8. Galeria — `/galeria/`

### 8.1 Objetivo

Dar protagonismo aos quadros de um pintor cabo-verdiano, com uma experiência calma e centrada na obra.

### 8.2 Estrutura

- Nome artístico e introdução breve.
- Retrato do pintor, se existir e se fizer sentido na composição.
- Grelha de obras publicadas.
- Biografia e ligação oficial, quando fornecidas.
- Créditos das obras e das fotografias.

### 8.3 Lista de obras

Cada obra apresenta imagem completa, título e ano quando conhecidos. A grelha adapta-se às proporções reais das pinturas. Usar uma coluna em mobile e duas ou três em desktop, conforme os formatos e a quantidade.

Não aplicar cortes automáticos, filtros cromáticos, molduras inventadas, efeitos de perspetiva ou texto sobre as pinturas. Uma fotografia do quadro na parede pode contextualizar a exposição, mas a visualização principal deve mostrar a obra com clareza.

### 8.4 Detalhe ampliado

- Imagem em maior resolução, preservando a proporção.
- Título, autoria, ano, técnica e dimensões disponíveis.
- Descrição apenas se fornecida ou aprovada pelo artista.
- Créditos.
- Botão de fecho sempre visível.
- Navegação “Anterior” e “Seguinte” quando houver várias obras; indicar a posição na coleção.
- Acesso por toque, rato e teclado.
- Escape fecha; foco regressa à obra de origem; scroll regressa à posição anterior.
- Não depender de gestos de deslizar para navegar.

### 8.5 Limites

Exposição, sem compra nem pedido comercial por obra nesta fase. O botão de reservas do restaurante não deve ser confundido com contacto para compra de um quadro.

Se a coleção estiver vazia, mostrar uma mensagem de preparação na pré-visualização. Não publicar grelhas com molduras vazias ou obras fictícias.

---

## 9. Reservas — `/reservas/`

### 9.1 Conteúdo

Uma página simples com fotografia do espaço, explicação breve e botão “Reservar por WhatsApp”. Não precisa de formulário.

Texto funcional proposto:

> Para reservar, fale connosco no WhatsApp e indique o dia, a hora e o número de pessoas. A equipa confirma a disponibilidade consigo.

Abaixo do botão:

> O pedido só fica confirmado depois da resposta da equipa.

Incluir email como alternativa de contacto. Não prometer tempo de resposta nem disponibilidade automática.

### 9.2 Construção da ligação

Usar o número real de WhatsApp do restaurante, em formato internacional, apenas com algarismos. O número de WhatsApp pode ser diferente do telefone geral e deve ter um campo próprio.

Padrão técnico:

```text
https://wa.me/{numero_internacional}?text={mensagem_codificada}
```

Mensagem inicial proposta:

```text
Olá! Gostaria de reservar uma mesa no Cachupa Rst.

Data:
Hora:
Número de pessoas:
Nome:
```

Codificar a mensagem com uma função própria para parâmetros de URL, como `encodeURIComponent`. Não inserir diretamente texto não codificado na ligação.

### 9.3 Comportamento

- Abrir apenas após clique do visitante.
- O WhatsApp apresenta a mensagem; o visitante é quem a envia.
- Testar em telemóvel e desktop, com os diferentes caminhos oferecidos pelo WhatsApp.
- Manter número visível para quem prefira iniciar a conversa manualmente.
- Não afirmar que é possível detetar com fiabilidade se a aplicação está instalada.
- Não usar a API do WhatsApp Business nem automatizar mensagens nesta fase.
- Não guardar nome, telefone, data ou número de pessoas no site.

### 9.4 Email

Padrão técnico:

```text
mailto:{email}?subject={assunto_codificado}
```

Assunto proposto: `Contacto pelo site — Cachupa Rst`.

Usar texto “Enviar email” e mostrar o endereço. Evitar formulários que simulem o envio de email sem serviço real.

---

## 10. Contactos — `/contactos/`

### Estrutura

| Área | Conteúdo |
|---|---|
| Identificação | Nome do restaurante e fotografia da entrada ou fachada |
| Morada | Endereço completo e cidade |
| Horários | Horários por dia, intervalos e dias de encerramento |
| WhatsApp | Número e botão de reserva |
| Email | Endereço visível, ligação e opção de copiar |
| Telefone | Ligação `tel:` se houver telefone de contacto confirmado |
| Direções | Botão “Como chegar” para o endereço exato no serviço de mapas escolhido |
| Informações práticas | Acessibilidade, transportes e estacionamento apenas quando confirmados |

### Mapa

Preferir inicialmente uma ligação externa para direções. Um mapa incorporado só deve ser adicionado se melhorar a experiência, considerando carregamento e serviços externos. Não fazer pedidos a serviços de mapas só para decorar a página.

### Horários

Representar claramente dias encerrados e períodos separados de almoço/jantar. Não apresentar “Aberto agora” sem lógica de fuso horário e exceções validada. Na primeira versão, horários estáticos claros são suficientes.

---

## 11. Cabeçalho, navegação móvel e rodapé

### Cabeçalho desktop

- Logo única e legível, com ligação ao início.
- Navegação curta.
- Ação principal de WhatsApp visível.
- Indicação discreta da página atual.
- Cabeçalho fixo apenas se não roubar demasiada área às imagens; compensar âncoras e foco se utilizado.

### Mobile

- Logo, botão de navegação e acesso claro à reserva.
- Navegação expansível com `aria-expanded` e `aria-controls`.
- Se for um painel modal: gerir foco, fecho e scroll como modal. Se for uma expansão no fluxo: não prender o foco.
- Fechar por botão ou Escape; impedir que ligações ocultas recebam foco.
- Áreas de toque confortáveis; objetivo de 44 × 44 px para ações principais.
- Não sobrepor botão flutuante, barra fixa, navegação e consentimento na mesma zona.

### Rodapé

Nome, cozinha, morada resumida, horários essenciais, WhatsApp, email, redes sociais confirmadas, navegação secundária e privacidade. Usar a mesma fonte de dados dos contactos.

---

## 12. Estratégia de imagens

### 12.1 Princípio

As imagens existem e serão fornecidas. Não produzir fotografias artificiais nem substituir pratos e obras reais por imagens de stock. A seleção definitiva e os recortes dependem da análise da pasta.

### 12.2 Inventário ao receber a pasta

1. Identificar ficheiros e separar pratos, espaço, equipa, obras, artista e marca.
2. Registar dimensões, orientação, formato e qualidade técnica.
3. Detetar duplicados e escolher o melhor ficheiro de cada enquadramento.
4. Associar cada fotografia ao prato, local ou obra corretos.
5. Identificar imagens adequadas a desktop e mobile.
6. Registar créditos e condições de utilização.
7. Propor a distribuição pelas páginas antes de otimizar.

### 12.3 Matriz de utilização

| Uso | Requisitos | Tratamento |
|---|---|---|
| Fotografia principal | Forte leitura, boa resolução, assunto claro | Recortes distintos para desktop/mobile se necessário |
| Especialidade | Prato identificável e apetecível | Preservar apresentação real e ponto focal |
| Ambiente | Enquadramento que explique o espaço | Combinar vistas amplas e detalhes |
| Equipa | Pessoas identificadas e conteúdo autorizado | Sem nomes ou funções inferidos |
| Quadros | Cor e proporção fiéis, boa legibilidade | Mostrar completos, sem filtros |
| Retrato do pintor | Identificação confirmada | Crédito e texto contextual |
| Partilha social | Imagem legível em miniatura | Composição própria a partir de imagem autorizada |

### 12.4 Ficheiros e derivados

```text
Originais fornecidos — preservar
            ↓
Seleção editorial e associação a cada conteúdo
            ↓
Derivados otimizados para a web
            ↓
Miniaturas / imagens de secção / imagens ampliadas
            ↓
Manifesto de imagens com dimensões, alt e créditos
```

Guardar originais fora da pasta publicada. Não alterar ficheiros de origem. Nomes de ficheiro descritivos, sem espaços, com identificadores estáveis.

### 12.5 Otimização

- Gerar tamanhos adequados ao uso; exemplo: 480, 800, 1280 e 1920 px quando a origem permitir.
- Não ampliar artificialmente imagens pequenas.
- Usar `srcset` e `sizes`; recorrer a `picture` quando forem necessários formatos ou recortes alternativos.
- Preparar WebP e/ou AVIF com alternativa adequada.
- Declarar largura e altura para evitar saltos de layout.
- Carregar a imagem principal sem lazy loading; priorizar apenas a imagem realmente crítica.
- Usar lazy loading nas imagens abaixo da primeira área visível.
- Carregar a versão ampliada das obras apenas quando necessária.
- Remover metadados desnecessários dos derivados; conservar créditos visíveis e o original arquivado.
- Avaliar a fidelidade de cor das pinturas após compressão.

### 12.6 Orçamento indicativo

Procurar uma imagem principal de aproximadamente 200–400 KB e miniaturas de 50–150 KB, sem sacrificar qualidade visível. São objetivos a ajustar às imagens reais. Evitar que a primeira vista descarregue toda a coleção ou ficheiros originais de vários megabytes.

---

## 13. Responsividade

| Ecrã | Composição |
|---|---|
| Telemóvel pequeno, desde 320 px | Uma coluna, títulos contidos, ações sem sobreposição |
| Telemóvel habitual | Imagens grandes, textos curtos, navegação recolhida |
| Tablet | Uma ou duas colunas consoante o conteúdo |
| Desktop | Grelhas de duas ou três colunas e secções fotográficas mais amplas |
| Ecrã muito largo | Limitar largura do texto; permitir imagens amplas sem esticar conteúdo |

Breakpoints devem responder ao conteúdo, não apenas a modelos de dispositivo. Verificar 320, 390, 768, 1024 e 1440 px, além de orientação horizontal e ampliação de texto.

Testar títulos longos de obras, email comprido, nomes do artista e horários em várias linhas. Não fixar alturas que cortem texto.

---

## 14. Acessibilidade

- Um `h1` por página e hierarquia coerente de títulos.
- `header`, `nav`, `main` e `footer` semânticos.
- Ligação para saltar para o conteúdo.
- Texto alternativo útil para imagens informativas; `alt=""` para imagens puramente decorativas.
- Nas obras, descrever elementos visuais sem inventar interpretação artística.
- Informação essencial em texto HTML, não apenas dentro de fotografias.
- Contraste verificado nos estados normal, hover, foco e desativado.
- Foco visível e percurso completo por teclado.
- Diálogos com nome acessível, fecho evidente e recuperação de foco.
- Anunciar o resultado de “Copiar email” sem deslocar o foco.
- Não usar apenas cor para indicar estado.
- Respeitar redução de movimento e ampliação de texto.
- Testar o conteúdo principal com JavaScript desativado: textos, contactos e links devem continuar disponíveis.

---

## 15. Arquitetura técnica e backend

### 15.1 Tecnologia de base

| Tecnologia | Papel |
|---|---|
| HTML | Páginas semânticas, conteúdos e ligações |
| CSS | Identidade visual, layout e responsividade |
| JavaScript | Navegação móvel, detalhe de obras e cópia de email |
| JSON | Conteúdo estruturado e configuração |
| Python | Gerar páginas durante a preparação/publicação |
| Alojamento estático | Servir os ficheiros públicos através de HTTPS |

A base atual já usa esta combinação. Não é necessário migrar para um framework para construir a experiência definida. A proposta é continuar com geração estática e componentes de template partilhados.

### 15.2 Diagrama

```text
Edição local de textos + dados + imagens
                    ↓
         Validação de conteúdo e ficheiros
                    ↓
          Gerador de páginas em Python
                    ↓
       HTML + CSS + JavaScript + imagens
                    ↓
          Alojamento estático / CDN
                    ↓
                  Visitante
                  ├── Vê páginas e galeria
                  ├── Abre WhatsApp por ligação
                  ├── Abre email por mailto
                  └── Abre direções no serviço de mapas
```

### 15.3 O que o backend precisa de fazer nesta fase

**Não é necessário um backend de aplicação em execução para os requisitos atuais.**

O alojamento entrega ficheiros. O gerador prepara as páginas antes da publicação. WhatsApp e email são ligações externas iniciadas pelo visitante. Não existe processamento de reservas no servidor do restaurante.

Não criar endpoints fictícios, tabelas de reservas vazias ou uma autenticação sem função. Não pedir credenciais do WhatsApp, do email ou do Notion para fazer simples links.

### 15.4 Responsabilidades reais

| Área | Responsabilidade |
|---|---|
| Gerador | Compor páginas a partir de templates e dados; escapar texto |
| Validação | Verificar campos obrigatórios, ficheiros, URLs e consistência |
| Processamento de imagens | Criar derivados e preservar originais |
| Alojamento | HTTPS, ficheiros, cache, redirecionamentos e erros 404 |
| JavaScript no navegador | Interações locais, sem acesso a credenciais |
| WhatsApp | Conversa e confirmação manual fora do site |
| Aplicação de email | Redação e envio feitos pelo visitante |

### 15.5 Quando um backend poderá passar a fazer sentido

Apenas com novos requisitos, como edição por uma equipa através de um painel, reservas próprias, sincronização de conteúdo ou integração do SaaS. Nessa fase, definir autenticação, autorização, base de dados, APIs e operação a partir do requisito concreto.

O menu continua independente deste planeamento. Não acoplar o site a uma arquitetura SaaS ainda não validada.

---

## 16. Modelo de conteúdo

### 16.1 Configuração do restaurante

| Campo proposto | Conteúdo |
|---|---|
| `name` | Nome apresentado |
| `preview` | Modo de pré-visualização |
| `siteUrl` | Domínio final para metadados e sitemap |
| `city` | Cidade confirmada |
| `address` | Morada completa |
| `phone` | Telefone geral, opcional |
| `whatsappNumber` | Número internacional para reservas |
| `whatsappMessage` | Texto inicial sem dados pessoais pré-preenchidos |
| `email` | Email público |
| `hours` | Horários estruturados por dia e intervalos |
| `directionsUrl` | Ligação confirmada para direções |
| `socialLinks` | Perfis oficiais |

### 16.2 Conteúdo editorial

- Apresentação inicial: título, texto curto, imagem desktop/mobile e respetivo alt.
- Especialidade: título, texto e imagens.
- Casa: história, fotografias, legendas e eventuais pessoas apresentadas.
- Visita: imagem e texto de apoio.
- SEO: título, descrição e imagem de partilha por página.

### 16.3 Artista e obras

| Entidade | Campos |
|---|---|
| Artista | Identificador, nome artístico, biografia, retrato, alt, site/perfil oficial |
| Obra | Identificador, título, artista, ano, técnica, dimensões, descrição autorizada |
| Imagem da obra | Original de referência, derivados, largura, altura, alt e crédito |
| Publicação | Ordem, destaque e indicação de publicado/rascunho |

### 16.4 Regras

- Identificadores estáveis, independentes do nome apresentado.
- Campos desconhecidos vazios; não inventar ano, técnica ou dimensões.
- Só obras publicadas aparecem no site.
- Manter produtos e quadros em coleções separadas.
- Nunca publicar notas internas, ficheiros de preparação ou dados de contacto privados.
- Alterações de morada, WhatsApp e email devem refletir-se em todas as páginas a partir da mesma configuração.

---

## 17. Organização do projeto

Seguir a estrutura definida no README e em [architecture.md](architecture.md): `frontend/src/` e `frontend/public/` para Codex; `backend/src/`, `backend/tests/` e `backend/prisma/` para Gemini; documentação e integração sob coordenação da Orca. A pasta Prisma é apenas reservada. O código legado na raiz permanece até à migração validada.

---

## 18. Componentes a construir

| Componente | Responsabilidade |
|---|---|
| Cabeçalho | Marca, navegação e reserva por WhatsApp |
| Navegação móvel | Expandir/recolher links com acessibilidade |
| Hero fotográfico | Imagem principal, título e ações |
| Secção editorial | Imagem e texto com variações controladas |
| Seleção de pratos | Fotografias e legendas, sem gestão do menu |
| Galeria do espaço | Fotografias do restaurante |
| Cartão de obra | Imagem completa e identificação |
| Detalhe de obra | Ampliação, ficha e navegação entre obras |
| Bloco de visita | Horários, localização e reserva |
| Ligações de contacto | WhatsApp, mailto, tel e cópia de email |
| Rodapé | Dados e navegação comuns |
| Mensagem de estado | Conteúdo em preparação ou falha de imagem |

Componentes são partes reutilizáveis do código; não obrigam ao uso de React ou de outra biblioteca.

---

## 19. Estados e exceções

| Situação | Comportamento |
|---|---|
| Imagem a carregar | Reservar espaço e manter o texto utilizável |
| Imagem indisponível | Mensagem discreta e legenda; sem ícone quebrado dominante |
| Galeria sem obras | Mensagem de preparação na pré-visualização |
| Ficha incompleta | Omitir campos desconhecidos |
| WhatsApp por configurar | Sem link fictício; estado de preparação e bloqueio de publicação |
| Email por configurar | Omitir ação na pré-visualização e sinalizar na validação |
| Cópia de email falha | Manter endereço selecionável e explicar alternativa |
| JavaScript desativado | Links e conteúdo essenciais continuam disponíveis; obras podem ligar à imagem completa |
| Endereço inexistente | Resposta 404 real com caminhos para início e contactos |
| Menu ainda de demonstração | Não apresentar como carta real ao público |
| Obra despublicada | Retirar da grelha e dos destaques na publicação seguinte |

---

## 20. SEO e partilha

- Título e descrição próprios para cada página.
- Nome, cidade e contactos consistentes.
- URLs legíveis e estáveis.
- Canonical e sitemap apenas quando o domínio final estiver definido.
- Imagem de partilha social baseada nos materiais reais.
- Favicon derivado da marca, legível em tamanho pequeno.
- Dados estruturados de restaurante apenas com informação confirmada; não inventar avaliações ou intervalos de preço.
- Texto HTML para identificar obras, artista e imagens.
- Não publicar páginas vazias em múltiplos idiomas.
- Nesta fase, português de Portugal. Os idiomas do módulo de menu não significam que todo o site já esteja traduzido.
- Pré-visualização com `noindex`; produção com indexação revista antes do lançamento.

---

## 21. Privacidade, segurança e serviços externos

### Princípios

O site não recolhe reservas em formulário nem guarda conversas. Uma ligação para WhatsApp ou email encaminha o visitante para um serviço externo.

A informação final de privacidade depende do responsável, do alojamento e dos serviços usados. Não tratar a página provisória como documentação final aprovada.

### Implementação

- HTTPS na produção.
- Nenhuma chave secreta ou credencial nos ficheiros públicos.
- Escapar texto introduzido nos dados e validar esquemas de URL.
- Publicar apenas ficheiros previstos; excluir originais, backups, scripts e notas internas.
- Limitar serviços externos ao necessário.
- Fontes locais; sem dependência de pedidos a fornecedores de fontes.
- Remover geolocalização e outros metadados desnecessários dos derivados de imagens.
- Rever cabeçalhos de segurança segundo o alojamento e os recursos utilizados.
- Proteger pré-visualizações privadas com controlo de acesso quando necessário: `noindex` não é proteção de acesso.

Não acrescentar um banner de cookies decorativo. Avaliar a necessidade e o comportamento quando os serviços reais forem definidos. Se forem adicionadas ferramentas de análise ou incorporações externas, rever a informação e os mecanismos aplicáveis antes da publicação.

---

## 22. Medição opcional

Não é um requisito para construir o site. Se for decidida posteriormente, medir apenas eventos úteis:

- Clique em reservar por WhatsApp.
- Clique em email.
- Clique em direções.
- Abertura de obra.

Um clique no WhatsApp mede intenção de contacto, não reserva confirmada. Não enviar texto de mensagens, nomes, telefones de visitantes ou conteúdo de email para ferramentas de análise.

---

## 23. Publicação e manutenção

### Fluxo proposto

```text
Editar dados e imagens
        ↓
Validar conteúdo e contactos
        ↓
Gerar páginas e derivados
        ↓
Rever pré-visualização em desktop e mobile
        ↓
Publicar os ficheiros públicos
        ↓
Verificar links externos e páginas no domínio final
```

### Regras de operação

- Manter uma versão anterior recuperável antes de cada publicação.
- Definir redirecionamento entre versões do domínio e respostas 404 no alojamento.
- Aplicar cache prolongada a recursos versionados e atualização previsível ao HTML.
- Regenerar o site quando os contactos, horários, obras ou textos mudarem.
- Não depender do servidor Python de desenvolvimento para produção.
- Verificar periodicamente se WhatsApp, email, direções e redes sociais continuam corretos.

---

## 24. Plano de implementação

### Etapa 1 — Confirmar conteúdo e organizar imagens

Receber a pasta, analisar os materiais, relacionar imagens com as secções e listar informações em falta. Confirmar WhatsApp, email, morada, horários e dados do pintor.

**Entrega:** inventário visual e distribuição das fotografias por página.

### Etapa 2 — Reformular a página inicial

Escolher fotografia principal, ajustar composição, cores, tipografia e versão mobile. Trocar o cartaz de marca atual por uma apresentação dominada pela fotografia.

**Entrega:** página inicial visual para revisão.

### Etapa 3 — Construir as páginas interiores

Aplicar a mesma linguagem à casa, galeria, reservas e contactos. Usar conteúdo real e manter componentes partilhados.

**Entrega:** navegação completa com imagens e textos.

### Etapa 4 — Implementar contactos

Configurar WhatsApp, mensagem inicial, email, telefone e direções. Remover qualquer fluxo antigo que implique reserva interna.

**Entrega:** percursos externos funcionais, sem envio automático.

### Etapa 5 — Preparar a galeria

Adicionar artista e obras, otimizar imagens e testar ampliação, anterior/seguinte e teclado.

**Entrega:** coleção real, com créditos e apresentação fiel.

### Etapa 6 — Validar e preparar publicação

Verificar acessibilidade, desempenho, metadados, conteúdos e configuração do alojamento.

**Entrega:** site pronto para publicar depois de concluir a revisão de conteúdo.

O menu online será retomado depois desta fase, sem bloquear a construção das páginas institucionais.

---

## 25. Critérios de aceitação

### Conteúdo e identidade

- [ ] Fotografias reais dominam a apresentação inicial.
- [ ] Logo e fontes correspondem aos materiais aprovados.
- [ ] Textos não inventam história, disponibilidade ou características dos pratos.
- [ ] Morada, cidade, WhatsApp, email e horários foram confirmados.
- [ ] Nome do pintor e identificação das obras foram validados.
- [ ] Créditos e utilização das imagens estão confirmados.
- [ ] Não há conteúdo de demonstração apresentado como real.

### Experiência

- [ ] Todas as páginas principais estão ligadas entre si.
- [ ] A reserva por WhatsApp é fácil de encontrar em mobile.
- [ ] O WhatsApp abre com a mensagem correta, sem a enviar automaticamente.
- [ ] O site explica que a confirmação depende da equipa.
- [ ] Email visível e ligação mailto testada.
- [ ] Cópia de email com feedback e alternativa em caso de falha.
- [ ] Direções apontam para a localização correta.
- [ ] Galeria separada das fotografias do espaço e dos pratos.
- [ ] Imagens das pinturas sem cortes ou deformações.
- [ ] Detalhe da obra fecha e devolve foco e posição.

### Técnica

- [ ] Sem scroll horizontal indesejado nos tamanhos definidos.
- [ ] Layout utilizável com ampliação de texto.
- [ ] Navegação e detalhe funcionam por teclado.
- [ ] Textos alternativos e contraste verificados.
- [ ] Imagem principal otimizada e imagens secundárias com carregamento adequado.
- [ ] Sem erros de consola ou ficheiros em falta.
- [ ] Links essenciais funcionam sem JavaScript.
- [ ] Sitemap, metadados e indexação correspondem ao ambiente.
- [ ] Resposta 404 e redirecionamentos configurados no alojamento.
- [ ] Apenas ficheiros públicos são publicados.
- [ ] Não existe formulário ou mensagem de sucesso a simular uma reserva.

---

## 26. Estado atual e informações em falta

| Elemento | Estado |
|---|---|
| Logo e proposta de identidade | Disponíveis |
| Base HTML/CSS/JS e gerador Python | Implementados |
| Páginas institucionais | Base montada; reformulação visual pendente |
| Fotografias dos pratos, espaço e quadros | Existência confirmada pelo utilizador; pasta ainda por partilhar |
| Galeria | Estrutura e ampliação básica preparadas; obras reais por adicionar |
| Reservas por WhatsApp | Decisão confirmada; número e implementação final pendentes |
| Ligação de email | Decisão confirmada; endereço e implementação final pendentes |
| Menu online | Preservado; desenvolvimento adiado |
| Base de produtos no Notion | Existe; última revisão com 86 registos; fora desta fase |
| Backend de reservas | Não necessário para o fluxo definido |
| Domínio e alojamento | Por definir |

### Dados necessários para concluir

- Pasta de imagens.
- Número de WhatsApp para reservas, com indicativo do país.
- Email público do restaurante.
- Cidade, morada e horários.
- Telefone geral, se diferente do WhatsApp.
- História breve e nomes/funções da equipa que será apresentada.
- Nome artístico, biografia e identificação das obras.
- Perfis oficiais e créditos.

A existência das imagens permite planear um site fortemente visual. A seleção e o layout definitivos serão feitos depois de analisar os ficheiros, preservando o enquadramento dos pratos, a atmosfera do espaço e a integridade das pinturas.


---

## 27. Coordenação e execução

A Orca é a coordenadora e integradora definida pelo utilizador. Seguir [workflow.md](workflow.md), [frontend-rules.md](frontend-rules.md), [backend-rules.md](backend-rules.md) e [testing.md](testing.md). A documentação anterior de dois agentes sem coordenador foi arquivada e não é normativa.
