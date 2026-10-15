# Agente frontend — Codex

## Missão

Construir a experiência visual do Cachupa Rst conforme `00-REGRAS/ESTRUTURA-DO-SITE.md`: fotografia real, identidade cabo-verdiana, páginas institucionais e galeria. Reservas por ligação WhatsApp; contacto por email. O menu fica adiado.

## Ler antes de começar

1. `00-REGRAS/REGRAS-DOS-AGENTES.md`.
2. `00-REGRAS/ESTRUTURA-DO-SITE.md`.
3. `00-REGRAS/CONTRATO-DE-DADOS.md`.
4. Este documento e o estado de entrega mais recente do backend, se existir.

## Ficheiros sob tua responsabilidade

- `frontend/`: templates, componentes, estilos, JavaScript e testes de interface.
- `frontend/public/`: logo, fontes e recursos estáticos próprios da interface.
- `frontend/fixtures/`: conteúdo de exemplo compatível com o contrato, sem dados inventados apresentados como reais.
- `visuals/`: capturas de revisão.
- `00-REGRAS/STATUS-FRONTEND.md`: registo da tua entrega.

Enquanto não ocorrer a separação, `assets/site.css` e `assets/site.js` pertencem ao frontend. Não alterar HTML gerado à mão nem executar o gerador antigo no checkout partilhado.

## Entregas

- Páginas Início, A nossa casa, Galeria, Reservas, Contactos, Privacidade e 404.
- Cabeçalho e rodapé partilhados, navegação mobile e ações de contacto.
- Layout fotográfico, recortes adequados e apresentação integral dos quadros.
- Detalhe acessível das obras e navegação entre elas.
- Metadados e estrutura semântica nos templates.
- Estados de preparação, ausência de conteúdo e falha de imagem.
- Verificação de teclado, contraste, mobile e links.

## Dependências do backend

Consumir o modelo descrito no contrato. Trabalhar primeiro com fixtures; não esperar por um serviço remoto. Usar links já preparados no modelo e tratar `null` explicitamente. Nunca apresentar uma reserva como confirmada.

Não criar APIs, credenciais, base de dados ou uma segunda fonte de contactos. Não alterar campos do contrato unilateralmente. Não editar `backend/`, `content/` nem a configuração de publicação.

## Primeira fase

Preparar os templates em `frontend/templates/`, retirando a apresentação de `scripts/build.py` em coordenação com o agente backend. O backend é o único editor desse script antigo. Indicar-lhe os blocos a extrair ou trabalhar a partir de uma cópia lida, sem alterar a origem.

## Conclusão da entrega

Atualizar o teu ficheiro de estado com: ficheiros alterados, versão do contrato, verificações executadas, limitações, imagens/dados em falta e dependências da integração. Não declarar funcionalidades de backend como concluídas sem evidência.
