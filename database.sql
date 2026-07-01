-- Fale Facil - Script de criacao do banco de dados

CREATE DATABASE IF NOT EXISTS fale_facil_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE fale_facil_db;

CREATE TABLE IF NOT EXISTS usuarios (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    nome       VARCHAR(100) NOT NULL,
    email      VARCHAR(150) NOT NULL UNIQUE,
    senha      VARCHAR(64)  NOT NULL,
    perfil     ENUM('admin','funcionario') NOT NULL DEFAULT 'funcionario',
    criado_em  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS feedbacks (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id   INT NOT NULL,
    funcionario  VARCHAR(100) NOT NULL,
    departamento VARCHAR(100) NOT NULL,
    categoria    ENUM('Sugestao','Reclamacao','Elogio','Melhoria','Outro') NOT NULL,
    titulo       VARCHAR(200) NOT NULL,
    descricao    TEXT NOT NULL,
    prioridade   ENUM('Baixa','Media','Alta','Urgente') NOT NULL DEFAULT 'Media',
    status       ENUM('Pendente','Em Analise','Resolvido') NOT NULL DEFAULT 'Pendente',
    anonimo      TINYINT(1) NOT NULL DEFAULT 0,
    criado_em    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Usuarios padrao
-- Senha admin: admin123
-- Senha funcionario: func123
INSERT INTO usuarios (nome, email, senha, perfil) VALUES
('Administrador', 'admin@empresa.com', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin'),
('Joao Silva', 'joao@empresa.com', '98bedb5e9f0218ff6dd0e95e914fd25f21f3fa8ef599b7a09a900e580f464e7e', 'funcionario');
