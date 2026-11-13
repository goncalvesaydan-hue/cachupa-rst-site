# Handoff — frontend

## Entrega de 14 de outubro de 2026

Responsável: Codex. Pedido direto do utilizador: começar o frontend e deixar a integração preparada para o Gemini. Coordenação: Orca.

Estado: implementação funcional de frontend entregue para integração; publicação bloqueada por conteúdo real em falta. Contrato consumido: v1, sem alteração do documento canónico. Nenhum trabalho de backend ou menu efetuado.

## O que está disponível

Sete páginas: início, a nossa casa, galeria, reservas, contactos, privacidade e 404. Layout responsivo com marca e fontes locais; imagens responsivas; detalhe das pinturas com navegação e teclado; reservas por link WhatsApp e email; contactos, horários e estados vazios; metadados básicos e noindex de preview.

Ponto de entrada: `frontend/src/render.py`, função `render_site(model) -> dict[str, str]`. O backend fornece o modelo validado e recebe ficheiros HTML por caminho relativo. A função não escreve em disco. Guia completo e exemplo executável de importação: `frontend/README.md`.

Ficheiros desta entrega: `frontend/src/`, `frontend/public/assets/brand/`, `frontend/fixtures/preview.json`, `frontend/tools/`, `frontend/tests/`, `frontend/package.json`, `frontend/.gitignore`, `frontend/README.md`, `frontend/AGENTS.md` e este handoff. `frontend/dist/` é saída gerada local e ignorada.

## Verificação realizada

- `npm --prefix frontend test`: 8 testes aprovados.
- `npm --prefix frontend run lint`: sintaxe Python, JSON e JavaScript válida.
- `npm --prefix frontend run build:preview`: 7 páginas geradas.
- Navegador: início sem overflow a 320/390/768/1024/1440 px; menu móvel abre e fecha com Escape.
- Galeria: abertura, obra seguinte, Escape e foco devolvido à obra inicial. Dados temporários identificados como teste; removidos da saída depois da verificação.
- Sem erros de consola observados no percurso verificado.

Preview local: http://127.0.0.1:18952/. Não substitui a versão anterior em 18951. Comando de arranque: `cd frontend && npm run dev`.

## Próxima tarefa do Gemini

1. Implementar a normalização e validação do contrato v1 na sua pasta, com testes próprios.
2. Integrar o renderer, copiar recursos de frontend e processar imagens públicas numa distribuição isolada.
3. Validar contactos, IDs/referências, exclusão de rascunhos e diferenças entre preview e produção.
4. Entregar à Orca comando real de build conjunto, resultados e limitações.

Não criar endpoints de reservas, contas de clientes, pagamentos ou SaaS para este MVP. O menu continua fora desta fase.

## Decisões para a Orca

O renderer usa `artist.portrait` como ID de imagem; confirmar a interpretação antes da integração. A stack mantém HTML/CSS/JS e Python sem dependências novas. O adaptador de apresentação está no frontend; o gerador de publicação pertence ao Gemini.

Os documentos partilhados que descrevem os módulos como vazios precisam de atualização pela Orca após aceitar a entrega: README raiz, arquitetura, estratégia de testes e estado de coordenação. Não foram alterados pelo Codex por pertencerem à coordenação. O backend ainda não está integrado; não marcar o build global como concluído com base nos testes deste módulo.

## Pendências antes de publicar

Fotografias reais de pratos/espaço/quadros, dados e autorização do artista, créditos e direitos de uso, contactos e horários confirmados, domínio e texto de privacidade. Revisão visual com fotos reais, testes de integração, links externos sem enviar mensagens, clipboard, falha de imagem, texto ampliado e percurso completo sem JavaScript. Confirmar metadados finais, cache, 404 e desempenho no alojamento.

A fixture é exclusivamente de desenvolvimento. Não deve substituir o conteúdo editorial ou a base de dados futura.

## Revisão visual — 14 de outubro de 2026

O utilizador rejeitou a primeira apresentação e pediu uma versão mais visual. Foi refeita a composição mantendo o contrato v1 e a mesma API do renderer.

- Abertura azul com tipografia de grande escala; quando `heroImageId` existe, a fotografia ocupa todo o fundo do hero, com proteção de contraste para o texto.
- Grafismos existentes da identidade substituem as caixas cinzentas da preview. Recursos provenientes de `Identidade Visual/SVG/`: panela, vapor e grãos. Foram removidas as fontes embutidas não utilizadas desses três SVG, mantendo os caminhos vetoriais.
- Alternância editorial, pinturas sem corte, estados vazios próprios, convite às reservas em vermelho e rodapé tipográfico.
- Documento de direção e justificação: `frontend/VISUAL-DIRECTION.md`.
- A fonte manuscrita local é agora utilizada numa nota decorativa; informação funcional permanece em Work Sans.
- As fotos reais ainda não foram fornecidas. Foi pedido ao utilizador o caminho da pasta. Não substituir conteúdo real por fotografias de demonstração.

Verificação desta revisão: 35 combinações de página/largura (7 rotas × 320/390/768/1024/1440 px), sem overflow horizontal e um h1 em cada página; menu móvel e Escape; sem erros de consola observados. Testes unitários e sintaxe novamente aprovados. Capturas em `visuals/frontend-v2-desktop.png` e `visuals/frontend-v2-mobile.png`.

As pendências de integração, fotografias, acessibilidade com conteúdo final e publicação da entrega anterior continuam aplicáveis. O teste de galeria realizado na primeira entrega não foi repetido nesta revisão; a interação JS manteve-se intacta.

## Fotografias integradas — 14 de outubro de 2026

O utilizador forneceu `/Volumes/Aydan/CACHUPA RESTAURANTE/` e pediu cuidado na seleção. Triadas 429 imagens; selecionados 10 originais para comida, sala e três quadros. Cópias locais WebP em `frontend/public/assets/photos/`; originais intactos. Nenhuma dependência nova no build.

Ler `frontend/PHOTO-SELECTION.md` para os critérios e a tabela de escolhas. `frontend/fixtures/photo-selection.json` regista origem, hashes e variantes. Esse registo não deve ser publicado. A fixture de preview foi atualizada com IDs e alt texts; não copiar metadados provisórios para produção.

Mudança de apresentação: hero fotográfico lado a lado em desktop, imagem antes do texto em mobile, preservando o prato completo. Os quadros mantêm o enquadramento integral, com detalhe ampliável. A autoria não foi inferida: artist/artistId null e referências Obra 01–03 são provisórias. O utilizador foi questionado sobre o pintor; resposta ainda pendente.

Verificação: testes de renderer e sintaxe aprovados, recursos referenciados presentes; início/casa/galeria em 5 larguras sem overflow ou imagens partidas detetadas; galeria com imagens reais abre, muda de obra e fecha por Escape com restituição de foco. O backend continua por integrar. Contactos, créditos e metadados das obras permanecem pendentes.

Nota de cor: perfis Display P3 preservados nas três cópias HEIC. A releitura do volume externo deixou de responder durante a auditoria ICC dos JPG; os restantes perfis precisam de revisão antes da publicação, sobretudo para as pinturas. Não se bloqueou a preview porque as cópias e os hashes já estavam disponíveis localmente.

## Refinamento UI/UX — 15 de outubro de 2026

Responsável: Antigravity (frente Frontend assumida por instrução direta do utilizador).
Objetivo: Elevação da qualidade de apresentação, apelo gastronómico, clareza na hierarquia e melhoria substancial na taxa de conversão das reservas.

- **Cabeçalho & Marca:** Cabeçalho com fundo branco limpo e fixo (`sticky`), integrando perfeitamente a transparência do logótipo e eliminando o antigo retângulo branco isolado sobre fundo creme.
- **Hierarquia de Ações:** O botão no Hero agora tem o rótulo caloroso e específico "Reservar mesa" (ou "Reservar por WhatsApp"), resolvendo o conflito cognitivo com o botão "Reservas" do topo da página.
- **Fotografia do Prato Principal:** Aplicação de elevação, sombra suave e raio de curvatura orgânico (`border-radius: 12px; box-shadow`) à taça de cachupa, valorizando o prato e o seu apelo visual no primeiro ecrã.
- **Assistente Interativo de Reserva (WhatsApp):** Na página de reservas (`/reservas/`), foi implementado um seletor nativo em JavaScript acessível (pessoas e almoço/jantar) que atualiza automaticamente o link do WhatsApp com mensagem pronta a enviar (ex: "Olá! Gostaria de pedir uma reserva para 4 pessoas (Jantar)..."). Sem necessidade de servidor ou base de dados, mantendo fidelidade estrita à arquitetura estática.
- **Galeria & Modal:** Diálogo (`<dialog>`) modernizado com cantos arredondados, backdrop suave, botões refinados de navegação e fecho estilo museu/exposição.
- **Rodapé:** Palavra decorativa "Cachupa." suavizada para um tom de marca elegante (marca d'água arquitetural com 22% de opacidade), sem abafar os links e contactos.

Verificação:
- `npm --prefix frontend test`: 8 testes unitários aprovados.
- `npm --prefix frontend run lint`: sintaxe Python, JSON e JavaScript válida.
- `npm --prefix frontend run build:preview`: 7 páginas geradas com sucesso em `frontend/dist`.

## Remoção de imagens (por agora) — 15 de outubro de 2026

Pedido direto do utilizador: retirar todas as imagens por agora do site.

- **Ajustes:**
  - `frontend/fixtures/preview.json`: limpos os identificadores de imagens, fotografias dos pratos/espaço e lista de obras (`images: {}`, `artworks: []`, `heroImageId: null`).
  - As fotografias selecionadas e a fixture anterior foram preservadas com segurança em `frontend/fixtures/preview-with-photos.json` e `frontend/fixtures/photo-selection.json` para reintegração posterior.
  - `frontend/src/render.py`: `placeholder` desativado para não injetar ilustrações SVG provisórias no lugar das fotos.
  - O site passa a exibir uma apresentação puramente editorial/tipográfica (`.text-only`), com layout equilibrado e a galeria a indicar o estado "A exposição está a ser preparada" sem imagens de obras. Apenas o logótipo oficial permanece no cabeçalho.
- **Verificação:** 8 testes unitários aprovados, `lint` sem erros e as 7 páginas geradas sem qualquer tag `<img>` de conteúdo.

## Redesenho Visual, Fotografias de Estúdio & Nova Secção de Novidades — 19 de outubro de 2026

Responsável: Antigravity (frente de Frontend assumida por instrução do utilizador).
Pedido do utilizador: Elevação substancial do design visual, seleção cuidada de fotografias da pasta de estúdio (`CACHUPA STUDIO copy`), eliminação rigorosa de qualquer distorção/esticamento de imagens, excelente usabilidade e ergonomia, e nova secção para "Notícias, Novidades & Avisos da Casa".

- **Seleção Criteriosa de Fotografias de Estúdio (`CACHUPA STUDIO copy`):**
  - Auditoria às 84 fotografias de estúdio de alta resolução com iluminação profissional e pratos de barro em fundo escuro.
  - Selecionadas e copiadas 9 imagens em resolução otimizada para `frontend/public/assets/photos/`:
    - `studio-hero.jpg` (1600x999): Cachupa rica com camarão grelhado, chouriço e piri-piri em caçarola de barro.
    - `studio-carne.jpg` (1600x1066): Cachupa rica de carne com pimentos e chouriço.
    - `studio-frango.jpg` (1600x1066): Cachupa de frango dourado e cebola caramelizada.
    - `studio-peixe.jpg` (1320x877): Cachupa de peixe fresco e lulas com cebolada.
    - `studio-cozinheira.jpg` (1066x1600): Pintura a óleo de mulher cabo-verdiana a mexer o caldeirão de cachupa.
    - `studio-sala.jpg` (1600x1200): Sala do restaurante com paredes rústicas de pedra e mesas de madeira maciça.
    - `studio-musicos.jpg` (1600x1200): Pintura a óleo de músicos cabo-verdianos com violão.
    - `studio-quadro-mulher.jpg` (1600x1200): Pintura com figura tradicional cabo-verdiana em tons quentes.
    - `studio-borrego.jpg` (1320x1928): Chambão de borrego confitado em taça de barro.

- **Zero Distorção & Proporções Naturais:**
  - Removidas todas as regras de `aspect-ratio` fixo e forçado que provocavam esticamento visual.
  - Fotografias renderizadas com `max-width: 100%; height: auto; object-fit: cover;` respeitando as suas proporções nativas de captura (3:2, 4:3, 16:10).
  - Pinturas e obras de arte na galeria e no modal `<dialog>` protegidas estritamente com `object-fit: contain !important` e moldura de museu sem qualquer corte.

- **Ambiente Visual & Paleta Refinada:**
  - Hero com fundo escuro cinematográfico (`#12171A` a `#1E262C`), fundindo-se de forma perfeita com o fundo negro das fotografias de estúdio, valorizando as cores quentes da comida e das caçarolas de barro.
  - Corpo da página em papel quente acolhedor (`#F9F7F2` e `#F4EEE3`), azul atlântico de Cabo Verde (`#006C9A`), vermelho terracota (`#C8232B`) e âmbar dourado (`#F5B324`).
  - Faixa de identidade cabo-verdiana sutil e elegante.

- **Nova Secção: "Novidades & Avisos da Casa":**
  - Renderizador especializado para cartões editoriais (`.news-card`) com badges estilizadas (`✦ Especial`, `✦ Cultura`, `✦ Aviso`), sem imagens esticadas de fundo.

- **Ergonomia e Usabilidade:**
  - Textos em 18px–20px com alto contraste WCAG AAA para leitura sem esforço.
  - Alvos de clique de 48px–52px.
  - Barra de ação móvel fixa inferior (`.mobile-bar`) com botão direto de WhatsApp e Ligar.

- **Verificação Técnica Realizada:**
  - `npm --prefix frontend test`: 8/8 testes unitários aprovados.
  - `npm --prefix backend test`: 38/38 testes de backend aprovados.
  - `npm --prefix frontend run build:preview`: 7 páginas geradas com sucesso em `frontend/dist/`.
  - `bash scripts/test-all.sh` e `bash scripts/lint-all.sh`: 0 erros em todo o projeto.
  - Servidor de preview ativo em `http://127.0.0.1:18952`.

## Reformulação Completa da UI e Curadoria Autêntica de Fotografias — 19 de outubro de 2026

Responsável: Antigravity (frente de Frontend).
Motivação: Ajuste crítico após feedback do utilizador relativamente ao aspeto sombrio da interface anterior e à seleção de fotografias.

- **Transformação Visual Completa (da penumbra à luz e calor cabo-verdiano):**
  - **Hero Principal (`.home-hero`):** Substituído o fundo escuro/cinzento quase preto por um degradé profundo e luminoso de Azul Atlântico (`#022939` a `#004D6E` a `#006C9A`), com subtil halo dourado quente em fundo. Tipografia em branco puro e dourado suave, com botão de reserva em ouro quente (`#F5B324`) e cartão de imagem elevado com sombra volumétrica (`box-shadow: 0 28px 64px -12px rgba(0, 18, 30, 0.55)`).
  - **Fita de Identidade (`.identity-band`):** Eliminado o aspeto de fita amarela berrante. Reformulada para linho areia quente (`#F7F1E6`), texto azul atlântico profundo (`#004D6E`) e estrelas em terracota suave (`#C8232B`).
  - **Cartões de Novidades & Avisos (`.news-card`):** Removida a barra rígida superior de 5px. Desenhados como cartões brancos orgânicos com raio de 16px, sombra leve e etiquetas pill específicas por tema: `✦ Especial` (terracota/âmbar), `✦ Cultura` (azul suave), `✦ Aviso` (mostarda quente).
  - **Paredes da Sala e Galeria de Arte:** As pinturas a óleo expostas na sala têm agora molduras reais centradas, exibindo as assinaturas autênticas do mestre cabo-verdiano Lito Silva e do tocador na praia ao pôr-do-sol.
  - **Secção de Visita & Reservas (`.section-visit`):** Ambiente crepuscular azul-marinho com caixa translúcida de horários e botões diretos de contacto.

- **Nova Curadoria e Enquadramento de Fotografias (`frontend/public/assets/photos/`):**
  1. `studio-hero.jpg` (1320x865): Caldeirão de barro fumegante com Cachupa de Marisco & Camarão tigre grelhado, pimentos e coentros frescos.
  2. `studio-carne.jpg` (1320x877): Autêntica Cachupa Rica tradicional de carne com feijão pedra em prato de barro rústico sobre papel pardo.
  3. `studio-polvo.jpg` (1320x860): Cachupa rica de polvo tenro e marisco com tomate cereja em travessa de barro.
  4. `studio-refogada.jpg` (1320x874): Cachupa Refogada clássica com ovos estrelados da quinta, chouriço corado e queijo fresco de cabra.
  5. `studio-frango.jpg` (1320x867): Cachupa de frango dourado em lume lento com cebolada caramelizada.
  6. `studio-sala.jpg` (1200x1600): Sala acolhedora com paredes de pedra rústica, mesas temáticas de Cabo Verde e relógio de parede.
  7. `studio-pintura-cachupa.jpg` (1320x872): Pintura a óleo emoldurada em madeira da mãe cabo-verdiana ao lume de chão, assinada por Lito Silva (sem garrafas ou obstáculos à frente).
  8. `studio-pintura-mar.jpg` (930x870): Pintura a óleo com moldura dourada do músico solitário com violão na praia de Cabo Verde ao entardecer.
  9. `studio-pintura-festa.jpg` (950x720): Pintura a óleo de pares a dançar funaná tradicional, assinada por Lito Silva, enquadrada perfeitamente na moldura.

- **Verificação Técnica Realizada:**
  - `npm --prefix frontend test`: 8/8 testes aprovados.
  - `npm --prefix backend test`: 38/38 testes aprovados.
  - `bash scripts/test-all.sh` e `bash scripts/lint-all.sh`: 0 erros.
  - `npm --prefix frontend run build:preview`: 7 páginas geradas com sucesso.
  - Servidor local ativo em `http://127.0.0.1:18952`.

## Redesenho Editorial Puro & Minimalista (Inspiração Blanquette & Palais d'Or) — 26 de outubro de 2026

Responsável: Antigravity (frente de Frontend, a pedido direto do utilizador).
Referências analisadas: `inspirações /Blanquette - Restaurant WordPress Theme.jpg`, `inspirações /Luxury Elegant Restaurant Webflow website template.jpg` (`Palais d'Or`) e manual da marca `Identidade Visual copy/visao-geral.png` (`direcao-criativa.md`).

- **Eliminação Total de "AI Slop" e Ornamentos Artificiais:**
  - Removidos todos os símbolos `✦`, emojis (`💬`, `📞`), etiquetas flutuantes sobre fotografias, molduras duplas deslocadas, gradientes radiais, sombras pesadas e cantos arredondados estilo SaaS (`border-radius: 0` em toda a grelha).
  - Removida a fita intermédia repetitiva (`.identity-band`) para permitir transição direta e limpa entre o Hero escuro e o espaço em branco editorial.
  - **Superfícies Planas & Espaço Vazio Generoso:** Contraste rigoroso entre o ardósia noturno plano (`#0B1D24`), o branco puro de galeria (`#FFFFFF`) e o papel quente oficial da marca (`#F5F1E8`), com secções de `132px` de respiro vertical.
  - **Hero & Barra de Reserva *Blanquette*:** Grelha assimétrica `5fr 7fr` onde a fotografia domina sem molduras nem legendas acopladas, acompanhada pela barra horizontal plana de reserva rápida na base do Hero (`Reservar mesa` com seletores retangulares sóbrios).
  - **Secção Agenda / Notas (`#noticias`):** Desenhada como índice editorial de 3 colunas separadas apenas por filetes verticais finos (`1px solid`), sem cartões em caixa nem pills coloridas.
  - **Galeria de Arte:** As obras de Lito Silva repousam sobre *passe-partout* plano em papel (`#F5F1E8`) com legenda tipográfica alinhada à esquerda sobre fundo branco, sem caixas nem sombras ao redor do cartão.
  - **Modal Light-Dismiss (`<dialog closedby="any">`) & Prioridade LCP:** `fetchpriority="high"` exclusivo na imagem principal do Hero e `fetchpriority="low"` na imagem oculta do modal `<dialog>`.

- **Verificação Técnica Realizada:**
  - `npm --prefix frontend test` → 8/8 testes aprovados.
  - `npm --prefix backend test` → 38/38 testes aprovados.
  - `bash scripts/test-all.sh` e `bash scripts/lint-all.sh` → 0 erros.
  - `npm --prefix frontend run build:preview` → 7 páginas atualizadas em `frontend/dist` e servidas em `http://127.0.0.1:18952`.


## Fusão Fiel com o Manual de Identidade Visual "Mesa Viva" (12 Páginas) — 26 de outubro de 2026

Responsável: Antigravity (frente de Frontend, por instrução direta do utilizador).
Referências aplicadas: Manual de Identidade Visual completo (`Identidade Visual copy/Cachupa-Rst_Manual-de-Identidade.pdf`, páginas 01/12 a 12/12) + estrutura limpa e funcional de reserva.

- **Direção Visual — Tradicional, Limpa e Profissional (Sem Falso "Luxo"):**
  - **Paleta Estrita do Manual (Página 04/12):** Substituídos os tons pretos/dourados de "fine dining" pelas 6 cores oficiais da marca: Azul `#006C9A`, Vermelho `#DD1A2A`, Amarelo `#FFED00`, Branco `#FFFFFF`, Papel `#F5F1E8` e Tinta `#12323C` (*"Branco e azul dominam. Vermelho conduz as ações. Amarelo aparece em estrelas, etiquetas e títulos sobre azul."*).
  - **Cabeçalho Oficial (Páginas 02/12 e 12/12):** Fundo branco puro (`#FFFFFF`), logo completa com `180px` de largura mínima, links de navegação em `Work Sans` (`16px`, cor `#006C9A`) e botão retangular vermelho `#DD1A2A` (`Reservas`).
  - **Hero em Papel `#F5F1E8` + "Letra de Letreiro" Bicolor (Páginas 05/12 e 12/12):** Título principal dividido em duas linhas e duas cores (`CABO VERDE,` em `#006C9A` e `À MESA.` em `#DD1A2A`), assinatura manuscrita `"Sente-se."` em `Nothing You Could Do`, botão principal em `#DD1A2A` e fotografia enquadrada sobre bloco `#006C9A`.
  - **Barra Horizontal de Reserva Rápida:** Integrada na base do Hero sobre fundo `#006C9A`, com título `RESERVAR MESA` em `#FFED00`, seletores limpos em fundo branco e botão de ação em `#DD1A2A`.
  - **Hierarquia Tipográfica e Numeração `01 / 02 / 03` (Páginas 02/12, 07/12 e 09/12):** Subtítulos e números de secção (`01`, `02`, `03`) em `Big Shoulders Bold` vermelho (`#DD1A2A`), títulos de secção e de pratos em `Big Shoulders Bold` azul (`#006C9A`) e divisórias vermelhas/azuis de traço limpo.
  - **Cartazes Azuis (`#house`, `#visit` e `.footer` — Páginas 01/12, 07/12 e 08/12):** Blocos em `#006C9A` com títulos em amarelo `#FFED00` (incluindo `"VOLTE COM FOME."` no rodapé), assinatura `"Sente-se. Há lugar à mesa."` em branco e o motivo isolado da panela (`grafismo-panela.svg`) em linha branca.


## 2026-10-26 — Correção Visual Profunda, Orientação EXIF e Refinamento Editorial Clean

- **Estado:** concluído
- **Âmbito:** `frontend/public/assets/photos/studio-*.jpg`, `frontend/src/render.py`, `frontend/src/styles/site.css`, `docs/handoffs/frontend.md`
- **Resumo:**
  - **Correção de fotografias rodadas a 90° (EXIF Orientation = 6):** Identificado por inspeção visual em Chrome headless que `studio-sala.jpg`, `studio-pintura-festa.jpg`, `studio-pintura-mar.jpg`, `studio-musicos.jpg` e `studio-quadro-mulher.jpg` já tinham os píxeis na vertical mas mantinham a tag EXIF `Orientation = 6`, fazendo o browser rodá-las 90° de lado. Reposta a tag EXIF `Orientation = 1` sem perda de qualidade.
  - **Correção de títulos truncados e grelhas esmagadas (`frontend/src/render.py` e `frontend/src/styles/site.css`):** Corrigida a truncagem a 4 palavras em `flavor_cards()` (`01 Cachupa de Polvo e Marisco`, `02 Cachupa Refogada com Ovos`), eliminadas legendas duplicadas (`show_caption=False` em cartões com corpo próprio) e corrigido `.section-news .section-layout` para `display: block` (evitando que a grelha de 3 colunas ficasse comprimida em 50% da largura).
  - **Direção de Arte Editorial Limpa (`Mesa Viva` + inspiração `Blanquette`):** Removidas as molduras pesadas de `16px` azul e linhas grossas; aplicados filetes de `1px solid`, superfícies dominantes em Branco (`#FFFFFF`) e Papel (`#F5F1E8`), grelhas com `minmax(0, 1fr)` sem overflow horizontal em mobile e contraste equilibrado no bloco `#visit` (`#006C9A` + `#FFED00`) e rodapé (`#12323C`).
- **Validação executada:**
  - `npm --prefix frontend run build:preview` (7 páginas geradas em `frontend/dist`)
  - Verificação visual completa por capturas de ecrã reais em Google Chrome Headless (`1440px` desktop e `500px` mobile)
  - `bash scripts/test-all.sh` (8 testes frontend + 38 testes backend: OK)
  - `bash scripts/lint-all.sh` (0 erros)


## 2026-10-27 — Redesign Impecável da Hero: Cápsula da Marca, Tipografia Harmoniosa, Menu Hamburger Fluido e Barra de Reserva Flutuante

- **Estado:** concluído
- **Âmbito:** `frontend/src/templates/base.html`, `frontend/src/render.py`, `frontend/src/styles/site.css`, `frontend/src/scripts/site.js`, `docs/handoffs/frontend.md`
- **Diagnóstico da versão anterior (o que motivou a rejeição):**
  - O título gigante comprimido em fonte poster `Big Shoulders` estava estampado diretamente por cima das cabeças das figuras na pintura a óleo de Lito Silva.
  - Havia 7 linhas e notas dispersas em conflito visual na mesma hero (kicker, título, subtítulo, slogan, rodapé da obra, seta e frase manuscrita).
  - A barra de reserva anterior apresentava um aspeto tabular cru e rígido com um botão vermelho sobredimensionado.
  - O logótipo transparente estava a colidir e a ser cortado pela barra de pré-visualização no topo.
- **Soluções implementadas com rigor sénior (aplicando `ui-ux-design-master` e inspirações `Lou's` & `Ma Joie`):**
  1. **Cápsula de Marca Protetora (`.brand-capsule`):** O logótipo oficial completo a cores repousa dentro de uma cápsula branca arredondada flutuante com sombra suave, respeitando rigorosamente o manual de identidade visual (*«Área de proteção mínima de 10%; não colocar a logo diretamente sobre uma fotografia movimentada»*), conferindo um aspeto tátil e arquitectónico de selo gastronómico artesanal.
  2. **Harmonização Visual da Fotografia & Tipografia Central:**
     - A vinheta de iluminação suave (`.hero-scrim`) e o grão analógico 35mm (`.hero-grain` com SVG `feTurbulence`) preservam a textura da parede, destacam o violão na esquerda e o quadro na direita como num ambiente de exposição acolhedor.
     - Removida toda a sobrecarga de notas e cursivas na hero. Apenas o essencial e refinado: `RESTAURANTE` em caixa alta espaçada a ouro suave (`letter-spacing: 0.32em`), `Cachupa` em `Work Sans` limpo e imponente, e o slogan discreto por baixo.
  3. **Barra de Reserva Flutuante Ultra Clean (`.booking-bar-card`):**
     - Em vez de uma barra em tabela que quebrava o ritmo da página, a barra surge como uma cápsula branca flutuante centrada (`border-radius: 9999px` em desktop / `20px` em mobile) com sombra difusa elegante, separadores subtis de 1px e botão `Pedir reserva →` refinado com transição de seta em hover.
  4. **Menu Hamburger Minimalista e Cortina Editorial:**
     - Botão `MENU =` em vidro fosco translúcido (`backdrop-filter`) que transiciona fluidamente para `✕` ao abrir.
     - Cortina de navegação de ecrã inteiro com desfoque profundo (`blur(28px)`), fecho rápido com botão `✕ FECHAR`, tecla `Escape` e clique exterior, links numerados (`01` a `04`) e bloco informativo com horário e tradição da casa.
  5. **Resolução de Conflitos e Responsividade:**
     - O cabeçalho usa margem negativa em vez de `position: absolute` rígido, garantindo que nunca colide com a barra de pré-visualização tanto em desktop como em mobile (`390px`).
- **Validação:**
  - `npm --prefix frontend run build:preview`: 7 páginas geradas com sucesso.
  - `bash scripts/test-all.sh`: 8 testes frontend + 38 testes backend aprovados (100%).
  - `bash scripts/lint-all.sh`: sintaxe Python, JSON e JavaScript válida.
  - Verificação visual real por capturas de ecrã em Google Chrome Headless com emulação de dispositivo móvel (`scratch/true-mobile.png`, `scratch/hero-v8-desktop.png`, `scratch/menu-desktop-open.png` e `scratch/menu-mobile-open.png`).

## Refinamento UI/UX — continuação

- **Renderer e templates:** a home usa o heading e a introdução do modelo, apresenta a fotografia sem texto por cima e dá prioridade ao percurso principal com ações distintas. Desktop tem navegação visível; mobile mantém menu acionável, com foco devolvido ao botão ao fechar.
- **Reservas e informação:** removidos seletores fictícios de pessoas/refeição/dia e respetivo JavaScript. As ações indicam WhatsApp ou email apenas quando o respetivo URL válido existe; sem contactos, a página explica a indisponibilidade, não sugere envio e não afirma confirmação. Mensagens de navegação sem suporte sobre cidade, artista e horário fixo foram removidas.
- **Qualidade visual:** mantidos o logótipo, as fontes e as cores oficiais. A fotografia lidera o primeiro ecrã; título, copy e ações ficam numa faixa editorial em papel, evitando sobrepor pessoas e obras.
- **Ficheiros alterados:** `frontend/src/render.py`, `frontend/src/templates/base.html`, `frontend/src/styles/site.css`, `frontend/src/scripts/site.js`, `frontend/tests/test_render.py`, `frontend/README.md`.
- **Validação executada:** `npm --prefix frontend test` (10/10); `npm --prefix frontend run lint`; `npm --prefix frontend run build:preview`. No navegador, 7 rotas × 5 larguras (320, 390, 768, 1024, 1440 px): zero overflow horizontal e exatamente um `h1` por rota; fotografia do hero carregada; menu móvel abre, fecha com Escape e devolve o foco.
- **Pendências:** preview continua identificada como tal; contactos, horários e créditos reais permanecem por confirmar. Não houve alteração ao contrato nem ao backend. A interação de reservas não foi enviada nem testada com um contacto real.

## Refinamento de acessibilidade e estados — 28 de outubro de 2026

- **Navegação:** o menu móvel é um diálogo acessível com foco inicial, ciclo de Tab, fecho por Escape e devolução de foco. Quando o JavaScript não carrega, os links de navegação permanecem visíveis no mobile.
- **Controlos e movimento:** alvos móveis do menu e da barra fixa, controlos de cópia e botões da galeria têm no mínimo 44 px; a galeria usa o estado nativo `disabled`; movimento reduzido e foco visível foram tratados. A barra fixa permanece abaixo do conteúdo.
- **Contactos:** removidas mensagens que sugeriam disponibilidade futura. Morada, contactos e horários em falta são indicados sem duplicação; o rodapé não descreve informação ausente como existente. Valores de contacto confirmados continuam visíveis mesmo que o URL recebido seja inválido, sem criar um link inseguro.
- **Desempenho:** o hero mantém prioridade alta; imagens restantes usam carregamento diferido e descodificação assíncrona.
- **Ficheiros alterados:** `frontend/src/render.py`, `frontend/src/templates/base.html`, `frontend/src/styles/site.css`, `frontend/src/scripts/site.js`, `frontend/tests/test_render.py`, `frontend/README.md`.
- **Validação:** `npm --prefix frontend test` (12/12); `npm --prefix frontend run lint`; `npm --prefix frontend run build:preview`; `git diff --check` dos ficheiros frontend. No browser: 7 rotas × 5 larguras (320, 390, 768, 1024, 1440 px), sem overflow e com um único `h1`; menu com foco contido/devolvido; fallback mobile sem JavaScript; diálogo da galeria com limites nativos de navegação.
- **Preview local:** `http://127.0.0.1:18953/` respondeu com HTTP 200 após a última geração. O servidor anterior na porta 18952 não foi alterado.
- **Pendências:** contactos, horários e créditos reais continuam por confirmar; este trabalho não aprova a publicação nem altera o contrato ou o backend.

## Refinamento da navegação — 28 de outubro de 2026

- **Problema corrigido:** o cabeçalho anterior sobrepunha-se à fotografia, tinha identidade de botão em formato de cápsula, e o menu aberto repetia informação num painel lateral. A hierarquia da marca, destinos e reservas não era clara.
- **Cabeçalho desktop/mobile:** uma faixa em papel, com logo sem cápsula decorativa, destinos alinhados e ação de reservas diferenciada. O cabeçalho não fica sobreposto ao hero. Em mobile, o controlo do menu tem rótulo claro, forma retangular e alto contraste.
- **Menu mobile:** painel limpo em papel com logo, botão de fecho, destinos em linhas de leitura e um único CTA interno “Ver reservas”. Removido o bloco lateral redundante. Corrigida a ordem de camadas para o painel ficar acima da faixa de preview.
- **Acessibilidade preservada:** diálogo modal rotulado; foco inicial, ciclo de Tab, Escape e retorno do foco; alternativa de links visível sem JavaScript. Alvos de toque respeitam 44 px.
- **Ficheiros alterados:** `frontend/src/templates/base.html`, `frontend/src/render.py`, `frontend/src/styles/site.css`, `frontend/tests/test_render.py`.
- **Validação:** `npm --prefix frontend test` (13/13), `npm --prefix frontend run lint`, `npm --prefix frontend run build:preview`. Browser: sete rotas em oito larguras (320, 375, 390, 768, 900, 901, 1024, 1440 px), sem overflow nem `h1` duplicado; teste de foco em ambos os limites, fecho e retorno ao botão; fallback mobile com JavaScript bloqueado.
- **Pendências:** contactos reais permanecem por confirmar. A alteração mantém o contrato e os restantes conteúdos do site.

## Ajuste da hierarquia desktop — 28 de outubro de 2026

- **Problema corrigido:** no viewport largo, o grupo de navegação estava encostado à direita, com a marca demasiado pequena e ação pouco legível. O resultado deixava um vazio excessivo entre logo e links.
- **Alteração:** cabeçalho em grelha de três zonas — marca alinhada à esquerda, destinos centrados no viewport de conteúdo e ação vermelha “Reservar” à direita. Logo com 60 px, links com corpo de 15 px, ação com alvo de 48 px e estado ativo visível por sublinhado. No mobile, o botão do menu fica alinhado à direita, separado da marca.
- **Ficheiros alterados:** `frontend/src/styles/site.css`, `frontend/src/render.py`, `frontend/tests/test_render.py`, `frontend/README.md`.
- **Validação:** `npm --prefix frontend test` (13/13), `npm --prefix frontend run lint` e `npm --prefix frontend run build:preview` aprovados. No browser, a home foi verificada em 320, 390, 768, 900, 901, 1024, 1440 e 1920 px, sem overflow; em desktop, navegação centrada, sem colisão com a ação, e um único `h1`. A captura desktop confirmou a hierarquia visual após o build. `git diff --check` global sinalizou apenas um espaço em branco preexistente em `documentation/archive/controlo_do_projeto/controlo.md`, fora desta alteração.

## Reestruturação integral de arquitetura e UI editorial — 31 de outubro de 2026

- **Motivação e causa-raiz corrigida:** a folha de estilos `frontend/src/styles/site.css` encontrava-se dessincronizada do HTML emitido por `frontend/src/render.py` (36 classes sem regras CSS ativas, provocando colapso estrutural em `/contactos/`, `/reservas/`, `/privacidade/`, `#noticias`, `#visit`, `#art` comprimida a 50%, logótipo cortado em mobile e `#site-nav` preso dentro do contexto de empilhamento de `<header>`).
- **Sistema visual e arquitetónico implementado (inspirado em `inspirações /` — *Blanquette*, *Palais d'Or*, *Morrison* e *Le Poivrier* — fundido com a identidade oficial *Mesa Viva*):**
  - **Cabeçalho e menu modal mobile (`frontend/src/templates/base.html`):** logótipo transparente `logo-clean.svg` em grelha de 3 zonas em desktop (flex limpo em mobile), CTA retangular `Reservar`, e `#site-nav.nav-overlay` movido para fora de `<header>` (`z-index: 220`, acima da barra móvel fixa) sobre fundo azul noturno (`#0d222b`) com `logo-white.svg` otimizado (removidos 675 KB de `@font-face` base64 não utilizados).
  - **Hero da Home e cabeçalhos das subpáginas (`frontend/src/render.py`):** palco escuro assimétrico `5fr 7fr` com moldura fina de `1px` sobre `hero-parede-quadro.jpg`, filete vermelho de `52px`, CTAs primário e fantasma, e barra arquitetónica inferior de 3 colunas (`.hero-ledger`) com texto factual alinhado ao contrato v1. Nas subpáginas, trilho de navegação real (`Início / <Página>`) sobre superfície `--paper` (`#f5f1e8`).
  - **Ritmo de secções, galeria e visita (`frontend/src/render.py`, `frontend/src/styles/site.css`):** alternância entre branco de galeria (`#ffffff`), papel (`#f5f1e8`) e azul arquitetónico profundo (`#0f2933` em `#house` com assinatura `Nothing You Could Do`; `#0d3345` em `#visit` com `grafismo-panela.svg` em linha branca e cartão tabular de horários). Índice editorial `.news-grid` em 3 colunas com filetes verticais de `1px`; galeria `.art-grid` a 100% da largura com *passe-partout* em papel (`object-fit: contain`), hierarquia de títulos sem salto (`<h2 class="sr-only">` quando `artist` é `null`) e modal `<dialog id="art-dialog" closedby="any">` dimensionado para exibir pintura, legenda e paginação sem corte.
  - **Interações e transições (`frontend/src/scripts/site.js`, `frontend/src/styles/site.css`):** separação entre estado de saída `[data-closing]` e `[hidden]` (`display: none`) para suportar fallback de animação discreta, ciclo de foco e `Escape` no menu móvel, *light-dismiss* com fallback de coordenadas para `<dialog>`, feedback visual no botão `Copiar email`, e omissão de auto-links redundantes na `.mobile-bar`.
- **Ficheiros alterados:** `frontend/public/assets/brand/logo-white.svg`, `frontend/src/templates/base.html`, `frontend/src/render.py`, `frontend/src/scripts/site.js`, `frontend/src/styles/site.css`, `docs/handoffs/frontend.md`.
- **Validação executada:**
  - `npm --prefix frontend run build:preview` (7 páginas geradas em `frontend/dist`, servidas em `http://127.0.0.1:3000/`).
  - `bash scripts/test-all.sh` (13/13 testes frontend + 38/38 testes backend aprovados) e `bash scripts/lint-all.sh` (0 erros).
  - Auditoria determinística (`impeccable detect`): 0 alertas de contraste (`low-contrast`), tipografia (`wide-tracking`), imagens (`broken-image`) ou hierarquia (`skipped-heading`).
  - Browser real via CDP (`http://127.0.0.1:3000/`): 35 combinações rota × largura (7 rotas × `320`, `390`, `768`, `1024`, `1440` px) com zero erros de consola, zero overflow horizontal e zero imagens partidas; inspeção visual completa em desktop e mobile (incluindo menu modal aberto e `<dialog>` da galeria).
- **Pendências:** contactos, horários e créditos reais permanecem por confirmar antes da publicação; contrato v1 e backend inalterados.

## Integração das 11 Pinturas do Restaurante e Destaques da Home — 31 de outubro de 2026

- **Pedido do utilizador:** incorporar as 11 fotografias de pinturas a óleo reais da sala (`CACHUPA STUDIO copy/IMG_7670.JPG` a `IMG_7688.JPG`) na galeria, retirando as obras temporárias anteriores, atribuindo títulos e descrições contextuais a cada uma com base no seu conteúdo artístico, e renovando a seleção em destaque na página inicial (`Início`).
- **Obras integradas em `frontend/public/assets/photos/` e `frontend/fixtures/preview.json`:**
  1. `arte-caldeirao.jpg` — **O Caldeirão da Mãe**: preparação da cachupa ao lume de chão servida pela mãe às crianças (*Destaque Home 1*).
  2. `arte-serenata.jpg` — **Serenata à Luz da Lamparina**: reunião comunitária e familiar em torno da mesa ao som da rabeca (*Destaque Home 2*).
  3. `arte-pescador.jpg` — **O Regresso do Pescador**: pescador vigoroso com vara e chapéu de palha junto ao mar e montanhas (*Destaque Home 3*).
  4. `arte-tres-gracas.jpg` — **As Três Graças da Terra**: tríptico com três figuras femininas em tons de barro e vestes vermelhas.
  5. `arte-caminho-entardecer.jpg` — **Caminho ao Entardecer**: mãe de vestido amarelo e cesto à cabeça de mãos dadas com filho.
  6. `arte-capoeira.jpg` — **Roda e Movimento**: capoeiristas de branco em acrobacia no ar sobre fundo carmesim.
  7. `arte-danca-batuque.jpg` — **Ritmo de Batuku**: dançarina de saia amarela rodada ao compasso de tocador de tambor tradicional.
  8. `arte-jazz-sopros.jpg` — **Sopros da Noite**: músicos expressionistas com trompete e saxofones dourados.
  9. `arte-alegria-ilhas.jpg` — **Festa na Areia**: grupo em trajes brancos e azuis em celebração dançante na praia.
  10. `arte-vale-santo-antao.jpg` — **Manhã no Vale Verdejante**: paisagem montanhosa rural com casario branco e carroça de burro.
  11. `arte-maos-ralador.jpg` — **Mãos de Labuta (O Ralador)**: grande plano de mãos a raspar a raiz num ralador artesanal de folha-de-flandres.
- **Ajuste visual no CSS (`frontend/src/styles/site.css`):**
  - Ajuste fino do enquadramento `.media-art img` para `object-position: center 44%` (alinhado com o baricentro ótico dos quadros nos ficheiros fotográficos), garantindo que tanto a pintura como a moldura se exibem completas e sem cortes indesejados.
- **Validação executada:**
  - `npm --prefix frontend run build:preview`: 7 páginas atualizadas em `frontend/dist/`.
  - `bash scripts/test-all.sh` (13/13 frontend + 38/38 backend aprovados) e `bash scripts/lint-all.sh` (0 erros).
  - Inspeção no browser real via CDP a 1440 px e 390 px para `/` (secção `#art`) e `/galeria/` (todas as 4 filas e modal de ampliação funcional `1 de 11`). Servidor ativo em `http://127.0.0.1:3000/`.

## Integração de Dados Reais do Restaurante (Localização, Horários e Contactos) — 31 de outubro de 2026

- **Dados confirmados pelo utilizador via ficha oficial:**
  - **Endereço:** `R. Alm. Reis 22 B, 2830-326 Barreiro`
  - **Cidade:** `Barreiro`
  - **Telefone:** `963 572 411` (`tel:+351963572411`)
  - **Horário de funcionamento:** Segunda a Domingo (7 dias por semana), das `11:00` às `23:00`
  - **Serviços / Características:** Esplanada, Opções veganas e Noites de música ao vivo.
  - **Como chegar:** ligação direta para localização no Google Maps.
- **Implementação efetuada:**
  - Atualizado [`frontend/fixtures/preview.json`](file:///Users/aydangoncalves/Desktop/Restaurante%20Cachupa/Site/frontend/fixtures/preview.json) com todos os campos de `restaurant` preenchidos de acordo com o contrato v1.
  - Corrigidas as referências de localização de "em Lisboa" para "no Barreiro" nas secções `house` e `story`, e integrada a menção aos serviços na secção `visit`.
  - Atualizado [`frontend/src/render.py`](file:///Users/aydangoncalves/Desktop/Restaurante%20Cachupa/Site/frontend/src/render.py) para incluir o telefone no rodapé institucional e simplificar a secção `#visit` na Home, retirando a tabela semanal extensa (que agora vive exclusivamente na página dedicada `/contactos/`), mantendo o enquadramento equilibrado da fotografia e ligação a "Contactos e localização".
  - Corrigido o contraste da tabela de horários em [`frontend/src/styles/site.css`](file:///Users/aydangoncalves/Desktop/Restaurante%20Cachupa/Site/frontend/src/styles/site.css).
  - Adicionado teste específico `test_confirmed_contacts_address_and_hours` em [`frontend/tests/test_render.py`](file:///Users/aydangoncalves/Desktop/Restaurante%20Cachupa/Site/frontend/tests/test_render.py) (14/14 testes aprovados).
  - Reconstruído o preview (`npm --prefix frontend run build:preview`).
- **Validação:**
  - `bash scripts/test-all.sh` (14/14 frontend + 38/38 backend aprovados).
  - `bash scripts/lint-all.sh` (0 erros).
  - Verificação visual via browser CDP em `/` e `/contactos/` (desktop e mobile).
- **Próximos dados necessários para publicação final (Gemini / Produção):**
  - Confirmação do canal oficial de reservas (se o número `963 572 411` atende WhatsApp para reservas e email de contacto institucional).

## Restruturação Completa e Explícita do Rodapé & Página de Privacidade e Termos — 02 de novembro de 2026

- **Pedido do utilizador:**
  - Esclarecer o estado de privacidade, termos e condições, livro de reclamações e acessibilidade.
  - "Quero que no footer esteja tudo bem explícito".
- **Alterações de Frontend Implementadas:**
  1. **Rodapé Arquitetónico (`frontend/src/templates/base.html` & `frontend/src/styles/site.css`):**
     - Estrutura de 4 colunas em grelha responsiva no topo (`.footer-top`):
       - **Identidade & Conceito:** Logótipo branco, headline `VOLTE COM FOME.`, subtítulo `Cachupa Rst · Cozinha cabo-verdiana`, assinatura caligráfica `Sente-se. Há lugar à mesa.` e parágrafo contextual sobre a casa de acolhimento autêntico no Barreiro, cachupa de lume brando e galeria viva de pintura original.
       - **Navegação Direta:** Links acessíveis (`min-height: 44px`) para `Início`, `A nossa casa`, `Galeria`, `Reservas` e `Contactos`.
       - **Horário & Serviços:** Destaque para `Segunda a Domingo (Todos os dias)` com horário `11:00 às 23:00` em destaque tipográfico, mais lista com marcadores: `✦ Cozinha em serviço contínuo`, `✦ Esplanada & sala acolhedora`, `✦ Opções vegetarianas & veganas`, `✦ Noites com música ao vivo`.
       - **Onde Estamos & Contactos:** Morada completa (`R. Alm. Reis 22 B, 2830-326 Barreiro`), telefone direto (`963 572 411`), atalho externo `Como chegar no Google Maps ↗` e ligação direta `Pedir reserva de mesa →`.
     - **Barra Intermédia de Conformidade Legal & Transparência (`.footer-legal-bar`):**
       - Links diretos com âncoras para:
         - `Privacidade & RGPD` (`/privacidade/#dados`)
         - `Ausência de Cookies` (`/privacidade/#cookies`)
         - `Termos & Reservas` (`/privacidade/#termos`)
         - `Livro de Reclamações ↗` (`https://www.livroreclamacoes.pt`, abre em nova janela com `rel="noopener noreferrer"`, conforme DL 74/2017)
         - `Resolução de Litígios (RAL)` (`/privacidade/#litigios` — CNIACC)
         - `Acessibilidade (WCAG 2.1 AA)` (`/privacidade/#acessibilidade`)
       - Selo de Transparência Digital em pill dedicada:
         - `🔒 Transparência Digital: Sem cookies de rastreio ou perfilamento · Tipografia e ícones 100% locais · Dados salvaguardados pelo RGPD.`
     - **Rodapé Inferior (`.footer-bottom`):**
       - Menção de Direitos de Autor e Artística: `© 2026 Cachupa Rst · Cozinha tradicional de Cabo Verde. Todos os direitos reservados. Obras de arte originais em exposição da autoria de Lito Silva. Barreiro · Margem Sul · Portugal.`
  2. **Página de Privacidade (`/privacidade/` em `frontend/fixtures/preview.json`):**
     - Substituição do texto provisório mínimo por 5 secções completas e detalhadas, rigorosamente em conformidade com o validador de backend:
       - Secção 1 (`#dados`): Proteção de Dados Pessoais (RGPD) — minimização de dados, finalidade exclusiva de gestão de reservas, ausência de cedência a terceiros e direitos dos titulares (acesso, retificação, esquecimento).
       - Secção 2 (`#cookies`): Ausência Total de Cookies de Rastreio & Fontes Locais — arquitetura *privacy by design*, fontes locais sem contacto com CDNs externos (sem fuga de IP), dispensa de banners intrusivos de consentimento.
       - Secção 3 (`#termos`): Termos de Utilização & Política de Reservas — confirmação expressa pela equipa, política de tolerância de 15 minutos em atrasos, direitos de propriedade intelectual da marca e proteção das obras de arte de Lito Silva.
       - Secção 4 (`#litigios`): Livro de Reclamações & Resolução Alternativa de Litígios (RAL) — indicação do Livro de Reclamações Eletrónico e do CNIACC para a Península de Setúbal / AML.
       - Secção 5 (`#acessibilidade`): Declaração de Acessibilidade Digital (WCAG 2.1 nível AA) — estrutura semântica, contrastes elevados, navegação total por teclado (`:focus-visible`), alvos tácteis móveis superiores a 44x44 px e canal direto de assistência.
     - Associação formal do artista `Lito Silva` (`id: lito-silva`, `name: Lito Silva`, biografia) na fixture, regularizando a validação de todas as 11 obras em `artworks[].artistId`.
  3. **Suporte a Links Externos no Renderer (`frontend/src/render.py`):**
     - Atualizada a função `link()` para adicionar automaticamente `target="_blank" rel="noopener noreferrer"` a URLs externos `https://`, preservando rotas internas e números de telefone/email.
  4. **Ligação Direta ao Google Maps (Restaurante Cachupa Brr):**
     - Atualizado o URL oficial em `directionsHref` (`frontend/fixtures/preview.json`), no template (`frontend/src/templates/base.html`), na barra rápida móvel e no painel de contactos (`frontend/src/render.py`) para apontar diretamente à ficha oficial de negócio no Google Maps: `https://www.google.com/maps/search/?api=1&query=Restaurante+Cachupa+Brr`.
     - Rótulo no rodapé atualizado explicitamente para `Restaurante Cachupa Brr no Google Maps →`.
     - Teste unitário `test_confirmed_contacts_address_and_hours` atualizado para validar a presença do link direto exato.
  5. **Remoção Total de Emojis e Símbolos Visuais:**
     - Removido o emoji `🔒` do selo de transparência digital e o símbolo de estrela `✦` das listas de serviços.
     - Substituídos por marcadores tipográficos em traço sóbrio (`—`) via CSS e setas tipográficas uniformes (`→`).
     - Varredura determinística confirma zero caracteres de emoji em todos os ficheiros HTML gerados.

## Redesenho da Hero: Full Viewport & Assinatura Caligráfica — 02 de novembro de 2026

- **Pedido do utilizador:**
  - Retirar todo o texto e botões da Hero inicial (*"Cabo Verde, à mesa."*, slogan e botões *"Ver reservas"* e *"Conhecer a casa"*).
  - Deixar escrito apenas **Restaurante Cachupa** na tipografia caligráfica manuscrita da casa (*Hand / Caveat*), alinhado à esquerda e centrado verticalmente, com *Restaurante* em cima e *Cachupa* em baixo.
  - Imagem de fundo a preencher a tela inteira (*full viewport*): ao entrar no site, antes de dar scroll, o visitante visualiza exclusivamente a Navbar e a Hero fotográfica imersiva.
- **Implementação efetuada:**
  - `frontend/src/render.py`: atualizada a renderização da Home para emitir `page-hero home-hero home-hero-fullscreen` contendo o `<h1>` com a marca manuscrita em duas linhas (`hero-script-top` e `hero-script-bottom`).
  - `frontend/fixtures/preview.json`: atualizado o título e cabeçalho da Home para *"Restaurante Cachupa"*.
  - `frontend/src/styles/site.css` (e `assets/site.css`):
    - `.home-hero`: dimensionada para preencher a janela completa sem scroll (`height: calc(100dvh - 84px); min-height: 520px; display: flex; align-items: center; justify-content: flex-start;`).
    - `@media (max-width: 900px)`: adaptada para `calc(100dvh - 72px)`.
    - Tipografia manuscrita escalada com `clamp()`: *Restaurante* em branco suave levemente rotacionado (-1.5°), *Cachupa* em amarelo âmbar com sombra volumétrica suave sobre a pintura.
  - `frontend/tests/test_render.py`: atualizado o teste `test_home_uses_confirmed_copy_and_clear_navigation` para validar a presença da nova assinatura de marca e a ausência dos elementos removidos.
- **Validação e Testes:**
  - `bash scripts/test-all.sh`: 14 testes frontend + 38 testes backend aprovados (100%).
  - `bash scripts/lint-all.sh`: 0 erros de sintaxe (Python, JSON, JavaScript).
  - `npm --prefix frontend run build:preview`: 7 páginas geradas com sucesso.
  - Verificação visual via browser Chrome CDP em desktop (1280 px) e mobile (375 px) confirmando alinhamento, hierarquia, legibilidade, contrastes e ausência de sobreposição.
  - Servidor preview ativo e funcional em `http://localhost:3000/`.

## Ajuste Visual da Hero: Remoção de Opacidade, Enquadramento Natural e Escala Tipográfica — 02 de novembro de 2026

- **Pedido do utilizador:**
  - Remover a opacidade/escurecimento da imagem (*"tira a opcidade da imagem"*).
  - Deixar o tamanho real da imagem o mais próximo possível das proporções naturais na hero (*"deixa o tamnho real mais proximo que da para o tamanho da hero"*).
  - Colocar as duas palavras com o mesmo tamanho (*"mete as duas palavras do mesmo tamanho"*).
- **Implementação efetuada:**
  - `frontend/src/styles/site.css` (e `assets/site.css`):
    - `.home-hero-scrim`: ocultado (`display: none;`), eliminando o gradiente escurecedor que tornava a parede castanha escura e sem vida. A fotografia original (`hero-parede-quadro.jpg`) passa a ser exibida com 100% de luminosidade, calor e nitidez naturais.
    - `.home-hero-backdrop img`: reposicionado com `object-position: center center` no desktop (e `20% center !important` no mobile), permitindo que o violão pendurado na parede à esquerda e a moldura do quadro a óleo fiquem totalmente visíveis e enquadrados sem cortes excessivos.
    - `.hero-script-top, .hero-script-bottom`: unificadas com a mesma dimensão tipográfica (`clamp(3.4rem, 7.2vw, 6.2rem)` em desktop e `clamp(2.4rem, 10vw, 3.8rem)` em mobile). Ambas as palavras em amarelo âmbar da marca (`var(--yellow)`), com `text-shadow` focado para garantir contraste e legibilidade perfeita diretamente sobre a parede e o violão, sem necessidade de scrim escuro.
- **Validação e Testes:**
  - `bash scripts/test-all.sh`: 14 testes frontend + 38 testes backend aprovados (100%).
  - `bash scripts/lint-all.sh`: 0 erros de sintaxe.
  - Capturas visuais geradas e validadas:
    - Desktop 1280x900 e 1440x900: composição natural com o violão completo à esquerda, moldura dourada inteira e assinatura manuscrita amarela de dimensões idênticas.
    - Mobile 375x812: enquadramento com violão e tela preservados, sem sobreposições indevidas.

## Transformação Editorial de Alta Costura: Inspiração "Mestizo" — 02 de novembro de 2026

- **Pedido do utilizador:**
  - *"faça coisas de jeito, estas a fazer ui horrivel. usa iso de inspiração e faça algo dejeito sem me fazer perder o tempo."*
  - Imagem de referência fornecida pelo utilizador: hero do restaurante **"Mestizo"**, com moldura de terracota quente, tipografia caligráfica clássica com floreios Spencerianos majestosos em tom marfim/champanhe, iluminação cinematográfica quente de restaurante fine-dining e barra de navegação integrada no topo com linha hairline sutil e tracking generoso.
- **Implementação efetuada:**
  - **Tipografia Caligráfica de Luxo (Pinyon Script & Monsieur La Doulaise):**
    - Adicionados os recursos de fontes locais `.woff2` de alta resolução em `assets/brand/fonts/` (`PinyonScript.woff2` e `Monsieur+La+Doulaise.woff2`), eliminando a caligrafia casual/escolar anterior (`NothingYouCouldDo`).
    - Composição editorial com a inicial **"C"** dotada de floreio curvo duplo Spenceriano, seguida das minúsculas fluidas e elegantes **"achupa"** em tom marfim porcelana (`#faebe0`), com subtítulo em maiúsculas espaçadas (`RESTAURANTE`) e rodapé geográfico sutil (`BARREIRO · COZINHA CABO-VERDIANA`).
  - **Moldura Editorial de Terracota ("Editorial Mat"):**
    - Enquadramento da Hero numa moldura exterior em terracota e âmbar queimado (`linear-gradient(145deg, #8a3d1c 0%, #6e2e12 50%, #54220b 100%)`), transformando o ecrã numa tela de alta costura gastronómica.
  - **Navegação Integrada e Invisível:**
    - O cabeçalho na página inicial foi integrado diretamente no topo do palco escuro, com linha divisória hairline quase imperceptível (`rgba(250, 235, 224, 0.2)`), logotipo em branco puro monocromático, links de navegação em maiúsculas refinadas com tracking largo (`letter-spacing: 0.24em; font-size: 11px`) e botão de reservas discreto em contorno de vidro (*ghost button*).
  - **Iluminação e Color Grading Cinematográfico:**
    - Aplicação de gradiente radial de vinheta atmosférica (`rgba(139, 60, 27, 0.12)` a `rgba(12, 7, 4, 0.9)`) que foca a luz no quadro tradicional de Cabo Verde e no violão da sala, conferindo calor e sofisticação incomparáveis.
  - **Adaptação Móvel Rigorosa:**
    - Margens e tipografia escaladas fluidamente para 375px/390px, garantindo que a composição inteira se mantenha 100% visível sem cortes laterais nem quebras visuais.
- **Validação e Testes:**
  - `bash scripts/test-all.sh`: 14 testes frontend + 38 testes backend aprovados (100%).
  - `bash scripts/lint-all.sh`: 0 erros de sintaxe (Python, JSON, JavaScript).
  - Screenshots capturados e validados em desktop (1440x900) e mobile (375x812).
  - Servidor preview ativo e atualizado em `http://localhost:3000/`.

## Restauração das Cores Naturais da Hero e Caligrafia em Amarelo — 02 de novembro de 2026

- **Pedido do utilizador:**
  - *"na gostei da forma que mudaste a cor do toda a hero na pagina inicio, deixa a mesma cor que estava, mantem o trabalho de letra que fizeste mas deixa a cor que estava ante. ficou horrivel essa cor ja agora."*
- **Implementação efetuada:**
  - **Cores Naturais da Fotografia:**
    - Removida a moldura exterior em terracota (`editorial-mat`), removido o filtro de color grading avermelhado e a vinheta densa.
    - A fotografia do espaço (`hero-parede-quadro.jpg`) foi restaurada a 100% das suas cores reais e calor natural: a parede de tom terroso/café, o violão de madeira pendurado e o quadro a óleo com a sua moldura dourada autêntica.
  - **Tipografia Caligráfica Preservada em Amarelo de Marca:**
    - Mantido o trabalho de caligrafia clássica de alta gama (`Monsieur La Doulaise` para floreio inicial + `Pinyon Script` para fluidez do texto cursivo).
    - Ambas as palavras (*"Restaurante"* e *"Cachupa"*) renderizadas na cor amarela original de identidade da marca (`var(--yellow)` / `#ffed00`), com sombra de texto focada para contraste ideal sobre o fundo natural.
    - Dimensões tipográficas perfeitamente idênticas para as duas palavras (`clamp(3.4rem, 7.2vw, 6.2rem)` no desktop e `clamp(2.3rem, 9.5vw, 3.6rem)` no mobile).
    - Espaçamento refinado no floreio inicial para transição fluida e legível em ambas as linhas.
  - **Correção da Visualização em Desktop:**
    - Corrigido o fechamento da media query em `frontend/src/styles/site.css` que provocava fuga visual da barra fixa móvel para o desktop a 1440px. A hero no desktop exibe agora exclusivamente o palco limpo e o cabeçalho translúcido com linha hairline discreta, cumprindo a diretriz de visualização pura antes do scroll.
- **Validação e Testes:**
  - `bash scripts/test-all.sh`: 14 testes frontend + 38 testes backend aprovados (100%).
  - `npm --prefix frontend run build:preview`: 7 páginas geradas sem erros.
  - Capturas visuais geradas e verificadas:
    - Desktop (1440x900): `hero-natural-yellow-desktop.png`
    - Mobile (375x812): `hero-natural-yellow-mobile.png`
  - Servidor de preview funcional em `http://localhost:3000/`.

## Reversão Total da Hero para o Estado Anterior — 02 de novembro de 2026

- **Pedido do utilizador:**
  - *"horrivel, volta a meter como era antes"*
- **Ações efetuadas:**
  - **Reversão Completa de Conteúdo e Estrutura:**
    - `frontend/fixtures/preview.json`: restaurado o título e cabeçalho original da Home para *"Cabo Verde, à mesa."*.
    - `frontend/src/render.py`: restaurada a estrutura editorial original com título `<h1>Cabo Verde, à mesa.</h1>`, traço vermelho de acento (`hero-rule`), texto de introdução da casa (`hero-slogan`) e os dois botões de ação originais (`contact_actions` com *"Ver reservas"* e *"Conhecer a casa"*).
  - **Reversão Completa de Estilos (`frontend/src/styles/site.css` e `assets/site.css`):**
    - Restaurado o cabeçalho original com fundo branco limpo, logótipo oficial colorido e botão de reserva em vermelho da marca.
    - Restaurado o layout de palco editorial com a fotografia `hero-parede-quadro.jpg`, o gradiente de proteção de contraste (`home-hero-scrim`) e alinhamento ergonómico.
    - Removidas as regras e definições experimentais de fontes cursivas na Hero.
  - **Testes e Validação:**
    - `bash scripts/test-all.sh`: 14 testes frontend + 38 testes backend aprovados a 100%.
    - Capturas de ecrã verificadas confirmando conformidade total com o estado anterior em desktop e mobile (`hero-restored-desktop.png` e `hero-restored-mobile.png`).
    - Servidor local atualizado e operacional em `http://localhost:3000/`.

## Hero de ecrã inteiro e conteúdo reduzido — 02 de novembro de 2026

- **Pedido do utilizador:** manter a navbar, preencher o primeiro ecrã com a fotografia e deixar na hero apenas “Cabo Verde, à mesa.”
- **Implementação:** removidos da hero o traço, a introdução e os dois botões. A fotografia ocupa o espaço restante do viewport abaixo da navbar. Na Home, a faixa de preview e a barra fixa mobile não aparecem no primeiro ecrã; as restantes secções da página mantêm-se abaixo da hero.
- **Ficheiros alterados:** `frontend/src/render.py`, `frontend/src/styles/site.css`, `frontend/tests/test_render.py`.
- **Validação:** `npm --prefix frontend test` (14/14), `npm --prefix frontend run lint` e `npm --prefix frontend run build:preview`. Browser em `1440×900`, `390×844` e `320×760`: navbar no topo, hero termina exatamente no fim do viewport, apenas o `h1` visível na hero, imagem carregada e sem overflow horizontal.
- **Preview:** `http://127.0.0.1:3000/`; atualizar a página para ver a versão gerada.

## Integração do menu na preview — 02 de novembro de 2026

- **Pedido do utilizador:** integrar o menu aprovado em `/menu/`, com navegação no site e sem aviso de demonstração.
- **Implementação frontend:** `menuEnabled` ligado na fixture; link de Menu na navegação desktop/móvel, no painel de navegação e no rodapé; preview copia para `frontend/dist/menu/` HTML, CSS, JavaScript, dados e marca. O catálogo importado não tem imagens de produto; as antigas pastas `assets/` e `assets_2/` não são publicadas e são removidas de distribuições de preview anteriores. Removidos `noindex,nofollow` e o aviso de demonstração; documentação local atualizada.
- **Validação:** 16/16 testes frontend, lint e build de preview aprovados; 9/9 testes do menu aprovados. `/menu/`, CSS, JS, dados, logótipo, fontes e imagens de amostra responderam HTTP 200 em `http://127.0.0.1:3000/`. Inspeção no browser a 320 px: categorias, detalhe do prato e fecho pelo botão funcionais. A ferramenta de browser não emitiu eventos de teclado no teste de Escape, por isso esse gesto não foi revalidado nesta sessão.
- **Pendência de integração de produção:** o gerador em `backend/src/generator.py` não copia `menu/`; Gemini deve incluir os mesmos recursos públicos no build de produção e garantir `navigation.menuEnabled=true` no modelo aprovado. Não alterado pelo frontend.
- **Estado:** menu integrado na preview local e pronto para revisão. Build de produção ainda não integrado; não houve deploy.

## Importação do catálogo de produtos — 02 de novembro de 2026

- **Fonte:** dois CSVs fornecidos pelo utilizador; 86 linhas em cada ficheiro, conteúdo equivalente apesar da ordem diferente das colunas.
- **Implementação:** importados 71 registos com estado `Aprovado`; a pedido do utilizador, adicionados também os oito pratos Cachupa CR-68 a CR-75 em `Outros pratos`, apesar de a fonte os marcar `Para validar`. Preservados códigos, nomes e preços existentes; sem inventar porções ou detalhes alimentares. As outras sete linhas pendentes continuam excluídas. Não foram copiados `Notas internas` ou outros metadados privados. A preview não distribui as imagens antigas sem referência.
- **Dados em falta na fonte:** fotografias, descrições, ingredientes, alergénios e validação alimentar. A interface agora não apresenta fotos/descrições do catálogo antigo e mostra explicitamente o aviso de informação alimentar não validada. Nomes de produtos permanecem em português; interface e categorias continuam localizadas nos quatro idiomas.
- **Validação:** 10/10 testes do menu, `node --check`, 16/16 testes frontend, lint e build de preview aprovados. No browser em 1440 px, `Outros pratos` mostra as oito Cachupas e a Espetada de búzio (9 itens), sem overflow horizontal.
- **Estado:** oito Cachupas adicionadas à preview segundo instrução expressa do utilizador. A origem ainda assinala esses registos como `Para validar`; ingredientes, alergénios, disponibilidade e fotografias não foram confirmados.

## Migração da Nova UI Editorial (Figma Make `Cachupa Rst`) & Colocação Integral de Fotografias — 02 de novembro de 2026

- **Pedido do utilizador:**
  - *"vais na pasta Cachupa Rst e vais encontrar o novo design de ui do site. puxa ele e faz essa atualização, antes de fazer isso, analisa e diz se percebeste."*
  - *"faz isso e depois adiciona as fotos certas nos lugares certos"*
- **Arquitetura preservada:**
  - A nova interface desenhada no Figma Make (`Cachupa Rst/src/App.tsx` e `Cachupa Rst/src/index.css`) foi integrada diretamente no gerador estático Python do frontend (`frontend/src/templates/base.html`, `frontend/src/render.py`, `frontend/src/styles/site.css`, `frontend/src/scripts/site.js`, `frontend/fixtures/preview.json` e `frontend/tests/test_render.py`), preservando integralmente o contrato `v1` (`render_site(model) -> dict[str, str]`), zero dependências externas e compatibilidade com `/menu/`.
- **Direção Visual & Componentes Integrados:**
  - **Tokens & Tipografia:** superfície `--paper` (`#faf8f2`), `--cream` (`#f4f0e6`), `--ink` (`#18221e`), `--blue` (`#006c9a`), `--red` (`#d51f2c`) e `--yellow` (`#ffed00`); títulos editoriais em `Georgia` com acentos em itálico vermelho (`<em>`) e corpo/eyebrows em sans-serif limpa.
  - **Cabeçalho & Navegação:** assinatura tipográfica `Cachupa RST`, navegação principal com sublinhado vermelho animado, botão retangular `Reservar ↗`, gaveta móvel deslizante com suporte completo a teclado (`Escape`, contenção de `Tab`) e fallback progressivo sem JavaScript.
  - **Molduras *Passe-Partout* de Galeria:** todas as fotografias e obras de arte repousam em moldura dupla editorial (`padding: 8px` sobre `--paper` com filetes de `1px`), preservando o enquadramento completo das pinturas a óleo, do violão na Hero e das asas das caçarolas de barro.
  - **Modal `<dialog id="art-dialog" closedby="any">` em Ecrã Dividido:** visualização `1.2fr / 0.8fr` com contador `01 / 11`, título, técnica, descrição curatorial, metadados, navegação por setas/botões, *light-dismiss* com fallback de coordenadas e contenção de scroll via CSS (`overscroll-behavior: contain` em `dialog:modal` e `dialog::backdrop`, sem mutar `overflow` em `<html>` ou `<body>`).
- **Mapeamento de Fotografias Reais e Pinturas (`frontend/fixtures/preview.json`):**
  - **Início (`/`):** `hero-parede-quadro.jpg` na Hero; `studio-carne.jpg` em `#speciality`; `studio-polvo.jpg` e `studio-refogada.jpg` em `#pratos`; faixa azul numerada `01–03` em `#noticias`; `studio-casa-quadro.jpg` em `#house`; `arte-caldeirao.jpg`, `arte-serenata.jpg` e `arte-pescador.jpg` em `#art`; `studio-frango.jpg` em `#visit`.
  - **A nossa casa (`/a-nossa-casa/`):** `studio-sala.jpg` na Hero; `studio-pintura-cachupa.jpg` (*A Cozinheira da Terra*, Lito Silva) em `#story`; `studio-hero.jpg` e `studio-carne.jpg` em `#cozinha`; faixa final de convite em vermelho.
  - **Galeria (`/galeria/`):** medalhão `LS` + biografia de Lito Silva e grelha escalonada numerada (`01` a `11`) com todas as 11 obras originais (`arte-*.jpg`).
  - **Contactos (`/contactos/`):** fotografia real da montra na Rua Almirante Reis (`janela-1600.webp` com variantes responsivas `480w`, `960w`, `1600w`) integrada em `.map-space`, telefone direto em grande escala e grelha semanal pontilhada.
  - **Reservas (`/reservas/`), Privacidade (`/privacidade/`) e 404 (`/404.html`):** canais factuais dinâmicos + 3 passos em `--cream` + nota `Importante`; índice lateral `sticky` com 5 secções ancoradas (`#dados` a `#acessibilidade`); página 404 centrada.
- **Validação Executada:**
  - `npm --prefix frontend run build:preview`: 7 páginas + `/menu/` geradas em `frontend/dist/`.
  - `bash scripts/lint-all.sh`: sintaxe Python, JSON e JavaScript aprovada.
  - `bash scripts/test-all.sh`: 17/17 testes frontend + 38/38 testes backend aprovados.

## Galeria «A chegar brevemente» e Retrato Real de Lito Silva — 13 de novembro de 2026

- **Pedido do utilizador:**
  - *"exato esse é o certo, so uma coisa / na galeria mete a chegar brevemente ja que vamos fazer fotos novas das artes e meta a foto que esta em assets/photos/litosilva.lpg"*
- **Diagnóstico do desalinhamento anterior no Git:**
  - Nos commits `c942e43` e `de049dd`, `assets/site.css` na raiz recebeu o CSS editorial novo enquanto os HTMLs da raiz (`index.html`, `galeria/index.html`, etc.) e `assets/site.js` continuavam no formato legado (já que `frontend/dist/` está em `.gitignore`). A pré-visualização completa e atualizada serve a partir de `frontend/dist/` na porta local `3000`.
- **Alterações implementadas (`frontend/**` e `assets/site.css`):**
  - **Fotografia real do artista (`frontend/public/assets/photos/litosilva.jpg`):** copiada a partir de `assets/photos/litosilva.jpg` (`1439×1067`, proporção `4:3`, `441811` bytes). Registada em `frontend/fixtures/preview.json` com `artist.portrait = "litosilva"` e `focalPoint` `{x: 0.72, y: 0.3}`.
  - **Estado «A chegar brevemente» (`frontend/fixtures/preview.json`, `frontend/src/render.py`, `frontend/src/styles/site.css`):**
    - Limpo `artworks: []`, limpo `artworkIds: []` na secção `#art` da página inicial (`Link`: `Conhecer a galeria`), removidas as 11 entradas antigas `arte-*` de `images` e ajustada a cópia da página `/galeria/` para evitar repetição.
    - Em `render_site` (`gallery`), `.artist-intro.has-portrait` passa a apresentar o retrato `litosilva.jpg` em `.artist-portrait` com proporção `4:3` e prioridade de carregamento LCP apenas quando não existe imagem hero na página (`loading="eager" fetchpriority="high"`). Quando `artworks` está vazio, `.exhibition-title` mostra `A chegar brevemente.` e `art_cards` renderiza o cartão editorial `.empty-gallery` adaptado à secção `#art` da homepage e à página `/galeria/`.
  - **Correção de flash da gaveta móvel (`frontend/src/styles/site.css`, `frontend/src/scripts/site.js`):** adicionada a classe `.js-nav-ready` via `requestAnimationFrame` após `void nav.offsetWidth` para evitar que o menu móvel deslizasse brevemente sobre o ecrã ao carregar a página.
  - **Testes (`frontend/tests/test_render.py`):** atualizado `test_real_photos_and_artworks_placed_in_correct_slots` para validar `litosilva.jpg`, `.artist-intro.has-portrait`, `"A chegar brevemente"` e `0` fichas `art-dialog` na pré-visualização.
- **Validação Executada:**
  - `npm --prefix frontend run build:preview`: 7 páginas geradas em `frontend/dist/`.
  - `bash scripts/lint-all.sh`: sintaxe válida em frontend e backend.
  - `bash scripts/test-all.sh`: 17/17 testes frontend + 38/38 testes backend aprovados.
  - `validator.validate_model(model, 'preview', public_dir='frontend/public')`: `errors = []` (3 avisos esperados de pré-visualização: `whatsappHref`, `emailHref`, `menuEnabled`).
  - Verificação visual em Chrome headless (emulação móvel `390×1750`, `320×1850` e desktop `1440×2100`) em `/galeria/` e `/#art`: zero erros de consola, zero falhas de rede (`HTTP 200` em `/`, `/galeria/` e `/assets/photos/litosilva.jpg`), imagens carregadas (`naturalWidth > 0`) e zero overflow horizontal (`document.documentElement.scrollWidth === window.innerWidth`).
- **Pendente de decisão do utilizador:**
  - Confirmar se pretende sincronizar as 7 páginas HTML geradas de `frontend/dist/` e `frontend/src/scripts/site.js` para a raiz do repositório para alinhar o GitHub com a nova UI.

## Remoção do banner de pré-visualização, melhoria de Reservas/Privacidade, correções do Menu e alinhamento com produção — 13 de novembro de 2026

- **Pedidos do utilizador:** remover o texto `Pré-visualização · ...` do topo, resolver incoerências e melhorar `/reservas/`, corrigir problemas em `/menu/` e alinhar os textos de privacidade e a raiz do repositório para publicação.
- **Alterações implementadas (`frontend/**`, `menu/**` e `assets/`):**
  - **Remoção do banner visual (`frontend/src/render.py`):** eliminada a faixa visível `Pré-visualização · Fotografias selecionadas; contactos digitais por confirmar`, mantendo apenas a meta tag `noindex, nofollow` em builds de pré-visualização.
  - **Melhoria da página `/reservas/` (`frontend/src/render.py`, `frontend/src/styles/site.css`, `assets/site.css`):** suprimida a frase enganadora «Os canais digitais de reserva não estão configurados.» quando existe telefone confirmado (`963 572 411`); adicionados links diretos em `.inline-links` para `/contactos/`, `/menu/` (quando `menuEnabled` está ativo) e Google Maps, cartões `.channel-summary` com resumo do horário (`Segunda a domingo · 11:00–23:00`) e morada (`R. Alm. Reis 22 B, 2830-326 Barreiro`), nota prática para grupos na caixa `.notice` e CTA móvel `Ligar para reservar` na barra inferior. Adicionado `id="horario"` ao bloco de horários em `/contactos/`.
  - **Alinhamento editorial (`frontend/fixtures/preview.json`):** corrigido o terceiro destaque na página inicial e a cópia de `/reservas/` para o atendimento telefónico direto; atualizada a página `/privacidade/` para refletir com exatidão a ausência de formulários/cookies de rastreio e a gravação local estritamente funcional do idioma do menu (`cachupa_menu_lang` em `localStorage`).
  - **Correções em `/menu/` (`menu/index.html`, `menu/style.css`):** adicionado `<link rel="icon" href="brand/logo.svg" type="image/svg+xml">` para eliminar o erro `404` de `/favicon.ico`, `padding-block: 10px` em `.header-inner` abaixo de `600px` para respiração vertical ao quebrar linha, e `gap: 14px` em `.category-nav` abaixo de `360px`.
  - **Testes (`frontend/tests/test_render.py`):** atualizados `test_unknown_contacts_are_not_invented` (cobre reservas por telefone e cenário sem qualquer contacto) e `test_production_has_no_preview_banner` (valida ausência de `"Pré-visualização"` em ambos os modos).
- **Verificação executada (após última edição):**
  - `bash scripts/lint-all.sh` → saída `0`; `bash scripts/test-all.sh` → frontend `17/17 OK` e backend `39/39 OK`; `node --test menu/tests/menu.test.cjs` → `10/10 pass`; `node --check menu/script.js` → saída `0`.
  - `npm --prefix frontend run build:preview` → 7 páginas + `/menu/` geradas em `frontend/dist/`.
  - Chrome headless em `http://127.0.0.1:3000/` (`frontend/dist/`) e em servidor local da raiz publicada (ambos em 8 rotas × 3 larguras `320/390/1440 px` = `24` verificações cada): zero erros de consola, zero erros HTTP (incluindo `/menu/` e `/favicon.ico`), zero overflow horizontal, zero imagens quebradas após scroll, ausência confirmada de `"Pré-visualização"` e alternância de idioma funcional em `/menu/`.

## Correções finais da auditoria geral (GitHub Pages em subpasta, `/menu/` i18n/mobile e lint) — 13 de novembro de 2026

- **Alterações implementadas (`frontend/**`, `menu/**` e raiz regenerada):**
  - **Portabilidade raiz (`/`) e subpasta (`/cachupa-rst-site/`):** adicionados `_rel_url()` e `_relativize_html()` em `frontend/src/render.py` (com suporte no `base.html`) para converter todos os links e recursos internos (`href`, `src`, `srcset`) em URLs relativos à profundidade da página, eliminando a dependência da raiz `/` em alojamento GitHub Pages sem `CNAME`.
  - **`404.html` em qualquer profundidade (`_NOT_FOUND_HEAD_ASSETS`):** injetado um `<base>` dinâmico via script em `<head>` (deteta `/cachupa-rst-site/` ou `/`) antes de criar `<link rel="icon">`, `<link rel="stylesheet">` e `<script src>`, evitando pedidos `404` pelo preloader especulativo do browser em URLs fundos inexistentes, com fallback `<noscript>`.
  - **`/menu/` (`menu/index.html`, `menu/script.js`, `menu/style.css`):** corrigido `.site-return` para `href="../"` com `data-copy="siteReturn"` e traduções `pt`/`en`/`es`/`fr` em `UI_COPY`; alinhado `detailHint` de fallback para «Preços e porções conforme o catálogo aprovado.» e ajustado `.category-nav` (`gap: 12px` em `<=600px` e `<=360px`) para caberem as 4 abas sem corte nos `390 px`.
  - **Lint e tipos (`frontend/src/render.py`, `frontend/tools/*.py`, `frontend/tests/*.py`):** removido `F841` (`digital = reservation_channels(model)`), convertidas formatações `%` em f-strings (`UP031`), organizados imports (`I001`) e atualizados os testes em `frontend/tests/test_render.py` para validar URLs relativos e o loader `<base>` do `404.html`.
