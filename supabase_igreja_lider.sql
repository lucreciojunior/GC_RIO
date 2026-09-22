-- ============================================================
-- Adiciona o líder de gestão de culto à tabela de igrejas
-- Rode no SQL Editor do Supabase.
-- ============================================================

ALTER TABLE igrejas ADD COLUMN IF NOT EXISTS lider TEXT;

-- (Opcional) A coluna endereco deixa de ser usada pelo sistema.
-- Não precisa remover; ela apenas fica ignorada.

SELECT 'coluna lider adicionada' AS status;
