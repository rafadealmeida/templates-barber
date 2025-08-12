CREATE DATABASE barberia CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE barberia;

PRAGMA foreign_keys = OFF;       -- evita problemas se rodar sobre BD existente
BEGIN TRANSACTION;

/*--------------------------------------------------------------
  BARBEARIA
--------------------------------------------------------------*/
CREATE TABLE barbearia (
    id                TEXT      NOT NULL PRIMARY KEY,     -- UUID
    nome              TEXT      NOT NULL,
    logo              TEXT,
    cor_primaria      TEXT,
    cor_secundaria    TEXT,
    telefone_whatsapp TEXT,
    endereco          TEXT,
    latitude          NUMERIC,
    longitude         NUMERIC,
    descricao         TEXT,
    proprietario_id   INTEGER,                           -- auth_user.id
    criado_em         DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

/*--------------------------------------------------------------
  CHAVE_CONTEUDO
--------------------------------------------------------------*/
CREATE TABLE chave_conteudo (
    id         TEXT   NOT NULL PRIMARY KEY,               -- UUID
    chave      TEXT   NOT NULL UNIQUE,
    descricao  TEXT
);

/*--------------------------------------------------------------
  PROFISSIONAL
--------------------------------------------------------------*/
CREATE TABLE profissional (
    id            TEXT  NOT NULL PRIMARY KEY,             -- UUID
    barbearia_id  TEXT  NOT NULL,
    nome          TEXT  NOT NULL,
    foto          TEXT,
    descricao     TEXT,
    FOREIGN KEY (barbearia_id) REFERENCES barbearia(id) ON DELETE CASCADE
);

/*--------------------------------------------------------------
  SERVICO
--------------------------------------------------------------*/
CREATE TABLE servico (
    id            TEXT   NOT NULL PRIMARY KEY,            -- UUID
    barbearia_id  TEXT   NOT NULL,
    nome          TEXT   NOT NULL,
    descricao     TEXT,
    preco         NUMERIC,
    imagem        TEXT,
    FOREIGN KEY (barbearia_id) REFERENCES barbearia(id) ON DELETE CASCADE
);

/*--------------------------------------------------------------
  INFORMACAO_SITE
--------------------------------------------------------------*/
CREATE TABLE informacao_site (
    id            TEXT   NOT NULL PRIMARY KEY,            -- UUID
    barbearia_id  TEXT   NOT NULL,
    categoria     TEXT   NOT NULL
                 CHECK (categoria IN ('CONTEUDO_SITE','REDES_SOCIAIS','PROMOCOES')),
    chave_id      TEXT   NOT NULL,
    conteudo      TEXT,
    url           TEXT,
    data_inicio   DATE,
    data_fim      DATE,
    criado_em     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (barbearia_id) REFERENCES barbearia(id)      ON DELETE CASCADE,
    FOREIGN KEY (chave_id)     REFERENCES chave_conteudo(id) ON DELETE CASCADE,
    UNIQUE (barbearia_id, categoria, chave_id)
);

/*--------------------------------------------------------------
  IMAGENS_SITE
--------------------------------------------------------------*/
CREATE TABLE imagens_site (
    id            TEXT   NOT NULL PRIMARY KEY,            -- UUID
    barbearia_id  TEXT   NOT NULL,
    chave_id      TEXT   NOT NULL,
    imagem        TEXT   NOT NULL,
    criado_em     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (barbearia_id) REFERENCES barbearia(id)      ON DELETE CASCADE,
    FOREIGN KEY (chave_id)     REFERENCES chave_conteudo(id) ON DELETE CASCADE,
    UNIQUE (barbearia_id, chave_id)
);

/*--------------------------------------------------------------
  PROFISSIONAL_SERVICO  (tabela ASSOCIATIVA M-M)
--------------------------------------------------------------*/
CREATE TABLE profissional_servico (
    id               TEXT    NOT NULL PRIMARY KEY,        -- UUID
    profissional_id  TEXT    NOT NULL,
    servico_id       TEXT    NOT NULL,
    duracao_min      INTEGER,
    preco_especial   NUMERIC,
    FOREIGN KEY (profissional_id) REFERENCES profissional(id) ON DELETE CASCADE,
    FOREIGN KEY (servico_id)      REFERENCES servico(id)      ON DELETE CASCADE,
    UNIQUE (profissional_id, servico_id)
);

COMMIT;
PRAGMA foreign_keys = ON;        -- reativa FKs
