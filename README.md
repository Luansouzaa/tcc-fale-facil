Teste 01

Ação: Cadastrar novo feedback com campos preenchidos
Resultado esperado: Feedback cadastrado com sucesso
Resultado obtido: Erro na página — campo prioridade com acento (Média) causou conflito com o MySQL
Solução: Removidos os acentos dos valores ENUM no banco de dados


Teste 02

Ação: Fazer login com email e senha corretos
Resultado esperado: Usuário redirecionado para o dashboard
Resultado obtido: Login realizado com sucesso
Status: ✅ Aprovado


Teste 03

Ação: Fazer login com email ou senha incorretos
Resultado esperado: Mensagem de erro informando credenciais inválidas
Resultado obtido: Mensagem de erro exibida corretamente
Status: ✅ Aprovado


Teste 04

Ação: Funcionário tenta acessar feedback de outro usuário
Resultado esperado: Acesso negado com mensagem de erro
Resultado obtido: Sistema bloqueou o acesso corretamente
Status: ✅ Aprovado


Teste 05

Ação: Enviar feedback marcando a opção anônimo
Resultado esperado: Feedback salvo sem nome e departamento visíveis
Resultado obtido: Feedback salvo como "Anonimo / Nao informado" com badge de anonimato
Status: ✅ Aprovado


Teste 06

Ação: Administrador altera o status de um feedback no dashboard
Resultado esperado: Status atualizado sem recarregar a página
Resultado obtido: Status atualizado via AJAX com sucesso
Status: ✅ Aprovado


Teste 07

Ação: Rodar o sistema com senha incorreta no app.py
Resultado esperado: Erro de conexão com o banco
Resultado obtido: Erro Access denied for user root@localhost exibido
Solução: Corrigida a senha no DB_CONFIG do app.py
Status: ✅ Resolvido


Teste 08

Ação: Acessar o sistema pelo celular via IP local
Resultado esperado: Interface adaptada para tela pequena
Resultado obtido: Layout responsivo funcionando corretamente
Status: ✅ Aprovado


Teste 09

Ação: Administrador tenta enviar um feedback
Resultado esperado: Acesso bloqueado com mensagem informativa
Resultado obtido: Sistema bloqueou e redirecionou para o dashboard
Status: ✅ Aprovado


Teste 10

Ação: Funcionário tenta editar um feedback
Resultado esperado: Opção de edição não disponível
Resultado obtido: Botão de editar removido e rota bloqueada
Status: ✅ Aprovado


Teste 11

Ação: Tentar excluir um feedback como admin ou funcionário
Resultado esperado: Opção de exclusão não disponível para nenhum perfil
Resultado obtido: Botão de excluir não existe no sistema
Status: ✅ Aprovado


Teste 12

Ação: Rodar o sistema em computador sem Flask instalado
Resultado esperado: Erro ModuleNotFoundError: No module named 'flask'
Resultado obtido: Erro exibido conforme esperado
Solução: Executado pip install flask mysql-connector-python
Status: ✅ Resolvido


Teste 13

Ação: Acessar o sistema sem banco de dados criado
Resultado esperado: Erro de banco não encontrado
Resultado obtido: Erro Unknown database 'fale_facil_db' exibido
Solução: Banco criado via MySQL Workbench com o script SQL
Status: ✅ Resolvido
