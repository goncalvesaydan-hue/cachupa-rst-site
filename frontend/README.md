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
6. Configurar no alojamento a resposta HTTP 404 com `404.html`; entregar todas as rotas com barra final.
7. Validar a saída em conjunto com a Orca antes de publicar.

O site pressupõe publicação na raiz do domínio. Uma publicação num subcaminho exige decisão coordenada sobre URLs; não introduzir prefixos apenas de um lado.

### Dados e comportamentos

- Os links de WhatsApp, email, telefone e direções chegam prontos do backend. A interface não reconstrói mensagens nem números. Um pedido de reserva só é confirmado pela equipa fora do site.
- Sem contactos: aparece um estado informativo, sem links falsos.
- `menuEnabled: false` mantém o menu fora da navegação. A integração do menu é uma fase posterior; não ativar até existir `/menu/` real.
- `images` é um mapa por ID. Dimensões, alt, variantes, crédito e posição focal são consumidos diretamente. Imagens principais têm prioridade; restantes carregam progressivamente.
- Retrato: o renderer interpreta `artist.portrait` como ID em `images`. A Orca deve confirmar esta interpretação se o backend precisar de outro formato; o contrato canónico não foi alterado nesta entrega.
- Pinturas usam `object-fit: contain`, sem recorte nem variante móvel alternativa. A imagem completa abre num diálogo; sem JavaScript o link abre o ficheiro diretamente.
- `artworkSelection.artworkIds: []` significa seleção vazia. A galeria apresenta todas as obras recebidas, ordenadas por `order`.
- `preview: true` mostra indicação de preparação, espaços reservados para imagens e `noindex`. Metadados canónicos só são gerados quando existe `site.baseUrl` HTTPS.
- A política de privacidade de preview não é um documento legal final. O conteúdo e os serviços efetivamente usados devem ser confirmados antes de publicar.

## Interface e identidade

HTML semântico, CSS e JavaScript nativos, com renderização em Python. Tipografia e logo existentes; azul na estrutura e nos títulos, vermelho nas ações, amarelo presente na marca. Fotografias de grande dimensão, texto curto e alternância editorial. A composição final deve ser revista com as fotografias reais; os espaços reservados não representam o resultado visual final.

Fontes locais: Big Shoulders, Work Sans e Nothing You Could Do (recurso disponível, não obrigatório no layout), acompanhadas dos ficheiros OFL em `public/assets/brand/fonts/`. Manter as licenças na distribuição dos recursos.

## Verificação e limites

Oito testes unitários cobrem rotas, imutabilidade, dados ausentes, URLs, escaping, contactos, horários que passam da meia-noite, imagens e versão do contrato. `lint` verifica sintaxe Python/JSON/JavaScript; não é um auditor completo de CSS ou acessibilidade.

Verificação no navegador: página inicial em 320, 390, 768, 1024 e 1440 px sem overflow horizontal; menu móvel e Escape; abertura da galeria, passagem para obra seguinte e restituição de foco ao fechar por Escape, com recurso explicitamente identificado como teste. Sem erros de consola observados nesse percurso.

Ainda exigem validação com o backend e dados reais: recortes, cores das pinturas, contactos externos, cópia de email nos navegadores alvo, erro real de imagem, ampliação de texto, revisão completa sem JavaScript, metadados de produção e desempenho final. Não confundir os testes de apresentação com aprovação para publicação.

## Segunda direção visual

A revisão pedida pelo utilizador está descrita em `VISUAL-DIRECTION.md`. A preview utiliza agora grafismos vetoriais da identidade existente em vez de caixas cinzentas. Quando há uma imagem principal válida, a página inicial passa para fotografia de fundo em grande dimensão. Não houve mudança no contrato v1. Os SVG de panela, vapor e grãos são recursos de marca, não fotografias nem representações de obras reais.

Nesta revisão, as sete rotas foram verificadas em cinco larguras (320, 390, 768, 1024, 1440 px), sem overflow horizontal. Fotos e contactos permanecem pendentes.

## Fotografias selecionadas

As fotografias fornecidas pelo utilizador já estão integradas na preview. Ver `PHOTO-SELECTION.md` e o inventário `fixtures/photo-selection.json`. Os ficheiros WebP estão incluídos em `public/assets/photos/`; o site não depende do disco externo. A abertura foi adaptada para preservar o prato completo ao lado do texto. As referências das obras são provisórias e a autoria permanece desconhecida até confirmação.
