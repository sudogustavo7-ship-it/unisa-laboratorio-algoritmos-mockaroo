# TaskFlow — Gerenciador de tarefas web

**Projeto Integrador: Programação WEB — Universidade Santo Amaro (UNISA), 2026.**

## Objetivo
Desenvolver um protótipo web funcional para organizar atividades pessoais e acadêmicas, com interface responsiva, operações de cadastro, consulta, atualização e exclusão (CRUD), filtros de pesquisa e persistência local.

## Execução
1. Baixe o arquivo [index.html](index.html).
2. Abra-o no Google Chrome, Microsoft Edge ou Firefox.
3. A aplicação iniciará com seis tarefas demonstrativas. Os dados são exemplos fictícios.
4. Clique em **Nova tarefa** para cadastrar uma atividade.
5. Para testar salvamento, edite uma tarefa e atualize a página.

**Não exige servidor, instalação nem dependências externas.** O arquivo possui HTML, CSS e JavaScript. Cada navegador/ambiente mantém seus próprios dados.

## Funcionalidades
- Criar tarefa com título, descrição, prioridade, prazo e status;
- Listar, pesquisar e ordenar tarefas;
- Filtrar por situação (todas, pendentes, em andamento, concluídas);
- Editar, concluir/reabrir e excluir;
- Visualizar contadores e taxa de conclusão;
- Reconhecer tarefas atrasadas;
- Persistência com \`localStorage\`;
- Exportar/importar backup JSON com verificação de esquema e confirmação;
- Restaurar dados fictícios de demonstração;
- Layout responsivo e navegação por teclado.

## Tecnologias e arquitetura
- **HTML5:** estrutura semântica, formulários e elementos de interface;
- **CSS3:** Grid, Flexbox, responsividade e estados de foco;
- **JavaScript (ES2017+):** eventos, validação, gerenciamento do estado e manipulação segura do DOM;
- **Web Storage API:** persistência no navegador sem servidor.

**Limitação intencional:** não há login, backend, sincronização multiusuário ou banco de dados remoto. \`localStorage\` não substitui um banco corporativo e pode ser limpo pelo navegador. A importação/exportação JSON permite cópias locais de segurança.

## Testes sugeridos
Consulte [TESTES.md](TESTES.md). Os testes manuais contemplam CRUD, busca, filtros, persistência, backup, validação e responsividade.

## Autoria
Documento acadêmico destinado à turma do Projeto Integrador da UNISA. Confirmar com os integrantes o rol exato de autores e professor orientador antes da submissão.

## Organização
- \`index.html\`: aplicação integral, sem dependências;
- \`README.md\`: instruções de execução e escopo;
- \`TESTES.md\`: roteiro para validação e registro de evidências.

## Bibliografia técnica
- Mozilla Developer Network. [Web Storage API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API).
- Mozilla Developer Network. [Constraint validation](https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Constraint_validation).
- W3C. [WCAG 2.2](https://www.w3.org/TR/WCAG22/).
- OWASP. [Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html).

**Observação:** o artigo/relatório em PDF compõe a entrega acadêmica, além deste código-fonte.