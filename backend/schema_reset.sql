-- ============================================================
-- RESET do schema - Contagem RIO
-- ATENÇÃO: isto APAGA as tabelas existentes e recria do zero.
-- Use apenas porque as tabelas atuais estão vazias / de teste.
-- Execute no Supabase: SQL Editor > New Query > Run
-- ============================================================

-- Remove as tabelas antigas (ordem importa por causa das FKs)
DROP TABLE IF EXISTS contagens CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;
DROP TABLE IF EXISTS igrejas CASCADE;

-- ------------------------------------------------------------
-- Tabela: igrejas
-- ------------------------------------------------------------
CREATE TABLE igrejas (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome TEXT NOT NULL UNIQUE,
    endereco TEXT,
    criado_em TIMESTAMPTZ DEFAULT NOW()
);

-- ------------------------------------------------------------
-- Tabela: usuarios
-- ------------------------------------------------------------
CREATE TABLE usuarios (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome TEXT NOT NULL,
    usuario TEXT NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL,
    perfil TEXT NOT NULL DEFAULT 'servo' CHECK (perfil IN ('admin', 'lider', 'servo')),
    igreja TEXT,
    criado_em TIMESTAMPTZ DEFAULT NOW()
);

-- ------------------------------------------------------------
-- Tabela: contagens
-- ------------------------------------------------------------
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
    usuario_id BIGINT REFERENCES usuarios(id) ON DELETE SET NULL,
    criado_em TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_contagens_igreja ON contagens(igreja);
CREATE INDEX idx_contagens_data ON contagens(data);

-- Igrejas padrão
INSERT INTO igrejas (nome, endereco) VALUES
    ('PRADO', 'R. Carlos Gomes, 390 - Prado, Recife, PE'),
    ('ALDEIA', 'Aldeia, PE'),
    ('OLINDA', 'Olinda, PE'),
    ('AGUAZINHA', 'Aguazinha, Olinda, PE'),
    ('ZONA SUL', 'Zona Sul, Recife, PE');

-- O admin é criado depois com: python seed_admin.py
