# Fale Fácil — Sistema de Feedbacks Corporativo

Sistema web para cadastro e gerenciamento de feedbacks de funcionários, desenvolvido como Trabalho de Conclusão de Curso (TCC).

---

## Tecnologias Utilizadas

- **Backend:** Python 3 + Flask
- **Banco de Dados:** MySQL
- **Frontend:** HTML5, CSS3, JavaScript
- **Controle de Versão:** Git + GitHub

---

## Funcionalidades

- Autenticação com dois perfis: **Administrador** e **Funcionário**
- Funcionário visualiza e edita apenas os próprios feedbacks
- Administrador visualiza e gerencia todos os feedbacks
- Opção de envio de feedback **anônimo**
- Nenhum usuário pode excluir feedbacks
- Apenas o administrador pode alterar o **status** dos feedbacks
- Interface responsiva para uso em **dispositivos móveis**
- Acesso via **QR Code** na portaria da empresa

---

## Estrutura do Projeto

```
fale_facil/
├── app.py                  <- Backend Flask (rotas, login, banco)
├── database.sql            <- Script de criação do banco de dados
├── requirements.txt        <- Dependências Python
├── static/
│   ├── css/
│   │   └── style.css       <- Estilos da interface
│   └── js/
│       └── main.js         <- JavaScript (AJAX, toasts)
└── templates/
    ├── base.html           <- Template base
    ├── login.html          <- Tela de login
    ├── index.html          <- Dashboard
    ├── form.html           <- Cadastro e edição de feedback
    ├── detalhe.html        <- Visualização completa
    ├── usuarios.html       <- Lista de usuários (admin)
    └── form_usuario.html   <- Cadastro de usuário (admin)
```

---

## Como Rodar Localmente

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Criar o banco de dados
```bash
mysql -u root -p
```
```sql
source /caminho/para/fale_facil/database.sql
exit
```

### 3. Configurar a senha no app.py
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'SUA_SENHA_AQUI',
    'database': 'fale_facil_db',
}
```

### 4. Iniciar o servidor
```bash
python app.py
```

Acesse: http://localhost:5000

---

## Usuários Padrão

| Perfil       | Email                  | Senha     |
|--------------|------------------------|-----------|
| Administrador| admin@empresa.com      | admin123  |
| Funcionário  | joao@empresa.com       | func123   |

---

## Testes Realizados

### Teste 01 — Cadastrar novo feedback
- **Descrição:** Preencher o formulário e cadastrar um feedback
- **Resultado esperado:** Feedback cadastrado com sucesso
- **Resultado obtido:** Erro na página — campo `prioridade` com acento (`Média`) causou conflito com o MySQL
- **Solução:** Removidos os acentos dos valores ENUM no banco de dados

---

### Teste 02 — Login com credenciais incorretas
- **Descrição:** Tentar fazer login com email ou senha errados
- **Resultado esperado:** Mensagem de erro informando credenciais inválidas
- **Resultado obtido:** Mensagem de erro exibida corretamente
- **Status:** ✅ Aprovado

---

### Teste 03 — Acesso de funcionário a feedback de outro usuário
- **Descrição:** Funcionário tenta editar feedback de outro funcionário
- **Resultado esperado:** Acesso negado com mensagem de erro
- **Resultado obtido:** Sistema bloqueou o acesso corretamente
- **Status:** ✅ Aprovado

---

### Teste 04 — Feedback anônimo
- **Descrição:** Marcar a opção anônimo e enviar feedback
- **Resultado esperado:** Feedback salvo sem nome e departamento
- **Resultado obtido:** Feedback salvo como "Anonimo / Nao informado" e exibido com badge de anonimato
- **Status:** ✅ Aprovado

---

### Teste 05 — Atualização de status pelo administrador
- **Descrição:** Admin altera o status de um feedback no dashboard
- **Resultado esperado:** Status atualizado sem recarregar a página
- **Resultado obtido:** Status atualizado via AJAX com sucesso
- **Status:** ✅ Aprovado

---

### Teste 06 — Conexão com banco de dados
- **Descrição:** Rodar o sistema com senha incorreta no app.py
- **Resultado esperado:** Erro de conexão
- **Resultado obtido:** Erro `Access denied for user root@localhost` exibido
- **Solução:** Corrigida a senha no DB_CONFIG do app.py
- **Status:** ✅ Resolvido

---

### Teste 07 — Responsividade mobile
- **Descrição:** Acessar o sistema pelo celular via IP local
- **Resultado esperado:** Interface adaptada para tela pequena
- **Resultado obtido:** Layout responsivo funcionando corretamente
- **Status:** ✅ Aprovado

---

## Licença

Projeto desenvolvido para fins acadêmicos — TCC.
