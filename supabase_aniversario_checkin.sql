-- ============================================================
-- Contagem RIO - Aniversariantes + Check-in
-- SQL incremental (não apaga nada). Rode no SQL Editor do Supabase.
-- ============================================================

-- ------------------------------------------------------------
-- 1) ANIVERSARIANTES: adiciona data de nascimento ao perfil
-- ------------------------------------------------------------
ALTER TABLE perfis ADD COLUMN IF NOT EXISTS data_nascimento DATE;

-- Atualiza o trigger para gravar data_nascimento vinda do cadastro
CREATE OR REPLACE FUNCTION criar_perfil_novo_usuario()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
    INSERT INTO public.perfis (id, nome, usuario, perfil, igreja, data_nascimento)
    VALUES (
        NEW.id,
        COALESCE(NEW.raw_user_meta_data->>'nome', NEW.email),
        COALESCE(NEW.raw_user_meta_data->>'usuario', split_part(NEW.email, '@', 1)),
        COALESCE(NEW.raw_user_meta_data->>'perfil', 'servo'),
        NEW.raw_user_meta_data->>'igreja',
        NULLIF(NEW.raw_user_meta_data->>'data_nascimento', '')::DATE
    )
    ON CONFLICT (id) DO NOTHING;
    RETURN NEW;
EXCEPTION WHEN OTHERS THEN
    RETURN NEW;
END;
$$;

-- ------------------------------------------------------------
-- 2) CHECK-IN: tabela de presença dos servos
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS checkins (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    servo_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    servo_nome TEXT NOT NULL,
    igreja TEXT NOT NULL,
    data DATE NOT NULL DEFAULT CURRENT_DATE,
    horario TIME DEFAULT (now() AT TIME ZONE 'America/Recife')::time,
    marcado_por UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    criado_em TIMESTAMPTZ DEFAULT NOW(),
    -- Um servo só pode ter 1 check-in por dia
    UNIQUE (servo_id, data)
);

CREATE INDEX IF NOT EXISTS idx_checkins_igreja ON checkins(igreja);
CREATE INDEX IF NOT EXISTS idx_checkins_data ON checkins(data);

-- ------------------------------------------------------------
-- 3) RLS da tabela checkins
-- ------------------------------------------------------------
ALTER TABLE checkins ENABLE ROW LEVEL SECURITY;

-- LER: admin vê tudo; lider/servo veem os check-ins da própria igreja
DROP POLICY IF EXISTS "checkins_select" ON checkins;
CREATE POLICY "checkins_select" ON checkins
    FOR SELECT TO authenticated
    USING (meu_perfil() = 'admin' OR igreja = minha_igreja());

-- INSERIR:
--   - servo pode marcar o PRÓPRIO check-in (servo_id = auth.uid) na própria igreja
--   - lider/admin podem marcar de qualquer servo da própria igreja (admin: qualquer)
DROP POLICY IF EXISTS "checkins_insert" ON checkins;
CREATE POLICY "checkins_insert" ON checkins
    FOR INSERT TO authenticated
    WITH CHECK (
        meu_perfil() = 'admin'
        OR (meu_perfil() = 'lider' AND igreja = minha_igreja())
        OR (servo_id = auth.uid() AND igreja = minha_igreja())
    );

-- APAGAR (desmarcar):
--   - servo pode remover o PRÓPRIO check-in
--   - lider pode remover check-ins da própria igreja
--   - admin pode remover qualquer
DROP POLICY IF EXISTS "checkins_delete" ON checkins;
CREATE POLICY "checkins_delete" ON checkins
    FOR DELETE TO authenticated
    USING (
        meu_perfil() = 'admin'
        OR (meu_perfil() = 'lider' AND igreja = minha_igreja())
        OR servo_id = auth.uid()
    );

-- ------------------------------------------------------------
-- 4) Permite que servos e líderes listem os servos da própria
--    igreja (necessário para o líder marcar check-in manual).
--    A policy de SELECT em "perfis" hoje só deixa ver o próprio.
--    Ajustamos para: admin vê todos; lider vê os da sua igreja;
--    servo vê o próprio.
-- ------------------------------------------------------------
DROP POLICY IF EXISTS "perfis_select" ON perfis;
CREATE POLICY "perfis_select" ON perfis
    FOR SELECT TO authenticated
    USING (
        id = auth.uid()
        OR meu_perfil() = 'admin'
        OR (meu_perfil() = 'lider' AND igreja = minha_igreja())
    );

-- Conferir
SELECT 'checkins criada' AS status;
