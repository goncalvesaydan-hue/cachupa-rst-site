# Cachupa Rst — Site

Site visual de um restaurante cabo-verdiano dedicado à cachupa, com galeria de um pintor cabo-verdiano. **Orca coordena; Codex implementa o frontend; Gemini implementa o backend.**

## Começar aqui

1. [AGENTS.md](AGENTS.md): regras comuns e propriedade dos ficheiros.
2. [Guia de coordenação da Orca](docs/orca-briefing.md): contexto, estado real e próximos passos.
3. [Arquitetura](docs/architecture.md) e [contrato](docs/api-contract.md).
4. [Workflow](docs/workflow.md), [padrões](docs/coding-standards.md) e [testes](docs/testing.md).
5. Briefing da função: [frontend](docs/frontend-rules.md) ou [backend](docs/backend-rules.md).
6. [Especificação do site](docs/site-specification.md): páginas, UX/UI, fotografia e conteúdo.

## Estado real

Existe uma pré-visualização estática funcional na raiz, com HTML/CSS/JavaScript e gerador Python. As pastas `frontend/` e `backend/` são a estrutura de destino; ainda não contêm a aplicação migrada. Os `package.json` são manifestos privados sem dependências ou scripts: não indicam uma aplicação Node implementada.

A nova organização foi preparada, não houve migração automática da aplicação nem criação de serviços. `backend/prisma/` está reservado e vazio; não há Prisma instalado, esquema, autenticação ou multitenancy implementados.

## Âmbito confirmado

- Site predominantemente fotográfico; existem imagens reais, pasta ainda a partilhar.
- Páginas Início, A nossa casa, Galeria, Reservas, Contactos, Privacidade e 404.
- Reservas por link WhatsApp; contacto por mailto. Sem envio automático ou confirmação de reserva no site.
- Menu e SaaS adiados; preservar `menu/` e o original independente.
- Galeria de exposição; venda de obras não confirmada.

## Pré-visualização atual — legado

```sh
python3 -m http.server 18951 --bind 127.0.0.1
```

Abrir http://127.0.0.1:18951/ . Não abrir os HTML por `file://`.

`python3 scripts/build.py` regenera as páginas na raiz e pode sobrescrever HTML. Só executar na cópia isolada ou quando a Orca reservar a geração. A saída isolada é uma das primeiras tarefas do Gemini.

## Preparação e verificação

```sh
bash scripts/setup.sh
bash scripts/lint-all.sh
bash scripts/test-all.sh
```

Os scripts não instalam dependências, não criam `.env` e não publicam. `test-all.sh` devolve código 2 enquanto faltarem suites dos módulos: isso é pendência, não sucesso. Ver [testing.md](docs/testing.md).

## Diretórios

`docs/`: documentação canónica e decisões. `frontend/`: Codex. `backend/`: Gemini. `scripts/`: coordenação e scripts partilhados. `content/`, `assets/` e páginas HTML na raiz: base legada em transição. `menu/`: preservado. `documentation/archive/`: histórico, sem autoridade sobre o âmbito atual.

Não apagar os diretórios legados antes de a Orca validar a migração. Publicação de produção ainda pendente de conteúdo, contactos, imagens, domínio e alojamento.
