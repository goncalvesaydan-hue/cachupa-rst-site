# Frontend — Cachupa Rst

Responsável: Codex. Coordenação: Orca. Backend: Gemini.
Entrega de 14 de outubro de 2026: frontend estático funcional e isolado, preparado para receber o modelo do contrato v1. Ainda não é uma publicação final: faltam fotografias, contactos, horários, informação do artista e revisão editorial.

## Executar

Requisitos: Python 3.10+ e Node.js para a verificação de sintaxe JavaScript. npm é apenas um atalho; não há pacotes a instalar.

Na pasta `frontend`:

```sh
npm run build:preview
npm run dev
npm test
npm run lint
```

Equivalentes: `python3 tools/preview.py`, `python3 tools/preview.py --serve`, `python3 -m unittest discover -s tests -v`, `python3 tools/check.py`.

Abrir http://127.0.0.1:18952/. O servidor só escuta no computador local. Interromper com Ctrl+C. Não há atualização automática: depois de editar, gerar novamente e atualizar o navegador. A porta 18951 continua reservada à versão anterior.

`tools/preview.py --model /caminho/modelo.json` aceita um modelo alternativo com `preview: true`. A saída é sempre `frontend/dist/`; o comando não publica o site. O renderer não rejeita produção, pois essa validação pertence ao backend; o comando de demonstração rejeita modelos de produção para impedir uso acidental.

## Organização

- `src/render.py`: apresentação; recebe o modelo completo e devolve HTML por rota.
- `src/templates/base.html`: estrutura comum, navegação, rodapé e metadados.
- `src/styles/site.css`: estilos responsivos, tipografia e estados.
- `src/scripts/site.js`: navegação móvel, cópia de email e detalhe das obras.
- `public/assets/brand/`: logótipo, fontes locais e licenças copiadas dos recursos existentes.
- `fixtures/preview.json`: dados provisórios para desenvolvimento; não é fonte editorial de produção.
- `tests/`: testes unitários do renderer.
- `tools/`: construção e servidor exclusivamente de preview, verificação de sintaxe.
- `dist/`: saída gerada, ignorada pelo Git.

## Integração para o Gemini

Fonte de verdade: `../docs/api-contract.md`. O frontend consome `schemaVersion: 1` sem mudar o contrato. Não lê `content/`, não consulta APIs, não persiste reservas e não normaliza contactos.

Entrada única:

```python
import importlib.util
from pathlib import Path

project = Path('/caminho/para/Site')
spec = importlib.util.spec_from_file_location('cachupa_frontend', project / 'frontend/src/render.py')
frontend = importlib.util.module_from_spec(spec)
spec.loader.exec_module(frontend)
pages = frontend.render_site(validated_model)
# pages: {'index.html': '<!doctype html>...', 'galeria/index.html': '...', ...}
# O backend escreve estes ficheiros numa saída isolada e controla a publicação.
```

O modelo é obrigatório e completo; os valores desconhecidos usam `null`/listas vazias segundo o contrato. A função não altera o modelo nem escreve ficheiros. Lê apenas o template local ao importar. URLs e texto recebem proteção de apresentação, mas a validação integral e a exclusão de rascunhos são responsabilidade do backend.

Para montar a distribuição, o Gemini deverá:

1. Validar/normalizar conteúdo para o contrato v1 e excluir obras não publicadas.
2. Passar o modelo a `render_site` e escrever cada resultado na rota relativa indicada.
3. Copiar o conteúdo de `frontend/public/` para a raiz da distribuição.
4. Copiar `src/styles/site.css` para `assets/site.css` e `src/scripts/site.js` para `assets/site.js`.
5. Gerar/copiar apenas imagens públicas referenciadas pelo modelo para `/assets/...`; os originais privados ficam fora da distribuição.
6. Se `navigation.menuEnabled` for `true`, copiar `menu/index.html`, CSS, JavaScript, dados e marca para `/menu/`; não publicar as antigas pastas de imagens sem referência no catálogo. Se forem adicionadas imagens de produto aprovadas, atualizar explicitamente os recursos públicos copiados.
7. Configurar no alojamento a resposta HTTP 404 com `404.html`; entregar todas as rotas com barra final.
8. Validar a saída em conjunto com a Orca antes de publicar.

O site pressupõe publicação na raiz do domínio. Uma publicação num subcaminho exige decisão coordenada sobre URLs; não introduzir prefixos apenas de um lado.

### Dados e comportamentos

- Os links de WhatsApp, email, telefone e direções chegam prontos do backend. A interface não reconstrói mensagens nem números. Um pedido de reserva só é confirmado pela equipa fora do site.
- Sem contactos: aparece um estado informativo, sem links falsos.
- `navigation.menuEnabled` controla os links do menu no cabeçalho, navegação móvel e rodapé. A fixture de preview já o ativa e publica `/menu/`; o gerador de produção ainda precisa copiar os mesmos recursos públicos. O menu inclui 71 produtos aprovados e oito Cachupas em `Outros pratos`, adicionadas por instrução do utilizador apesar de estarem marcadas `Para validar`; as outras sete pendentes não são publicadas. Não há imagens ou detalhes alimentares validados.
- `images` é um mapa por ID. Dimensões, alt, variantes, crédito e posição focal são consumidos diretamente. Imagens principais têm prioridade; restantes carregam progressivamente.
- Retrato: o renderer interpreta `artist.portrait` como ID em `images`. A Orca deve confirmar esta interpretação se o backend precisar de outro formato; o contrato canónico não foi alterado nesta entrega.
- Pinturas usam `object-fit: contain`, sem recorte nem variante móvel alternativa. A imagem completa abre num diálogo; sem JavaScript o link abre o ficheiro diretamente.
- `artworkSelection.artworkIds: []` significa seleção vazia. A galeria apresenta todas as obras recebidas, ordenadas por `order`.
- `preview: true` mostra indicação de preparação, espaços reservados para imagens e `noindex`. Metadados canónicos só são gerados quando existe `site.baseUrl` HTTPS.
- A política de privacidade de preview não é um documento legal final. O conteúdo e os serviços efetivamente usados devem ser confirmados antes de publicar.

## Interface e identidade

HTML semântico, CSS e JavaScript nativos, com renderização em Python. Tipografia e logo existentes; azul na estrutura e nos títulos, vermelho nas ações, amarelo presente na marca. Fotografias de grande dimensão, texto curto e alternância editorial. A composição final deve ser revista com as fotografias reais; os espaços reservados não representam o resultado visual final.

Fontes locais: Big Shoulders, Work Sans e Nothing You Could Do (recurso disponível, não obrigatório no layout), acompanhadas dos ficheiros OFL em `public/assets/brand/fonts/`. Manter as licenças na distribuição dos recursos.

A navegação móvel mantém links disponíveis sem JavaScript; com JavaScript, o menu contém o foco e devolve-o ao botão ao fechar. Os controlos móveis têm áreas de toque de pelo menos 44 px. Imagens fora do hero carregam progressivamente e a preferência por movimento reduzido é respeitada.

O cabeçalho mantém o mesmo fundo claro em todas as páginas, com a marca à esquerda, links centrados e ação principal “Reservar” à direita. Em mobile, o botão abre um painel simples com os mesmos destinos e um link interno para reservas; não há conteúdo promocional duplicado no menu.

## Verificação e limites

Dezasseis testes unitários cobrem rotas, imutabilidade, dados ausentes, URLs, escaping, contactos, horários que passam da meia-noite, imagens, versão do contrato, navegação, cópia pública do menu e canais de reserva. `lint` verifica sintaxe Python/JSON/JavaScript; não é um auditor completo de CSS ou acessibilidade.

Verificação no navegador: as sete rotas em 320, 375, 390, 768, 900, 901, 1024 e 1440 px, sem overflow horizontal e com um único `h1`; navegação muda no breakpoint; painel mobile fica acima do aviso de preview, contém o foco e fecha com Escape; navegação alternativa disponível sem JavaScript.

Ainda exigem validação com o backend e dados reais: recortes, cores das pinturas, contactos externos, cópia de email nos navegadores alvo, erro real de imagem, ampliação de texto, metadados de produção e desempenho final. Não confundir os testes de apresentação com aprovação para publicação.

## Segunda direção visual

A revisão pedida pelo utilizador está descrita em `VISUAL-DIRECTION.md`. A preview utiliza grafismos vetoriais da identidade existente em vez de caixas cinzentas. Na página inicial, a fotografia abre o percurso sem texto sobreposto; o título, a introdução e as ações surgem numa faixa editorial própria. As reservas usam apenas canais realmente fornecidos pelo modelo: sem WhatsApp ou email válidos, a interface explica que os contactos estão indisponíveis e não simula um pedido. Não houve mudança no contrato v1. Os SVG de panela, vapor e grãos são recursos de marca, não fotografias nem representações de obras reais.

Nesta revisão, as sete rotas foram verificadas em cinco larguras (320, 390, 768, 1024, 1440 px), sem overflow horizontal. Fotos e contactos permanecem pendentes.

## Fotografias selecionadas

As fotografias fornecidas pelo utilizador já estão integradas na preview. Ver `PHOTO-SELECTION.md` e o inventário `fixtures/photo-selection.json`. Os ficheiros WebP estão incluídos em `public/assets/photos/`; o site não depende do disco externo. A abertura foi adaptada para preservar o prato completo ao lado do texto. As referências das obras são provisórias e a autoria permanece desconhecida até confirmação.
