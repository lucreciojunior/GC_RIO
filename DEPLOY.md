# Guia de Deploy na Vercel

Como o sistema agora fala **direto com o Supabase**, só existe **um projeto** para
publicar: o **frontend** (site estático). Sem backend, sem CORS, sem servidor.

O banco (Supabase) já está na nuvem — nada a fazer nele além do setup inicial
(veja o `README.md`).

---

## Pré-requisitos

- Conta no **GitHub**
- Conta na **Vercel** (pode entrar com o GitHub)
- `src/scripts/config.js` preenchido com a URL e a anon key do seu Supabase

---

## Passo 1 — Subir para o GitHub

Na raiz do projeto:

```bash
git add .
git commit -m "Sistema Contagem RIO - frontend + Supabase"
git push
```

> A `config.js` contém apenas a **anon key** (pública e protegida por RLS), então
> pode ir para o repositório sem problema.

---

## Passo 2 — Publicar na Vercel

1. Acesse https://vercel.com → **Add New... > Project**
2. Importe o repositório do projeto
3. **Framework Preset**: **Other** (site estático)
4. **Root Directory**: deixe na **raiz** (não altere)
5. Clique em **Deploy**
6. Copie a URL gerada (ex: `https://contagem-rio.vercel.app`)

Pronto. O site já está no ar.

---

## Passo 3 — Liberar o domínio no Supabase

Para o login funcionar no domínio publicado:

1. Supabase > **Authentication > URL Configuration**
2. Em **Site URL**, coloque a URL da Vercel (ex: `https://contagem-rio.vercel.app`)
3. Em **Redirect URLs**, adicione a mesma URL

---

## Passo 4 — Testar

1. Acesse a URL da Vercel
2. Faça login com o admin criado no setup
3. Teste cadastrar igreja, usuário e salvar uma contagem

---

## Observações

- **Marca d'água**: a Vercel não coloca marca d'água. O plano grátis (Hobby) serve
  bem para um sistema interno de igreja (uso não-comercial).
- **Atualizações**: cada `git push` re-publica o site automaticamente.
- **Domínio próprio**: se quiser algo como `contagemrio.com.br`, dá para adicionar
  em **Settings > Domains** (o domínio em si é pago; a configuração na Vercel é grátis).

## Segurança

- A anon key é pública por design; a proteção real está no **RLS** do Supabase.
- Considere **rotacionar as chaves** no Supabase, já que chaves circularam durante
  a configuração inicial.
