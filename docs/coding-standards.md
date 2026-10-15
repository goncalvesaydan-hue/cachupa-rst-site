# Padrões de código

## Comuns

- UTF-8; interface em português de Portugal; identificadores técnicos consistentes em inglês.
- Funções e módulos pequenos com responsabilidades claras; evitar infraestrutura sem requisito.
- Não introduzir framework ou dependência apenas para satisfazer o nome de uma pasta.
- Dados num único local; nada de contactos repetidos em templates.
- Não versionar credenciais nem alterar originais de imagens.
- Não aplicar formatação global aos ficheiros do outro agente.
- Explicar decisões não óbvias; evitar comentários que apenas repetem o código.

## Frontend

HTML semântico, foco visível, interações por teclado e estados honestos. CSS com classes previsíveis e especificidade controlada; usar tokens da marca. JavaScript melhora a experiência, mas links principais funcionam sem ele. Evitar HTML não escapado, inline handlers e conteúdo remoto não validado. Respeitar movimento reduzido. Não recortar pinturas. Não inventar conteúdo para completar cartões.

## Backend

Validar na fronteira de dados; erros com campo e motivo. Escapar texto no renderizador. Rejeitar URLs de esquemas inesperados e caminhos que saiam das pastas autorizadas. Builds determinísticos, saída explícita e sem escrita fora do destino. Não eliminar saídas arbitrárias por parâmetro sem validação. Não expor rascunhos, originais ou caminhos privados. Mensagens e assuntos de links devidamente codificados.

## Convenções de entrega

Scripts documentados e com códigos de saída úteis. Manifestos e lockfiles pertencem ao módulo respetivo. Alterações partilhadas coordenadas pela Orca. Testes devem provar comportamento relevante, sem espelhar cada linha de implementação.
