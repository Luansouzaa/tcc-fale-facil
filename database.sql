
--SCRIPT DE CRIAÇÃO DO BANCO DE DADOS - Sistema de Feedbacks


CREATE DATABASE IF NOT EXISTS feedback_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE feedback_db;

CREATE TABLE IF NOT EXISTS feedbacks (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    funcionario  VARCHAR(100)  NOT NULL,
    departamento VARCHAR(100)  NOT NULL,
    categoria    ENUM('Sugestao','Reclamacao','Elogio','Melhoria','Outro') NOT NULL,
    titulo       VARCHAR(200)  NOT NULL,
    descricao    TEXT          NOT NULL,
    prioridade   ENUM('Baixa','Media','Alta','Urgente') NOT NULL DEFAULT 'Media',
    status       ENUM('Pendente','Em Analise','Resolvido') NOT NULL DEFAULT 'Pendente',
    criado_em    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dados de exemplo
INSERT INTO feedbacks (funcionario, departamento, categoria, titulo, descricao, prioridade, status) VALUES
('Ana Silva',    'RH',           'Sugestao',   'Flexibilidade de horario',        'Seria otimo termos mais opcoes de horario flexivel para melhorar o equilibrio entre trabalho e vida pessoal.', 'Media',   'Pendente'),
('Carlos Souza', 'TI',           'Reclamacao', 'Internet lenta no andar 3',       'A conexao de internet no terceiro andar esta muito instavel ha semanas, prejudicando a produtividade.',        'Alta',    'Em Analise'),
('Mariana Lima', 'Financeiro',   'Elogio',     'Otimo suporte do time de TI',     'O time de TI resolveu meu problema rapidamente e com muita cordialidade. Parabens!',                          'Baixa',   'Resolvido'),
('Pedro Nunes',  'Comercial',    'Melhoria',   'Atualizar sistema de vendas',     'O sistema atual e lento e tem bugs frequentes. Precisamos de uma atualizacao urgente.',                        'Urgente', 'Pendente'),
('Juliana Costa','Operacoes',    'Sugestao',   'Sala de descompressao',           'Uma sala para pausas curtas ajudaria muito o bem-estar dos funcionarios.',                                      'Media',   'Pendente');
