# Contagem RIO - Sistema de Gestão de Cultos

Sistema de contagem e análise de dados dos cultos da Igreja RIO (Relevante, Integral e Orgânico).

Composto por um **frontend** (HTML/CSS/JS) e um **backend** (Python/FastAPI) com banco de dados no **Supabase** (PostgreSQL).

## Estrutura do Projeto

```
Contagem/
├── index.html                     ← Ponto de entrada (redireciona ao login)
├── README.md
├── src/
│   ├── css/
│   │   └── global.css             ← Estilos globais (cores, fontes, componentes)
│   ├── pages/
│   │   ├── login.html             ← Login
│   │   ├── home.html              ← Home (estilo Linktree)
│   │   ├── usuarios.html          ← Gerenciar usuários (admin)
│   │   ├── igrejas.html           ← Gerenciar igrejas (admin)
│   │   ├── Contagem_Culto_RIO.html← Formulário de contagem
│   │   └── Contagem_RIO.html      ← Dashboard gerencial
│   └── scripts/
│       ├── api.js                 ← Camada de comunicação com o backend
│       ├── auth.js                ← Autenticação/sessão
│       └── Contagem_RIO.py        ← (legado) gerador do dashboard estático
├── backend/                       ← API FastAPI (ver backend/README.md)
├── data/                          ← Planilhas
└── assets/images/                 ← Imagens de referência
```

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Frontend | HTML5, CSS3, JavaScript |
| Backend | Python 3, FastAPI |
| Banco de dados | Supabase (PostgreSQL) |
| Gráficos | Chart.js (CDN) |
| Ícones / Fontes | Font Awesome, Google Fonts (Inter) |

## Como Rodar (local)

O sistema tem duas partes que precisam estar no ar: o **backend** e o **frontend**.

### 1. Backend (API)

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

O backend fica em http://localhost:8000 (docs em `/docs`).

> A configuração do Supabase e do `.env` está detalhada em `backend/README.md`.

### 2. Frontend

O frontend precisa ser servido por HTTP (não abra o arquivo direto com `file://`,
senão as chamadas à API são bloqueadas pelo navegador).

Numa **segunda aba** do terminal, na raiz do projeto:

```bash
python3 -m http.server 5500
```

Depois acesse no navegador:

```
http://localhost:5500/index.html
```

### 3. Login

- **Usuário:** `admin`
- **Senha:** `admin`

## Sistema de Permissões

| Perfil | Contagem | Dashboard | Gerenciar Usuários/Igrejas |
|---|---|---|---|
| Admin | Todas as igrejas | Sim | Sim |
| Líder | Só a própria igreja | Sim (própria igreja) | Não |
| Servo | Só a própria igreja | Não | Não |

A regra de igreja é **aplicada no backend**: servos e líderes só acessam dados da
própria igreja, mesmo que tentem burlar pelo navegador.

## Fluxo de Uso

1. Fazer login
2. Na home, escolher **Contagem Geral**
3. Preencher os dados do culto (a igreja vem preenchida conforme o usuário)
4. Clicar em **Gerar Relatório** → **Enviar e Copiar**
   - Copia o relatório formatado para colar no WhatsApp
   - Salva a contagem no banco de dados
5. No **Dashboard**, ver os gráficos e KPIs com os dados salvos

## Configuração da URL do Backend

O frontend aponta para o backend em `src/scripts/api.js`:

```js
const API_BASE_URL = "http://localhost:8000";
```

Ao publicar o backend na Vercel, troque essa URL pela URL de produção.

## Documentação do Backend

Veja `backend/README.md` para: configuração do Supabase, variáveis de ambiente,
criação do admin e deploy na Vercel.

---

Desenvolvido para a Igreja RIO | 2026
# GC_RIO
# GC_RIO
