# Roteiro de testes funcionais — TaskFlow

Os dados iniciais são ilustrativos. Não editar o código para a execução dos cenários abaixo.

| Código | Cenário | Procedimento | Resultado esperado |
|---|---|---|---|
| T01 | Carregamento | Abrir index.html | Exibir painel e seis tarefas de exemplo |
| T02 | Cadastro | Clicar em Nova tarefa, preencher título e salvar | Nova tarefa aparece na lista e total incrementa |
| T03 | Validação | Tentar salvar título com menos de três caracteres | Formulário impede o salvamento |
| T04 | Edição | Clicar no ícone de editar e alterar o título | Texto atualizado e contadores coerentes |
| T05 | Conclusão | Marcar uma tarefa não concluída | Contador de concluídas e progresso aumentam |
| T06 | Reabertura | Desmarcar uma concluída | Status volta a pendente |
| T07 | Exclusão | Selecionar excluir e confirmar | Item desaparece da lista |
| T08 | Filtros | Alternar Pendentes/Em andamento/Concluídas | Exibir somente tarefas compatíveis |
| T09 | Busca | Pesquisar termo do título ou descrição | Mostrar somente itens que contêm o termo |
| T10 | Ordenação | Alterar o campo de ordenação | Itens mudam conforme critério selecionado |
| T11 | Persistência | Atualizar a página após editar | Alterações permanecem no mesmo navegador |
| T12 | Backup | Exportar JSON e reimportar | Dados recuperados após confirmação |
| T13 | Erro de backup | Importar JSON inválido | Mensagem de erro e tarefas preservadas |
| T14 | Restauração | Clicar em Restaurar exemplo, confirmar | Seis tarefas demonstrativas restauradas |
| T15 | Responsividade | Abrir em viewport de 390px e 1366px | Sem rolagem horizontal indevida; controles acessíveis |
| T16 | Segurança no DOM | Cadastrar título contendo caracteres HTML | Exibição textual, sem execução de marcação ou script |

## Regras de registro
Registrar data, navegador, versão, resultado obtido e observações. Os cenários acima constituem um **plano de testes**; não são evidência de execução automática. Na entrega, documentar somente testes realmente realizados.

## Restrições
- \`localStorage\` pode ser indisponível em alguns ambientes de navegação privativa ou políticas de segurança.
- Os arquivos exportados contêm os textos cadastrados pelo usuário; não incluir informações sensíveis no protótipo.
- Como não há servidor, não há autenticação ou sincronização entre dispositivos.