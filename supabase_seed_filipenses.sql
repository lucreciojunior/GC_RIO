-- ============================================================
-- Seed: Escala de Pregação - Filipenses (Ago-Out/2026)
-- Rode DEPOIS de supabase_programacao.sql
-- Limpa a série antes de inserir (evita duplicar se rodar de novo)
-- ============================================================

DELETE FROM pregacoes WHERE serie = 'Filipenses — Jornada de Alegria';

-- ------------------------------------------------------------
-- PRADO (09h, 11h15, 17h)
-- ------------------------------------------------------------
INSERT INTO pregacoes (igreja, data, texto, tema, serie, escalas) VALUES
('PRADO','2026-08-02','Fp 1:1-11','Alegria nas Relações','Filipenses — Jornada de Alegria','[{"horario":"09h","pregador":"Tomas Souza"},{"horario":"11h15","pregador":"Tomas Souza"},{"horario":"17h","pregador":"Marçal Lima"}]'),
('PRADO','2026-08-09','Fp 1:12-18','Alegria nos Sofrimentos','Filipenses — Jornada de Alegria','[{"horario":"09h","pregador":"Tomas Souza"},{"horario":"11h15","pregador":"Tomas Souza"},{"horario":"17h","pregador":"Rubens Lopes"}]'),
('PRADO','2026-08-16','Fp 1:19-26','Alegria em Cristo','Filipenses — Jornada de Alegria','[{"horario":"09h","pregador":"Tomas Souza"},{"horario":"11h15","pregador":"Tomas Souza"},{"horario":"17h","pregador":"Adelson Acioly"}]'),
('PRADO','2026-08-23','Fp 1:27-30','Alegria nas Lutas','Filipenses — Jornada de Alegria','[{"horario":"09h","pregador":"Marçal Lima"},{"horario":"11h15","pregador":"Marçal Lima"},{"horario":"17h","pregador":"Marçal Lima"}]'),
('PRADO','2026-08-30','Fp 2:1-4','Alegria Humilde','Filipenses — Jornada de Alegria','[{"horario":"09h","pregador":"Marçal Lima"},{"horario":"11h15","pregador":"Marçal Lima"},{"horario":"17h","pregador":"Marçal Lima"}]'),
('PRADO','2026-09-06','Fp 2:5-11','Alegria em Imitá-lo','Filipenses — Jornada de Alegria','[{"horario":"09h","pregador":"Tomas Souza"},{"horario":"11h15","pregador":"Tomas Souza"},{"horario":"17h","pregador":"Eduardo Noberto"}]'),
('PRADO','2026-09-13','Fp 2:12-18','Alegria em Servir','Filipenses — Jornada de Alegria','[{"horario":"09h","pregador":"Tomas Souza"},{"horario":"11h15","pregador":"Tomas Souza"},{"horario":"17h","pregador":"Marçal Lima"}]'),
('PRADO','2026-09-20','Fp 2:19-30','Alegria em Cuidar','Filipenses — Jornada de Alegria','[{"horario":"09h","pregador":"Tomas Souza"},{"horario":"11h15","pregador":"Tomas Souza"},{"horario":"17h","pregador":"Marçal Lima"}]'),
('PRADO','2026-09-27','Fp 3:1-11','Alegria em Perder para Ganhar','Filipenses — Jornada de Alegria','[{"horario":"09h","pregador":"Rubens Lopes"},{"horario":"11h15","pregador":"Rubens Lopes"},{"horario":"17h","pregador":"Rubens Lopes"}]'),
('PRADO','2026-10-04','Fp 3:12-16','Alegria em Avançar','Filipenses — Jornada de Alegria','[{"horario":"09h","pregador":"Tomas Souza"},{"horario":"11h15","pregador":"Tomas Souza"},{"horario":"17h","pregador":"Adelson Acioly"}]'),
('PRADO','2026-10-11','Fp 3:17-4:1','Alegria em Esperar','Filipenses — Jornada de Alegria','[{"horario":"09h","pregador":"Marçal Lima"},{"horario":"11h15","pregador":"Marçal Lima"},{"horario":"17h","pregador":"Marçal Lima"}]'),
('PRADO','2026-10-18','Fp 4:2-9','Alegria em Ter Paz','Filipenses — Jornada de Alegria','[{"horario":"09h","pregador":"Rubens Lopes"},{"horario":"11h15","pregador":"Rubens Lopes"},{"horario":"17h","pregador":"Rubens Lopes"}]'),
('PRADO','2026-10-25','Fp 4:10-23','Alegria em Estar Contente','Filipenses — Jornada de Alegria','[{"horario":"09h","pregador":"Tomas Souza"},{"horario":"11h15","pregador":"Tomas Souza"},{"horario":"17h","pregador":"Eduardo Noberto"}]');

-- ------------------------------------------------------------
-- ALDEIA (18h)
-- ------------------------------------------------------------
INSERT INTO pregacoes (igreja, data, texto, tema, serie, escalas) VALUES
('ALDEIA','2026-08-02','Fp 1:1-11','Alegria nas Relações','Filipenses — Jornada de Alegria','[{"horario":"18h","pregador":"Tomas Souza"}]'),
('ALDEIA','2026-08-09','Fp 1:12-18','Alegria nos Sofrimentos','Filipenses — Jornada de Alegria','[{"horario":"18h","pregador":"Tomas Souza"}]'),
('ALDEIA','2026-08-16','Fp 1:19-26','Alegria em Cristo','Filipenses — Jornada de Alegria','[{"horario":"18h","pregador":"Tomas Souza"}]'),
('ALDEIA','2026-08-23','Fp 1:27-30','Alegria nas Lutas','Filipenses — Jornada de Alegria','[{"horario":"18h","pregador":"Rafael Leonardo"}]'),
('ALDEIA','2026-08-30','Fp 2:1-4','Alegria Humilde','Filipenses — Jornada de Alegria','[{"horario":"18h","pregador":"Sóstenes Bernardes"}]'),
('ALDEIA','2026-09-06','Fp 2:5-11','Alegria em Imitá-lo','Filipenses — Jornada de Alegria','[{"horario":"18h","pregador":"Tomas Souza"}]'),
('ALDEIA','2026-09-13','Fp 2:12-18','Alegria em Servir','Filipenses — Jornada de Alegria','[{"horario":"18h","pregador":"Tomas Souza"}]'),
('ALDEIA','2026-09-20','Fp 2:19-30','Alegria em Cuidar','Filipenses — Jornada de Alegria','[{"horario":"18h","pregador":"Tomas Souza"}]'),
('ALDEIA','2026-09-27','Fp 3:1-11','Alegria em Perder para Ganhar','Filipenses — Jornada de Alegria','[{"horario":"18h","pregador":"Rafael Leonardo"}]'),
('ALDEIA','2026-10-04','Fp 3:12-16','Alegria em Avançar','Filipenses — Jornada de Alegria','[{"horario":"18h","pregador":"Tomas Souza"}]'),
('ALDEIA','2026-10-11','Fp 3:17-4:1','Alegria em Esperar','Filipenses — Jornada de Alegria','[{"horario":"18h","pregador":"Sóstenes Bernardes"}]'),
('ALDEIA','2026-10-18','Fp 4:2-9','Alegria em Ter Paz','Filipenses — Jornada de Alegria','[{"horario":"18h","pregador":"Rafael Leonardo"}]'),
('ALDEIA','2026-10-25','Fp 4:10-23','Alegria em Estar Contente','Filipenses — Jornada de Alegria','[{"horario":"18h","pregador":"Tomas Souza"}]');

-- ------------------------------------------------------------
-- AGUAZINHA (10h)
-- ------------------------------------------------------------
INSERT INTO pregacoes (igreja, data, texto, tema, serie, escalas) VALUES
('AGUAZINHA','2026-08-02','Fp 1:1-11','Alegria nas Relações','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Davi Elias"}]'),
('AGUAZINHA','2026-08-09','Fp 1:12-18','Alegria nos Sofrimentos','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Davi Elias"}]'),
('AGUAZINHA','2026-08-16','Fp 1:19-26','Alegria em Cristo','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Davi Elias"}]'),
('AGUAZINHA','2026-08-23','Fp 1:27-30','Alegria nas Lutas','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Carlinhos Senegal"}]'),
('AGUAZINHA','2026-08-30','Fp 2:1-4','Alegria Humilde','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Davi Elias"}]'),
('AGUAZINHA','2026-09-06','Fp 2:5-11','Alegria em Imitá-lo','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Davi Elias"}]'),
('AGUAZINHA','2026-09-13','Fp 2:12-18','Alegria em Servir','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Davi Elias"}]'),
('AGUAZINHA','2026-09-20','Fp 2:19-30','Alegria em Cuidar','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Gabriel Ribeiro"}]'),
('AGUAZINHA','2026-09-27','Fp 3:1-11','Alegria em Perder para Ganhar','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Davi Elias"}]'),
('AGUAZINHA','2026-10-04','Fp 3:12-16','Alegria em Avançar','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Davi Elias"}]'),
('AGUAZINHA','2026-10-11','Fp 3:17-4:1','Alegria em Esperar','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Davi Elias"}]'),
('AGUAZINHA','2026-10-18','Fp 4:2-9','Alegria em Ter Paz','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Carlinhos Senegal"}]'),
('AGUAZINHA','2026-10-25','Fp 4:10-23','Alegria em Estar Contente','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Davi Elias"}]');

-- ------------------------------------------------------------
-- ZONA SUL (10h)
-- ------------------------------------------------------------
INSERT INTO pregacoes (igreja, data, texto, tema, serie, escalas) VALUES
('ZONA SUL','2026-08-02','Fp 1:1-11','Alegria nas Relações','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Rodrigo Dantas"}]'),
('ZONA SUL','2026-08-09','Fp 1:12-18','Alegria nos Sofrimentos','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Rodrigo Dantas"}]'),
('ZONA SUL','2026-08-16','Fp 1:19-26','Alegria em Cristo','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Jeiseriel (Convidado)"}]'),
('ZONA SUL','2026-08-23','Fp 1:27-30','Alegria nas Lutas','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Rodrigo Dantas"}]'),
('ZONA SUL','2026-08-30','Fp 2:1-4','Alegria Humilde','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Rodrigo Dantas"}]'),
('ZONA SUL','2026-09-06','Fp 2:5-11','Alegria em Imitá-lo','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Rodrigo Dantas"}]'),
('ZONA SUL','2026-09-13','Fp 2:12-18','Alegria em Servir','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Rodrigo Dantas"}]'),
('ZONA SUL','2026-09-20','Fp 2:19-30','Alegria em Cuidar','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Raryel Montenegro"}]'),
('ZONA SUL','2026-09-27','Fp 3:1-11','Alegria em Perder para Ganhar','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Rodrigo Dantas"}]'),
('ZONA SUL','2026-10-04','Fp 3:12-16','Alegria em Avançar','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Rodrigo Dantas"}]'),
('ZONA SUL','2026-10-11','Fp 3:17-4:1','Alegria em Esperar','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Tomas Souza"}]'),
('ZONA SUL','2026-10-18','Fp 4:2-9','Alegria em Ter Paz','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Raryel Montenegro"}]'),
('ZONA SUL','2026-10-25','Fp 4:10-23','Alegria em Estar Contente','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Rodrigo Dantas"}]');

-- ------------------------------------------------------------
-- OLINDA (10h, 16h, 18h30)
-- ------------------------------------------------------------
INSERT INTO pregacoes (igreja, data, texto, tema, serie, escalas) VALUES
('OLINDA','2026-08-02','Fp 1:1-11','Alegria nas Relações','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Rodrigo Simeão"},{"horario":"16h","pregador":"Rodrigo Simeão"},{"horario":"18h30","pregador":"Rodrigo Simeão"}]'),
('OLINDA','2026-08-09','Fp 1:12-18','Alegria nos Sofrimentos','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Ednaldo Vasconcelos"},{"horario":"16h","pregador":"Rodrigo Dantas"},{"horario":"18h30","pregador":"Rodrigo Dantas"}]'),
('OLINDA','2026-08-16','Fp 1:19-26','Alegria em Cristo','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Rodrigo Simeão"},{"horario":"16h","pregador":"Rodrigo Simeão"},{"horario":"18h30","pregador":"Rodrigo Simeão"}]'),
('OLINDA','2026-08-23','Fp 1:27-30','Alegria nas Lutas','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Matheus Omena"},{"horario":"16h","pregador":"Matheus Omena"},{"horario":"18h30","pregador":"Matheus Omena"}]'),
('OLINDA','2026-08-30','Fp 2:1-4','Alegria Humilde','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Rodrigo Simeão"},{"horario":"16h","pregador":"Rodrigo Simeão"},{"horario":"18h30","pregador":"Rodrigo Simeão"}]'),
('OLINDA','2026-09-06','Fp 2:5-11','Alegria em Imitá-lo','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Rodrigo Simeão"},{"horario":"16h","pregador":"Rodrigo Simeão"},{"horario":"18h30","pregador":"Rodrigo Simeão"}]'),
('OLINDA','2026-09-13','Fp 2:12-18','Alegria em Servir','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Ednaldo Vasconcelos"},{"horario":"16h","pregador":"Rodrigo Dantas"},{"horario":"18h30","pregador":"Rodrigo Dantas"}]'),
('OLINDA','2026-09-20','Fp 2:19-30','Alegria em Cuidar','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Rodrigo Simeão"},{"horario":"16h","pregador":"Rodrigo Simeão"},{"horario":"18h30","pregador":"Rodrigo Simeão"}]'),
('OLINDA','2026-09-27','Fp 3:1-11','Alegria em Perder para Ganhar','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Matheus Omena"},{"horario":"16h","pregador":"Matheus Omena"},{"horario":"18h30","pregador":"Matheus Omena"}]'),
('OLINDA','2026-10-04','Fp 3:12-16','Alegria em Avançar','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Ednaldo Vasconcelos"},{"horario":"16h","pregador":"Rodrigo Dantas"},{"horario":"18h30","pregador":"Rodrigo Dantas"}]'),
('OLINDA','2026-10-11','Fp 3:17-4:1','Alegria em Esperar','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Matheus Omena"},{"horario":"16h","pregador":"Tomas Souza"},{"horario":"18h30","pregador":"Tomas Souza"}]'),
('OLINDA','2026-10-18','Fp 4:2-9','Alegria em Ter Paz','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Rodrigo Simeão"},{"horario":"16h","pregador":"Rodrigo Simeão"},{"horario":"18h30","pregador":"Rodrigo Simeão"}]'),
('OLINDA','2026-10-25','Fp 4:10-23','Alegria em Estar Contente','Filipenses — Jornada de Alegria','[{"horario":"10h","pregador":"Rodrigo Simeão"},{"horario":"16h","pregador":"Rodrigo Simeão"},{"horario":"18h30","pregador":"Rodrigo Simeão"}]');

-- ------------------------------------------------------------
-- AVISOS - Setembro / ALDEIA (exemplo enviado)
-- ------------------------------------------------------------
DELETE FROM avisos WHERE igreja = 'ALDEIA' AND data IN ('2026-09-06','2026-09-13','2026-09-20','2026-09-27');
INSERT INTO avisos (igreja, data, responsavel) VALUES
('ALDEIA','2026-09-06','Rafa'),
('ALDEIA','2026-09-13','Rafa'),
('ALDEIA','2026-09-20','Sóstenes'),
('ALDEIA','2026-09-27','Samuel');

SELECT 'seed filipenses + avisos aplicado' AS status;
