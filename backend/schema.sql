-- ============================================================
-- Schema do banco de dados - Contagem RIO
-- Execute este SQL no Supabase: SQL Editor > New Query > Run
-- ============================================================

-- ------------------------------------------------------------
-- Tabela: igrejas
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS igrejas (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome TEXT NOT NULL UNIQUE,
    endereco TEXT,
    criado_em TIMESTAMPTZ DEFAULT NOW()
);

-- ------------------------------------------------------------
-- Tabela: usuarios
-- perfil: 'admin' | 'lider' | 'servo'
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS usuarios (
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
-- Guarda o registro de cada culto contado.
-- dados: JSON com todos os campos por ministério (flexível)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS contagens (
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

-- Índices para acelerar filtros comuns do dashboard
CREATE INDEX IF NOT EXISTS idx_contagens_igreja ON contagens(igreja);
CREATE INDEX IF NOT EXISTS idx_contagens_data ON contagens(data);

-- ------------------------------------------------------------
-- Dados iniciais
-- ------------------------------------------------------------

-- Igrejas padrão
INSERT INTO igrejas (nome, endereco) VALUES
    ('PRADO', 'R. Carlos Gomes, 390 - Prado, Recife, PE'),
    ('ALDEIA', 'Aldeia, PE'),
    ('OLINDA', 'Olinda, PE'),
    ('AGUAZINHA', 'Aguazinha, Olinda, PE'),
    ('ZONA SUL', 'Zona Sul, Recife, PE')
ON CONFLICT (nome) DO NOTHING;

-- Usuário admin padrão:
-- NÃO é criado por aqui porque a senha precisa ser hasheada com bcrypt.
-- Depois de configurar o .env, rode:  cd backend && python seed_admin.py
-- Isso cria o admin com login "admin" e senha "admin".
