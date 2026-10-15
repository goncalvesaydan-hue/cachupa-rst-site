# Contrato de dados e integração — v1

**Coordenação:** Orca. **Produtor:** Gemini/backend. **Consumidor:** Codex/frontend. O nome api-contract.md segue a organização do projeto; nenhuma API HTTP está implementada ou exigida nesta fase.

**Estado:** especificação inicial para implementação pelos dois agentes. Não é uma API existente nem um esquema já validado por código.

## 1. Fronteira de integração

O backend lê fontes editoriais, valida e normaliza um modelo de conteúdo. O frontend recebe esse modelo nos templates durante a geração. O resultado é HTML estático servido ao visitante.

```text
content/ → backend: normalizar e validar → modelo v1
                                                ↓
frontend/src/templates/ + frontend/public/ → geração → saída pública
```

Não são necessárias chamadas HTTP para obter o conteúdo em tempo de visita. A galeria pode receber um pequeno JSON público para as interações, mas o conteúdo principal deve estar no HTML.

## 2. Convenções

- UTF-8; idioma inicial `pt-PT`.
- `schemaVersion` é `1`.
- Campos desconhecidos são `null`; coleções sem itens são `[]`.
- Não usar textos como “a confirmar” no lugar de números, URLs ou identificadores.
- IDs são strings estáveis; títulos podem mudar sem alterar o ID.
- Campos de texto são texto simples, sem HTML. O renderizador deve escapá-los.
- URLs públicas de recursos são relativas à raiz, por exemplo `/assets/images/obra-01-800.webp`.
- Caminhos privados do computador não entram no modelo público.
- Dados de demonstração só podem existir em pré-visualização claramente identificada.

## 3. Modelo público

| Campo | Tipo | Regra |
|---|---|---|
| `schemaVersion` | inteiro | `1` |
| `preview` | booleano | Controla identificação da pré-visualização e indexação |
| `site` | objeto | `name`, `locale`, `baseUrl` |
| `restaurant` | objeto | `city`, `address`, `hours`, `contacts` |
| `pages` | objeto | Conteúdo editorial por chave de página |
| `artist` | objeto ou null | `id`, `name`, `bio`, `portrait`, `website` |
| `artworks` | lista | Apenas obras publicadas no modelo público |
| `images` | objeto | Imagens indexadas por ID |
| `navigation` | objeto | `menuEnabled`; falso nesta fase pública |

`site.baseUrl` é `null` antes de existir domínio. `site.locale` é `pt-PT`. O endereço é texto confirmado ou `null`.

### Contactos

`restaurant.contacts` contém:

- `phoneDisplay`: telefone legível ou `null`.
- `phoneHref`: `tel:` validado ou `null`.
- `whatsappDisplay`: número legível ou `null`.
- `whatsappHref`: ligação HTTPS `wa.me` com mensagem codificada ou `null`.
- `emailDisplay`: email validado ou `null`.
- `emailHref`: ligação `mailto:` com assunto codificado ou `null`.
- `directionsHref`: ligação HTTPS confirmada ou `null`.
- `socialLinks`: lista de `{label, href}` com URLs HTTPS confirmadas.

A fonte privada de conteúdo pode ter `whatsappNumber` e `whatsappMessage` separados. O backend constrói as ligações públicas; o frontend não as recompõe em cada componente. A cópia de email usa `emailDisplay`.

### Horários

Lista de objetos `{day, closed, intervals, note}`:

- `day`: inteiro de 1 (segunda-feira) a 7 (domingo).
- `closed`: booleano.
- `intervals`: lista de `{opens, closes, closesNextDay}`; horas `HH:MM`.
- `closesNextDay`: booleano explícito para períodos que ultrapassam meia-noite.
- `note`: texto opcional ou `null`.

Lista vazia significa horários desconhecidos. Um dia fechado tem intervalos vazios. Não implementar “Aberto agora” nesta fase.

### Conteúdo das páginas

Chaves: `home`, `house`, `gallery`, `reservations`, `contacts`, `privacy`, `notFound`.

Cada página tem `{title, description, heading, intro, heroImageId, sections}`. Texto opcional é `null`. `sections` é uma lista ordenada de:

```json
{
  "id": "identificador-estavel",
  "type": "editorial",
  "heading": null,
  "paragraphs": [],
  "imageIds": [],
  "links": []
}
```

Tipos iniciais de secção: `editorial`, `photoGrid`, `artworkSelection`, `visit`. Cada ligação é `{label, href}` com destino validado. A escolha do layout é do frontend, não do conteúdo. Uma secção `artworkSelection` usa `artworkIds` como lista adicional. Tipos novos exigem atualização conjunta do contrato. Secções sem conteúdo não devem produzir blocos vazios na produção.

### Imagens

Cada entrada em `images` tem:

`{id, src, width, height, alt, caption, credit, variants, mobileImageId, focalPoint}`.

- `width` e `height`: inteiros positivos, dimensões intrínsecas de `src`.
- `variants`: lista de `{src, width, height, mimeType}`.
- `mobileImageId`: referência a outro recurso ou `null`.
- `focalPoint`: `{x, y}`, valores entre 0 e 1, ou `null`.
- `alt`: texto; vazio apenas para imagens decorativas.
- `caption` e `credit`: texto ou `null`.

O frontend escolhe composição e recortes dos pratos/espaço. O backend gera os derivados solicitados e não altera os originais. Pinturas usam a imagem completa e não usam recorte por ponto focal.

### Obras

Cada obra tem:

`{id, artistId, title, year, technique, dimensions, description, imageId, fullImageId, order, featured}`.

- `title`: obrigatório para publicação; não atribuir “Sem título” sem confirmação do artista.
- `year`: texto confirmado ou `null`, permitindo datas aproximadas fornecidas pelo artista.
- `dimensions`: texto confirmado com unidade ou `null`.
- `technique` e `description`: texto autorizado ou `null`.
- `imageId` e `fullImageId`: referências válidas ao manifesto de imagens.
- `order`: inteiro; `featured`: booleano.

O estado `published` existe na fonte de conteúdo; o backend remove rascunhos antes de gerar o modelo público. Não enviar rascunhos ao navegador para apenas os esconder com CSS.

## 4. Rotas estáveis

`/`, `/a-nossa-casa/`, `/galeria/`, `/reservas/`, `/contactos/`, `/privacidade/` e `/404.html`.

`/menu/` é reservado ao módulo existente, fora do desenvolvimento atual. A configuração de produção deve impedir a exposição involuntária da demonstração.

## 5. Validação por ambiente

**Pré-visualização:** permitir contactos e imagens em falta; emitir avisos identificáveis e usar estados honestos. Não fabricar valores para satisfazer o esquema.

**Produção:** falhar com mensagem clara se faltarem WhatsApp, email, morada, cidade, horários, metadados essenciais ou imagens referenciadas. Validar que não há rascunhos nem catálogo de demonstração exposto. A publicação da galeria requer identificação e materiais aprovados do artista; se ainda não existirem, decidir explicitamente com o utilizador o adiamento dessa página.

Erros do validador incluem caminho do campo e motivo, por exemplo: `restaurant.contacts.emailDisplay: email obrigatório para produção`.

## 6. Alterações ao contrato

- Codex e Gemini podem propor mudanças; a Orca é a editora e integradora do contrato, após rever o impacto nos dois lados.
- Campos opcionais novos podem manter a versão 1 se os consumidores anteriores continuarem válidos.
- Renomear, remover ou mudar tipos exige nova versão e migração coordenada.
- Cada entrega declara a versão usada e fornece dados de exemplo compatíveis.
- Fixtures não substituem dados reais e não devem ser publicadas como conteúdo do restaurante.

## 7. Comandos de integração a implementar

A interface exata será entregue pelo backend no README. Deve oferecer: validação, geração com diretório de saída explícito e modo preview/produção. Não assumir que esses comandos já existem.

A Orca coordena os comandos partilhados. O comando atual `python3 scripts/build.py` escreve diretamente na pasta do site. Até à migração, não o executar em paralelo com outro agente no mesmo checkout. Usar checkout isolado ou atribuir a geração a um único integrador.
