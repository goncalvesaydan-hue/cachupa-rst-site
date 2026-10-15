# Cachupa Rst — Menu

Cópia independente do projeto `/Users/aydangoncalves/Documents/menu-luxury-ref`, adaptada à identidade do Cachupa Rst. O projeto original não foi alterado. A cópia preserva também o conteúdo atual de data.js, incluindo alterações locais existentes no original.

## Abrir

Abrir `index.html` no navegador. Também funciona servido dentro do site em `/menu/`.

```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory "/Users/aydangoncalves/Desktop/Restaurante Cachupa/Site"
```

Aceder a `http://localhost:8000/menu/`.

## Identidade

Logo vetorial em `brand/logo.svg`. Fontes locais e respetivas licenças em `brand/fonts/`: Work Sans, Big Shoulders e Nothing You Could Do. Sem chamadas ao Google Fonts.

Azul #006C9A, vermelho #DD1A2A, amarelo #FFED00 e branco. Títulos de letreiro, nomes e preços em Work Sans e uma breve nota manuscrita na versão desktop.

## Conteúdo preservado

Os 22 produtos, imagens, preços, descrições e etiquetas alimentares do original mantêm-se. São conteúdos de demonstração; ainda não representam a ementa validada do Cachupa Rst. Não foi acrescentada uma receita de cachupa fictícia.

## Funcionalidades

- Português, inglês, espanhol e francês.
- Preferência guardada em `cachupa_menu_lang`, separada do menu original.
- Categorias por clique e teclado.
- Detalhe em dialog nativo, com fecho por botão e Escape, retorno do foco e da posição na lista.
- Versão móvel, zoom permitido e respeito por movimento reduzido.
- Continua a ser uma interface estática. Backend, painel de gestão e ligação ao Notion não fazem parte desta adaptação.

## Verificação

```sh
node --check script.js
node --test tests/menu.test.cjs
```

Os nove testes existentes passaram. Verificação no navegador: desktop, 390 px e 320 px; abertura/fecho de prato, retorno do foco, troca de categoria e idiomas. Imagens locais verificadas na categoria testada. Não substitui testes em dispositivos físicos.

Capturas em `visuals/cachupa-desktop.png` e `visuals/cachupa-mobile.png`.
