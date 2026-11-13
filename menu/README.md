# Cachupa Rst — Menu

Cópia independente do projeto de menu, adaptada à identidade do Cachupa Rst. O projeto original não foi alterado. O conteúdo atual foi aprovado pelo utilizador para publicação.

## Abrir

O site serve o menu em `/menu/`, no mesmo domínio e sem iframe. A preview em `frontend/dist/menu/` é gerada pelo comando do frontend:

```sh
npm --prefix frontend run build:preview
```

Para servir a preview localmente, usar `npm --prefix frontend run dev` e abrir `http://127.0.0.1:18952/menu/`.

## Identidade

Logo vetorial em `brand/logo.svg`. Fontes locais e respetivas licenças em `brand/fonts/`: Work Sans, Big Shoulders e Nothing You Could Do. Sem chamadas ao Google Fonts.

Azul #006C9A, vermelho #DD1A2A, amarelo #FFED00 e branco. Títulos de letreiro, nomes e preços em Work Sans e uma breve nota manuscrita na versão desktop.

## Conteúdo carregado

O catálogo tem 86 linhas nos CSVs fornecidos. Estão no menu 79 produtos: 71 marcados `Aprovado` e as oito Cachupas (CR-68 a CR-75), incluídas a pedido do utilizador em `Outros pratos`. A categoria fica com nove produtos, além de Bebidas (51), Entradas (13) e Sobremesa (6). As outras sete linhas marcadas `Para validar` permanecem excluídas.

O CSV só fornece nome, preço e, por vezes, porção. As Cachupas continuam marcadas `Para validar` na fonte; foram incluídos apenas os nomes e preços existentes, sem inventar porções ou detalhes alimentares. Os nomes mantêm-se em português nas quatro escolhas de idioma; categorias e interface são traduzidas. Não há fotografias, descrições, ingredientes ou alergénios validados para estes produtos. O menu mostra uma nota para clientes com alergias e não reutiliza as imagens ou descrições do catálogo anterior. A coluna `Notas internas` e restantes metadados editoriais não são publicados.

## Funcionalidades

- Português, inglês, espanhol e francês.
- Preferência guardada em `cachupa_menu_lang`, separada do menu original.
- Categorias por clique e teclado.
- Dialog nativo para produtos que tenham detalhes editoriais; o catálogo importado não tem esses dados, por isso os seus itens são apresentados como linhas sem interação.
- Versão móvel, zoom permitido e respeito por movimento reduzido.
- Continua a ser uma interface estática. Backend, painel de gestão e ligação ao Notion não fazem parte desta adaptação.

## Verificação

```sh
node --check script.js
node --test tests/menu.test.cjs
```

`node --test tests/menu.test.cjs` verifica os 79 produtos, preços, porções, as oito Cachupas em `Outros pratos`, exclusão dos restantes pendentes e consistência entre idiomas. A disponibilidade de alergénios, detalhes e fotografias continua pendente de dados aprovados.

Capturas em `visuals/cachupa-desktop.png` e `visuals/cachupa-mobile.png`.
