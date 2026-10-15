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
