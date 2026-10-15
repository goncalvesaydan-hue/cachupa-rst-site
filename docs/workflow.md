# Workflow — Orca, Codex e Gemini

## Ciclo de trabalho

1. Orca abre uma tarefa com objetivo, âmbito, dono, caminhos permitidos, dependências, versão do contrato e critérios de aceitação.
2. Agente lê contexto e confirma os pressupostos no seu handoff.
3. Agente implementa no seu módulo e testa a alteração.
4. Agente entrega resumo, ficheiros, comandos, resultados e limitações.
5. Orca revê contrato e conflitos, integra numa saída isolada e valida ponta a ponta.
6. Orca regista o estado e atribui a tarefa seguinte.

Não iniciar automaticamente novos chats, enviar mensagens externas ou executar o trabalho de outro agente a partir destes documentos. A coordenação pode usar ficheiros de handoff ou o canal que o utilizador disponibilizar.

## Modelo de tarefa

```text
ID / objetivo:
Responsável: Codex ou Gemini
Caminhos permitidos:
Contrato e decisões aplicáveis:
Dependências:
Critérios de aceitação:
Testes esperados:
Limites e exclusões:
```

## Ambientes

Preferir checkouts/worktrees separados, após confirmar um repositório específico do projeto. Não criar ramos no repositório pessoal por engano. Ramos sugeridos: `codex/site-frontend`, `gemini/site-backend`, `orca/site-integration`.

No mesmo checkout: sem troca de ramo, reset, stash, clean ou operações globais enquanto outro agente trabalha. Orca reserva ficheiros partilhados. Builds usam saídas distintas. Portas sugeridas 18952 (frontend), 18953 (backend, se necessário) e 18951 (integrado), verificando disponibilidade. Não terminar processos alheios.

## Contratos e decisões

Mudança necessária → proposta no handoff → Orca consulta impacto nos dois lados → atualiza contrato/ADR → agentes implementam → validação conjunta. Mudanças incompatíveis não podem ser publicadas primeiro de um só lado.

Não basta alterar o documento: atualizar fixtures, validadores e consumidores afetados. A Orca confirma que não há instruções antigas em conflito.

## Entrega

Usar `docs/handoffs/frontend.md` e `docs/handoffs/backend.md`, um editor por ficheiro. Incluir data, tarefa, versão do contrato, alterações, resultados reais de testes, dados em falta e próximos passos. Orca usa `docs/handoffs/orca.md` para decisões e integração.

Estados: preparado, em curso, pronto para revisão, integrado, pendente de dados. “Integrado” exige validação conjunta. “Publicado” exige deploy verificado e instrução do utilizador.

## Proteção de trabalho

Não corrigir um conflito aceitando tudo de um lado sem inspeção. Não remover código para fazer testes passar. Não misturar refatoração ampla com entrega pequena. Manter entregas recuperáveis e explicar migrações.
