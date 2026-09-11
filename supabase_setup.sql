-- ============================================================
-- Contagem RIO - Setup completo (Supabase direto, sem backend)
-- Execute no Supabase: SQL Editor > New Query > Run
--
-- Este schema usa Supabase Auth + Row Level Security (RLS).
-- As regras de permissão rodam NO BANCO, então são seguras
-- mesmo o frontend chamando o Supabase diretamente.
-- ============================================================

-- ------------------------------------------------------------
-- Limpa versões antigas (as tabelas estavam vazias / de teste)
-- ------------------------------------------------------------
DROP TABLE IF EXISTS contagens CASCADE;
DROP TABLE IF EXISTS perfis CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;
DROP TABLE IF EXISTS igrejas CASCADE;

-- ============================================================
-- TABELA: igrejas
-- ============================================================
CREATE TABLE igrejas (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome TEXT NOT NULL UNIQUE,
    endereco TEXT,
    criado_em TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- TABELA: perfis
-- Liga cada usuário do Supabase Auth (auth.users) ao seu
-- perfil e igreja. O id é o mesmo id do usuário autenticado.
-- ============================================================
CREATE TABLE perfis (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    nome TEXT NOT NULL,
    usuario TEXT UNIQUE,
    perfil TEXT NOT NULL DEFAULT 'servo' CHECK (perfil IN ('admin', 'lider', 'servo')),
    igreja TEXT,
    criado_em TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- TABELA: contagens
-- ============================================================
CREATE TABLE contagens (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    igreja TEXT NOT NULL,
    data DATE NOT NULL,
    horario TEXT,
    responsavel TEXT,
    total_visitantes INT DEFAULT 0,
    total_criancas INT DEFAULT 0,
    total_nauta INT DEFAULT 0,
    total_servos INT DEFAULT 0,
    total_templo INT DEFAULT 0,
    total_geral INT DEFAULT 0,
    dados JSONB,
    criado_por UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    criado_em TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_contagens_igreja ON contagens(igreja);
CREATE INDEX idx_contagens_data ON contagens(data);

-- ============================================================
-- FUNÇÕES AUXILIARES (usadas nas regras de RLS)
-- ============================================================

-- Retorna o perfil do usuário logado
CREATE OR REPLACE FUNCTION meu_perfil()
RETURNS TEXT
LANGUAGE sql SECURITY DEFINER STABLE
AS $$
    SELECT perfil FROM perfis WHERE id = auth.uid();
$$;

-- Retorna a igreja do usuário logado
CREATE OR REPLACE FUNCTION minha_igreja()
RETURNS TEXT
LANGUAGE sql SECURITY DEFINER STABLE
AS $$
    SELECT igreja FROM perfis WHERE id = auth.uid();
$$;

-- ============================================================
-- ROW LEVEL SECURITY
-- ============================================================
ALTER TABLE igrejas ENABLE ROW LEVEL SECURITY;
ALTER TABLE perfis ENABLE ROW LEVEL SECURITY;
ALTER TABLE contagens ENABLE ROW LEVEL SECURITY;

-- ------------------------------------------------------------
-- IGREJAS
-- Qualquer usuário logado pode LER (para os selects).
-- Só admin pode inserir/editar/excluir.
-- ------------------------------------------------------------
CREATE POLICY "igrejas_select_logados" ON igrejas
    FOR SELECT TO authenticated
    USING (true);

CREATE POLICY "igrejas_admin_insert" ON igrejas
    FOR INSERT TO authenticated
    WITH CHECK (meu_perfil() = 'admin');

CREATE POLICY "igrejas_admin_update" ON igrejas
    FOR UPDATE TO authenticated
    USING (meu_perfil() = 'admin');

CREATE POLICY "igrejas_admin_delete" ON igrejas
    FOR DELETE TO authenticated
    USING (meu_perfil() = 'admin');

-- ------------------------------------------------------------
-- PERFIS
-- Cada um lê o próprio perfil; admin lê todos.
-- Só admin cria/edita/exclui perfis.
-- ------------------------------------------------------------
CREATE POLICY "perfis_select" ON perfis
    FOR SELECT TO authenticated
    USING (id = auth.uid() OR meu_perfil() = 'admin');

CREATE POLICY "perfis_admin_insert" ON perfis
    FOR INSERT TO authenticated
    WITH CHECK (meu_perfil() = 'admin');

CREATE POLICY "perfis_admin_update" ON perfis
    FOR UPDATE TO authenticated
    USING (meu_perfil() = 'admin');

CREATE POLICY "perfis_admin_delete" ON perfis
    FOR DELETE TO authenticated
    USING (meu_perfil() = 'admin' AND id <> auth.uid());

-- ------------------------------------------------------------
-- CONTAGENS
-- Admin vê/gerencia tudo.
-- Líder e servo só veem e criam da própria igreja.
-- ------------------------------------------------------------
CREATE POLICY "contagens_select" ON contagens
    FOR SELECT TO authenticated
    USING (meu_perfil() = 'admin' OR igreja = minha_igreja());

CREATE POLICY "contagens_insert" ON contagens
    FOR INSERT TO authenticated
    WITH CHECK (meu_perfil() = 'admin' OR igreja = minha_igreja());

CREATE POLICY "contagens_update" ON contagens
    FOR UPDATE TO authenticated
    USING (meu_perfil() = 'admin' OR igreja = minha_igreja());

CREATE POLICY "contagens_delete" ON contagens
    FOR DELETE TO authenticated
    USING (meu_perfil() = 'admin');

-- ============================================================
-- TRIGGER: cria automaticamente um perfil quando um usuário
-- novo é criado no Supabase Auth.
-- Lê nome/perfil/igreja dos metadados do cadastro.
-- ============================================================
CREATE OR REPLACE FUNCTION criar_perfil_novo_usuario()
RETURNS TRIGGER
LANGUAGE plpgsql SECURITY DEFINER
AS $$
BEGIN
    INSERT INTO perfis (id, nome, usuario, perfil, igreja)
    VALUES (
        NEW.id,
        COALESCE(NEW.raw_user_meta_data->>'nome', NEW.email),
        -- usa o "usuario" dos metadados; se faltar, deriva do e-mail (antes do @)
        COALESCE(NEW.raw_user_meta_data->>'usuario', split_part(NEW.email, '@', 1)),
        COALESCE(NEW.raw_user_meta_data->>'perfil', 'servo'),
        NEW.raw_user_meta_data->>'igreja'
    );
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION criar_perfil_novo_usuario();

-- ============================================================
-- DADOS INICIAIS: igrejas padrão
-- ============================================================
INSERT INTO igrejas (nome, endereco) VALUES
    ('PRADO', 'R. Carlos Gomes, 390 - Prado, Recife, PE'),
    ('ALDEIA', 'Aldeia, PE'),
    ('OLINDA', 'Olinda, PE'),
    ('AGUAZINHA', 'Aguazinha, Olinda, PE'),
    ('ZONA SUL', 'Zona Sul, Recife, PE')
ON CONFLICT (nome) DO NOTHING;

-- ============================================================
-- ADMIN INICIAL
-- O login do sistema é por NOME DE USUÁRIO. Nos bastidores, o
-- Supabase Auth guarda um e-mail sintético no formato:
--     <usuario>@rio.local
--
-- Para criar o admin (usuário: admin / senha: à sua escolha):
--
-- 1) Auth > Users > Add user > Create new user
--      Email: admin@rio.local
--      Password: (escolha uma senha)
--      Marque "Auto Confirm User".
--
-- 2) Rode o SQL abaixo para dar nome/usuário e promover a admin:
--
--   UPDATE perfis
--   SET perfil = 'admin', nome = 'Administrador', usuario = 'admin', igreja = 'PRADO'
--   WHERE id = (SELECT id FROM auth.users WHERE email = 'admin@rio.local');
--
-- Depois é só logar no sistema com usuário "admin" e a senha escolhida.
-- (instruções detalhadas no README)
-- ============================================================
