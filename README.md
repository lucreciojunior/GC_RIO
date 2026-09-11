# Contagem RIO - Sistema de Gestão de Cultos

Sistema de contagem e análise de dados dos cultos da Igreja RIO (Relevante, Integral e Orgânico).

Arquitetura enxuta: **frontend** (HTML/CSS/JS) conectado **diretamente ao Supabase**
(banco de dados + autenticação). Não há backend próprio para manter.

## Estrutura do Projeto

```
Contagem/
├── index.html                     ← Ponto de entrada (redireciona ao login)
├── supabase_setup.sql             ← Script para configurar o banco no Supabase
├── vercel.json                    ← Configuração de deploy do frontend
├── src/
│   ├── css/
│   │   └── global.css             ← Estilos globais
│   ├── pages/
│   │   ├── login.html             ← Login (Supabase Auth)
│   │   ├── home.html              ← Home (estilo Linktree)
│   │   ├── usuarios.html          ← Gerenciar usuários (admin)
│   │   ├── igrejas.html           ← Gerenciar igrejas (admin)
│   │   ├── Contagem_Culto_RIO.html← Formulário de contagem
│   │   └── Contagem_RIO.html      ← Dashboard gerencial
│   └── scripts/
│       ├── config.js              ← Configuração do Supabase (URL + anon key)
│       ├── api.js                 ← Camada de dados (Supabase JS)
│       └── auth.js                ← Proteção de páginas / sessão
├── data/                          ← Planilhas de referência
└── assets/images/                 ← Imagens
```

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Frontend | HTML5, CSS3, JavaScript |
| Banco + Auth | Supabase (PostgreSQL + Auth + RLS) |
| Gráficos | Chart.js (CDN) |
| Ícones / Fontes | Font Awesome, Google Fonts (Inter) |

## Configuração inicial (uma vez)

### 1. Criar o banco no Supabase

1. No Supabase, abra **SQL Editor > New Query**
2. Cole o conteúdo de `supabase_setup.sql` e clique em **Run**
   - Isso cria as tabelas (`igrejas`, `perfis`, `contagens`), as regras de segurança
     (RLS) e cadastra as 5 igrejas padrão.

### 2. Desativar confirmação de e-mail (obrigatório)

O login é por **usuário** (sem e-mail visível). Nos bastidores, o Supabase guarda
um e-mail interno `usuario@rio.local`. Como esse e-mail é fictício, a confirmação
precisa estar desligada:
- Supabase > **Authentication > Providers > Email** > desative **Confirm email** > Save

### 3. Criar o primeiro admin

1. Supabase > **Authentication > Users > Add user > Create new user**
   - **Email:** `admin@rio.local`
   - **Password:** escolha uma senha (guarde)
   - Marque **Auto Confirm User**
2. Volte ao **SQL Editor** e rode:

   ```sql
   UPDATE perfis
   SET perfil = 'admin', nome = 'Administrador', usuario = 'admin', igreja = 'PRADO'
   WHERE id = (SELECT id FROM auth.users WHERE email = 'admin@rio.local');
   ```

3. Pronto: logue no sistema com **usuário `admin`** e a senha escolhida.
   Os próximos usuários você cria pela tela "Gerenciar Usuários".

### 4. Conectar o frontend ao Supabase

Abra `src/scripts/config.js` e preencha:

```js
const SUPABASE_CONFIG = {
    url: "https://SEU-PROJETO.supabase.co",
    anonKey: "SUA_ANON_PUBLIC_KEY",   // Project Settings > API > anon public
};
```

> Use a chave **anon public** (não a service_role). Ela pode ficar no frontend
> com segurança porque o RLS protege os dados no banco.

## Como Rodar (local)

O frontend precisa ser servido por HTTP (não abra com `file://`):

```bash
python3 -m http.server 5500
```

Depois acesse: `http://localhost:5500/index.html`

## Sistema de Permissões

| Perfil | Contagem | Dashboard | Gerenciar Usuários/Igrejas |
|---|---|---|---|
| Admin | Todas as igrejas | Sim | Sim |
| Líder | Só a própria igreja | Sim (própria igreja) | Não |
| Servo | Só a própria igreja | Não | Não |

As regras são aplicadas pelo **RLS do Supabase** (no banco), então são seguras
mesmo o frontend acessando o banco diretamente.

## Fluxo de Uso

1. Login (usuário + senha)
2. Home → **Contagem Geral**
3. Preencher os dados (a igreja vem preenchida conforme o usuário)
4. **Gerar Relatório** → **Enviar e Copiar**: copia o texto para o WhatsApp e
   salva a contagem no banco
5. No **Dashboard**, ver gráficos e KPIs com os dados salvos

## Deploy

Veja `DEPLOY.md` — publica só o frontend na Vercel (um projeto, sem backend).

---

Desenvolvido para a Igreja RIO | 2026
