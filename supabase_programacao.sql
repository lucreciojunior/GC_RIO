-- ============================================================
-- Contagem RIO - Programação (Pregação + Avisos)
-- SQL incremental. Rode no SQL Editor do Supabase.
-- ============================================================

-- ------------------------------------------------------------
-- TABELA: pregacoes
-- escalas = JSON no formato [{ "horario": "09h", "pregador": "Tomas Souza" }, ...]
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS pregacoes (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    igreja TEXT NOT NULL,
    data DATE NOT NULL,
    texto TEXT,           -- ex: "Fp 1:1-11"
    tema TEXT,            -- ex: "Alegria nas Relações"
    serie TEXT,           -- ex: "Filipenses — Jornada de Alegria"
    escalas JSONB,        -- lista de { horario, pregador }
    criado_em TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_pregacoes_igreja ON pregacoes(igreja);
CREATE INDEX IF NOT EXISTS idx_pregacoes_data ON pregacoes(data);

-- ------------------------------------------------------------
-- TABELA: avisos
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS avisos (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    igreja TEXT NOT NULL,
    data DATE NOT NULL,
    responsavel TEXT,
    descricao TEXT,
    criado_em TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_avisos_igreja ON avisos(igreja);
CREATE INDEX IF NOT EXISTS idx_avisos_data ON avisos(data);

-- ------------------------------------------------------------
-- RLS: admin vê/gerencia tudo; líder vê/gerencia a própria igreja
-- ------------------------------------------------------------
ALTER TABLE pregacoes ENABLE ROW LEVEL SECURITY;
ALTER TABLE avisos ENABLE ROW LEVEL SECURITY;

-- PREGACOES
DROP POLICY IF EXISTS "pregacoes_select" ON pregacoes;
CREATE POLICY "pregacoes_select" ON pregacoes
    FOR SELECT TO authenticated
    USING (meu_perfil() = 'admin' OR (meu_perfil() = 'lider' AND igreja = minha_igreja()));

DROP POLICY IF EXISTS "pregacoes_insert" ON pregacoes;
CREATE POLICY "pregacoes_insert" ON pregacoes
    FOR INSERT TO authenticated
    WITH CHECK (meu_perfil() = 'admin' OR (meu_perfil() = 'lider' AND igreja = minha_igreja()));

DROP POLICY IF EXISTS "pregacoes_update" ON pregacoes;
CREATE POLICY "pregacoes_update" ON pregacoes
    FOR UPDATE TO authenticated
    USING (meu_perfil() = 'admin' OR (meu_perfil() = 'lider' AND igreja = minha_igreja()));

DROP POLICY IF EXISTS "pregacoes_delete" ON pregacoes;
CREATE POLICY "pregacoes_delete" ON pregacoes
    FOR DELETE TO authenticated
    USING (meu_perfil() = 'admin' OR (meu_perfil() = 'lider' AND igreja = minha_igreja()));

-- AVISOS
DROP POLICY IF EXISTS "avisos_select" ON avisos;
CREATE POLICY "avisos_select" ON avisos
    FOR SELECT TO authenticated
    USING (meu_perfil() = 'admin' OR (meu_perfil() = 'lider' AND igreja = minha_igreja()));

DROP POLICY IF EXISTS "avisos_insert" ON avisos;
CREATE POLICY "avisos_insert" ON avisos
    FOR INSERT TO authenticated
    WITH CHECK (meu_perfil() = 'admin' OR (meu_perfil() = 'lider' AND igreja = minha_igreja()));

DROP POLICY IF EXISTS "avisos_update" ON avisos;
CREATE POLICY "avisos_update" ON avisos
    FOR UPDATE TO authenticated
    USING (meu_perfil() = 'admin' OR (meu_perfil() = 'lider' AND igreja = minha_igreja()));

DROP POLICY IF EXISTS "avisos_delete" ON avisos;
CREATE POLICY "avisos_delete" ON avisos
    FOR DELETE TO authenticated
    USING (meu_perfil() = 'admin' OR (meu_perfil() = 'lider' AND igreja = minha_igreja()));

SELECT 'pregacoes e avisos criadas' AS status;
