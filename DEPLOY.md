# Guia de Deploy na Vercel

Este guia publica o sistema Contagem RIO na Vercel: **backend** (FastAPI) e
**frontend** (HTML/CSS/JS) como **dois projetos separados**, a partir do mesmo
repositório no GitHub.

O banco de dados (Supabase) já está na nuvem, então não precisa fazer nada nele.

---

## Pré-requisitos

- Conta no **GitHub** (grátis)
- Conta na **Vercel** (grátis) — pode entrar com o GitHub
- Seu projeto já configurado localmente (Supabase + `.env` funcionando)

---

## Passo 1 — Subir o projeto para o GitHub

1. Crie um repositório novo no GitHub (ex: `contagem-rio`), **privado** de preferência.
2. No terminal, na raiz do projeto:

```bash
cd /Users/lucreciojuniorjr/Documents/RIO/Contagem
git init
git add .
git commit -m "Sistema Contagem RIO - frontend + backend"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/contagem-rio.git
git push -u origin main
```

> O `.gitignore` já garante que o arquivo `.env` (com as chaves secretas) **não** vai para o GitHub.

---

## Passo 2 — Publicar o BACKEND na Vercel

1. Acesse https://vercel.com e clique em **Add New... > Project**
2. Importe o repositório `contagem-rio`
3. Em **Root Directory**, clique em **Edit** e selecione a pasta **`backend`**
4. Em **Environment Variables**, adicione (os mesmos valores do seu `.env`):

   | Nome | Valor |
   |---|---|
   | `SUPABASE_URL` | sua Project URL do Supabase |
   | `SUPABASE_KEY` | sua service_role key do Supabase |
   | `JWT_SECRET` | a chave secreta (a mesma do `.env`) |
   | `JWT_EXPIRE_MINUTES` | `480` |
   | `CORS_ORIGINS` | *(deixe em branco por enquanto, ajustamos no passo 4)* |

5. Clique em **Deploy**
6. Quando terminar, copie a URL gerada (ex: `https://contagem-rio-api.vercel.app`)
7. Teste abrindo `SUA_URL/docs` — deve aparecer a documentação da API

---

## Passo 3 — Publicar o FRONTEND na Vercel

1. Novamente em **Add New... > Project**, importe o **mesmo** repositório
2. Deixe o **Root Directory** como a **raiz** (não mude)
3. Framework Preset: **Other** (é site estático)
4. Clique em **Deploy**
5. Copie a URL do frontend (ex: `https://contagem-rio.vercel.app`)

---

## Passo 4 — Conectar frontend e backend

### 4.1 Apontar o frontend para o backend

No arquivo `src/scripts/api.js`, troque a URL de produção pela URL real do backend:

```js
// >>> TROQUE pela URL do seu backend publicado na Vercel <<<
return "https://contagem-rio-api.vercel.app";  // <- sua URL real do backend
```

Faça commit e push (a Vercel re-publica sozinha):

```bash
git add src/scripts/api.js
git commit -m "Aponta frontend para backend de producao"
git push
```

### 4.2 Liberar o frontend no CORS do backend

No projeto **backend** na Vercel: **Settings > Environment Variables**, edite a
variável `CORS_ORIGINS` colocando a URL do frontend:

```
CORS_ORIGINS=https://contagem-rio.vercel.app
```

Depois vá em **Deployments** e clique em **Redeploy** no backend para aplicar.

---

## Passo 5 — Testar

1. Acesse a URL do frontend (ex: `https://contagem-rio.vercel.app`)
2. Faça login com `admin` / `admin`
3. Teste cadastrar uma igreja, um usuário e salvar uma contagem

---

## Observações importantes

- **Marca d'água**: a Vercel **não** coloca marca d'água. O plano grátis (Hobby)
  é para uso pessoal/não-comercial, o que se aplica a um sistema interno de igreja.
- **Backend "dormindo"**: diferente do Render, na Vercel o backend é serverless e
  responde sob demanda. A primeira requisição após um tempo ocioso pode ser um
  pouco mais lenta (alguns segundos).
- **Domínio próprio**: se quiser um domínio como `contagemrio.com.br`, dá para
  adicionar em **Settings > Domains** (o domínio em si é pago, mas a configuração
  na Vercel é grátis).

## Segurança

- Depois de tudo funcionando, **rotacione a service_role key** no Supabase
  (Settings > API Keys > Roll) e atualize a variável `SUPABASE_KEY` na Vercel,
  já que a chave circulou durante a configuração.
- **Troque a senha do admin** logo após o primeiro login.
