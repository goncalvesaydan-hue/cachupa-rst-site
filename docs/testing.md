# Estratégia de testes

## Estado atual

Não há suites dos novos módulos implementadas. Os manifestos estão sem scripts. `test-all.sh` sinaliza essa ausência com saída 2; não simula sucesso. `lint-all.sh` verifica sintaxe da base legada e executará `lint` dos módulos quando existir, indicando explicitamente os que faltam. Não substitui revisão ou testes funcionais.

Os nove testes antigos do menu podem ser executados com `node --test menu/tests/menu.test.cjs`, mas não contam como cobertura dos novos módulos. O menu está fora da alteração atual.

## Codex

Verificar navegação por teclado, foco, fecho de painéis, detalhe de obras, campos null, erro de imagem, cópia de email e links externos. Testar 320/390/768/1024/1440 px e texto ampliado. Verificar conteúdo essencial sem JavaScript. Usar dados reais para revisão final de recortes e cor; fixtures não bastam para qualidade visual.

## Gemini

Testar esquema/versão, IDs e referências, URLs, valores ausentes, exclusão de rascunhos, URLs WhatsApp/mailto com caracteres especiais e distinção preview/produção. Testar geração em diretório temporário, sem modificar fontes ou saída alheia. Confirmar que ficheiros privados e originais não entram na publicação.

## Orca

Executar suites dos dois módulos e build conjunto em saída isolada. Inspecionar todas as rotas, imagens, metadados, 404 e links. Verificar que WhatsApp apenas abre mensagem por enviar e que o site não mostra sucesso de reserva. Confirmar ausência de demo pública do menu.

## Comandos

```sh
bash scripts/setup.sh
bash scripts/lint-all.sh
bash scripts/test-all.sh
```

Cada agente adiciona `test` e `lint` ao package do seu módulo quando houver código verificável, podendo chamar Python ou Node conforme a stack. Documentar runtime e dependências; não instalar ferramentas implicitamente nestes scripts.

## Critério de conclusão

Registar comando, resultado, âmbito coberto e pendências. Falha de teste bloqueia a entrega afetada; conteúdo em falta bloqueia publicação, mas não impede entrega técnica limitada e identificada. Não executar ações reais de reserva ou enviar emails como teste.
