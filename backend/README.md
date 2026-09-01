# Backend - Contagem RIO (FastAPI + Supabase)

API em Python (FastAPI) para o sistema de gestão de cultos da Igreja RIO, com banco de dados no Supabase (PostgreSQL) e deploy na Vercel.

## Estrutura

```
backend/
├── api/
│   └── index.py            # Entrypoint da Vercel (reexporta o app)
├── app/
│   ├── main.py             # App FastAPI + CORS + rotas
│   ├── config.py           # Configuração (variáveis de ambiente)
│   ├── database.py         # Cliente Supabase
│   ├── security.py         # Hash de senha (bcrypt) + JWT
│   ├── dependencies.py     # Autenticação e permissões
│   ├── models.py           # Models Pydantic
│   └── routers/
│       ├── auth.py         # POST /auth/login
│       ├── usuarios.py     # CRUD /usuarios (admin)
│       ├── igrejas.py      # CRUD /igrejas
│       └── contagens.py    # POST/GET /contagens
├── schema.sql              # SQL para criar as tabelas no Supabase
├── seed_admin.py           # Cria o usuário admin padrão
├── requirements.txt
├── vercel.json             # Configuração de deploy na Vercel
└── .env.example
```

## Passo a passo

### 1. Criar conta e projeto no Supabase

1. Acesse https://supabase.com e crie uma conta (gratuita).
2. Crie um novo projeto (escolha uma senha para o banco e guarde).
3. Vá em **SQL Editor > New Query**, cole o conteúdo de `schema.sql` e clique em **Run**.
   Isso cria as tabelas e cadastra as igrejas padrão.
4. Vá em **Project Settings > API** e copie:
   - **Project URL** → será o `SUPABASE_URL`
   - **service_role key** (em Project API keys) → será o `SUPABASE_KEY`

> A `service_role key` é secreta. Nunca coloque no frontend nem no Git.

### 2. Configurar o ambiente local

```bash
cd backend

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate   # No Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis
cp .env.example .env
# Edite o .env e preencha SUPABASE_URL, SUPABASE_KEY e JWT_SECRET
```

Para gerar uma `JWT_SECRET` segura:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Criar o usuário admin

```bash
python seed_admin.py
```

Isso cria o login `admin` com senha `admin`.

### 4. Rodar localmente

```bash
uvicorn app.main:app --reload --port 8000
```

Acesse:
- API: http://localhost:8000
- Documentação interativa (Swagger): http://localhost:8000/docs

### 5. Deploy na Vercel

1. Instale a CLI da Vercel: `npm i -g vercel`
2. Na pasta `backend`, rode: `vercel`
3. Configure as variáveis de ambiente no painel da Vercel
   (**Project Settings > Environment Variables**): `SUPABASE_URL`, `SUPABASE_KEY`,
   `JWT_SECRET`, `CORS_ORIGINS` (com a URL do seu frontend).
4. Rode `vercel --prod` para publicar.

## Endpoints principais

| Método | Rota | Acesso | Descrição |
|---|---|---|---|
| POST | `/auth/login` | Público | Login, retorna token JWT |
| GET | `/usuarios` | Admin | Lista usuários |
| POST | `/usuarios` | Admin | Cria usuário |
| PUT | `/usuarios/{id}` | Admin | Atualiza usuário |
| DELETE | `/usuarios/{id}` | Admin | Exclui usuário |
| GET | `/igrejas` | Logado | Lista igrejas |
| POST | `/igrejas` | Admin | Cria igreja |
| PUT | `/igrejas/{id}` | Admin | Atualiza igreja |
| DELETE | `/igrejas/{id}` | Admin | Exclui igreja |
| POST | `/contagens` | Logado | Salva contagem |
| GET | `/contagens` | Logado | Lista contagens (filtra por igreja/perfil) |
| GET | `/contagens/{id}` | Logado | Detalha uma contagem |

## Segurança

- Senhas são armazenadas com **hash bcrypt** (nunca em texto puro).
- Autenticação via **token JWT** enviado no header `Authorization: Bearer <token>`.
- **Regra de igreja aplicada no servidor**: servos e líderes só acessam dados da própria
  igreja, independentemente do que o frontend enviar.
- Apenas admin gerencia usuários e igrejas.
