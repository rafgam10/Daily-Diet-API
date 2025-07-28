
## 🥗 Projeto PRF – API de Registro de Refeições

Esta é uma API RESTful construída com Flask que permite gerenciar **usuários** e suas **refeições**, com autenticação de login/logout e controle de dieta.

---

### 🧱 Tecnologias Utilizadas

* Python 3
* Flask
* Flask-Login
* SQLAlchemy
* MySQL (ou outro SGBD via `SQLALCHEMY_DATABASE_URI`)
* Python-dotenv
* Postman (para testes)

---

## 📦 Instalação

1. **Clone o projeto:**

```bash
git clone https://github.com/seuusuario/nome-do-repo.git
cd nome-do-repo
```

2. **Crie um ambiente virtual:**

```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
```

3. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

4. **Crie o arquivo `.env`:**

```env
API_KEY=chave_secreta_para_flask
DATABASE_URL=mysql+pymysql://usuario:senha@localhost/nome_do_banco
```

---

## 🚀 Execução

```bash
flask run
# ou
python app.py
```

---

## 📚 Endpoints da API

---

### 👤 Usuários

#### 🔸 Criar Usuário

```http
POST /user
```

**Body JSON:**

```json
{
  "nome": "João",
  "email": "joao@email.com",
  "senha": "123456",
  "criando_em": "28/07/2025"
}
```

---

#### 🔸 Buscar Usuário por ID

```http
GET /user/1
```

---

#### 🔸 Listar Todos os Usuários

```http
GET /user
```

---

#### 🔸 Atualizar Senha de um Usuário

```http
PUT /user/1
```

**Body JSON:**

```json
{
  "senha": "nova_senha_segura"
}
```

---

#### 🔸 Deletar Usuário

```http
DELETE /user/1
```

---

### 🍽️ Refeições

#### 🔸 Criar Refeição para Usuário

```http
POST /user/1/refeicoes
```

**Body JSON:**

```json
{
  "nome": "Café da manhã",
  "data_hora": "28/07/2025 - 08:00",
  "dentro_dieta": true,
  "criado_em": "28/07/2025"
}
```

---

#### 🔸 Listar Refeições do Usuário

```http
GET /user/1/refeicoes
```

---

#### 🔸 Listar Refeições por Data

```http
GET /user/1/refeicoes?data=28/07/2025
```

---

#### 🔸 Atualizar Nome da Refeição

```http
PUT /user/1/refeicoes/2
```

**Body JSON:**

```json
{
  "novo_nome": "Lanche da tarde"
}
```

---

#### 🔸 Deletar Refeição

```http
DELETE /user/1/refeicoes/2
```

---

### 🔐 Autenticação

#### 🔸 Login

```http
POST /login
```

**Body JSON:**

```json
{
  "email": "joao@email.com",
  "senha": "123456"
}
```

---

#### 🔸 Logout

```http
GET /logout
```

---

## 🛠️ Estrutura do Projeto

```
.
├── app.py
├── models/
│   ├── usuarios.py
│   └── refeicoes.py
├── database.py
├── .env
└── README.md
```

---

## 🧪 Testando com Postman

1. Crie uma Collection chamada `Refeições API`.
2. Configure os métodos conforme os exemplos acima.
3. Use o ambiente com variável `{{base_url}}` apontando para `http://localhost:5000`.

---

## ⚠️ Observações

* Datas devem seguir os formatos:

  * `data_hora`: `DD/MM/YYYY - HH:MM`
  * `criando_em`: `DD/MM/YYYY`
* Certifique-se de que o banco está rodando e a URL no `.env` está correta.
* O campo `usuario_id` é gerado automaticamente pelo relacionamento entre usuários e refeições.

---

## 📄 Licença

Este projeto está sob a licença MIT.


