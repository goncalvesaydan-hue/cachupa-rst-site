# Seleção de fotografias — Cachupa Rst

## Origem e critério

Pasta fornecida pelo utilizador: `/Volumes/Aydan/CACHUPA RESTAURANTE/`.
Triagem visual de 429 imagens: 276 JPG, 152 HEIC e 1 PNG. Os três vídeos não foram usados. Foram comparadas folhas de miniaturas e ampliadas as candidatas principais.

Selecionadas 10 imagens. Critérios: nitidez, resolução, prato reconhecível, variedade de enquadramentos, ambiente do restaurante e pinturas inteiras. Montagens, capturas de redes sociais, logótipos alternativos, repetições e miniaturas pequenas ficaram fora. A série promocional com fundo preto não foi escolhida nesta versão; preferiram-se fotografias com contexto do restaurante.

## Escolhas

| Original | Utilização | Motivo |
|---|---|---|
| IMG_0952.HEIC | Abertura | Cachupa visível por inteiro, detalhe suficiente e enquadramento horizontal. |
| IMG_6528.JPG | Especialidade | Apresentação em barro, complementar à abertura. |
| IMG_0910.HEIC | Cozinha | Ingredientes vistos em conjunto; sem associar uma receita não confirmada. |
| IMG_0984.HEIC | Cozinha | Outra apresentação do milho, com ovos e enchidos. |
| IMG_7633.JPG | Casa na página inicial | Mesas, pinturas e ambiente na mesma imagem. |
| IMG_7634.JPG | Abertura da página Casa | Vista complementar da sala e da entrada. |
| IMG_7635.JPG | Visita | Mesa junto à janela e marca visível no vidro. |
| IMG_7636.JPG | Galeria: referência 01 | Pintura completa, original com 3024 × 4032 px. |
| IMG_7637.JPG | Galeria: referência 02 | Pintura de músicos completa, com melhor resolução que a miniatura equivalente. |
| IMG_7639.JPG | Galeria: referência 03 | Pintura com figuras em movimento completa e contextualizada na sala. |

As referências 01–03 não são títulos atribuídos pelo artista. Autoria, títulos, técnica, dimensões, data e créditos continuam por confirmar. Não se deduziu a identidade do artista pela assinatura. Estes dados não devem ser promovidos a catálogo de produção automaticamente.

## Exportação

Cópias em `public/assets/photos/`, com dimensões proporcionais de até 480, 960 e 1600 px de largura, sem ampliação acima da resolução disponível. Três imagens de detalhe adicionais, até 2000 px de largura, para os quadros. Formato WebP; não foram alterados os originais no volume externo. Não foram criados elementos, removidos objetos ou retocadas pinturas. O enquadramento integral foi preservado nas exportações.

Na abertura, o texto fica ao lado da comida em desktop e abaixo da fotografia no telemóvel. A fotografia principal não recebe recorte de preenchimento. Na galeria, a imagem integral usa `object-fit: contain`, incluindo a moldura e o contexto original. Outras fotografias de ambiente podem adaptar-se ao espaço disponível no layout.

O inventário técnico em `fixtures/photo-selection.json` associa IDs, caminhos originais, hashes SHA-256 e variantes geradas. Não colocar este inventário na pasta pública: contém caminhos locais. O site usa apenas caminhos `/assets/photos/...` e funciona sem o volume externo ligado.

## Integração e revisão

O modelo v1 em `fixtures/preview.json` contém a seleção para revisão local. `artist` e `artistId` permanecem null porque a autoria é desconhecida; o Gemini deverá exigir ou resolver essa associação antes de admitir as obras no catálogo público, consoante o validador final. Não criar um artista fictício para passar validações.

A cópia da pasta `frontend/public/`, já prevista na integração, inclui as imagens. O build normal não requer Pillow, HEIC ou acesso ao volume Aydan. A exportação foi feita com ferramentas locais de imagem, separadamente da geração de HTML.

Verificação: renderer e sintaxe aprovados; todos os recursos referenciados existem; galeria abre e muda de obra, Escape fecha e devolve o foco; início, casa e galeria verificados a 320/390/768/1024/1440 px sem overflow horizontal. Ainda é necessária a revisão editorial pelo restaurante antes da publicação.

### Verificação de cor

O perfil Display P3 foi preservado nas três imagens provenientes das cópias HEIC locais. Na releitura dos JPG para verificação adicional de ICC, o volume externo deixou de responder, tanto dentro como fora do ambiente restrito. A primeira exportação e os hashes já estavam concluídos. As sete imagens JPG mantêm-se na preview; rever os perfis a partir dos originais antes da publicação, especialmente nas pinturas. Não foi aplicado um filtro ou uma correção criativa de cor. Essa pendência está registada por imagem no inventário.
