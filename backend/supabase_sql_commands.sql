-- Comandos SQL para executar no Supabase SQL Editor
-- Acesse: https://supabase.com/dashboard/project/mdbmrxzfliwlqgalcvan/sql

-- Criar enum para status de solicitação
CREATE TYPE status_solicitacao AS ENUM (
    'aguardando_orcamentos',
    'com_orcamentos', 
    'fechada',
    'cancelada'
);

-- Criar enum para status de orçamento
CREATE TYPE status_orcamento AS ENUM (
    'aguardando',
    'aceito',
    'recusado',
    'realizado'
);

-- Criar tabela de clientes
CREATE TABLE IF NOT EXISTS clientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    telefone VARCHAR(20),
    cpf VARCHAR(255),
    endereco TEXT,
    avaliacao_media FLOAT DEFAULT 0.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Criar tabela de prestadores
CREATE TABLE IF NOT EXISTS prestadores (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    telefone VARCHAR(20),
    cpf_cnpj VARCHAR(255),
    categorias JSONB DEFAULT '[]'::jsonb,
    regioes_atendimento JSONB DEFAULT '[]'::jsonb,
    avaliacao_media FLOAT DEFAULT 0.0,
    portfolio JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Criar tabela de solicitações
CREATE TABLE IF NOT EXISTS solicitacoes (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER NOT NULL REFERENCES clientes(id),
    categoria VARCHAR(100) NOT NULL,
    descricao TEXT NOT NULL,
    localizacao VARCHAR(255) NOT NULL,
    prazo_desejado VARCHAR(100),
    informacoes_adicionais TEXT,
    status status_solicitacao DEFAULT 'aguardando_orcamentos',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Criar tabela de orçamentos
CREATE TABLE IF NOT EXISTS orcamentos (
    id SERIAL PRIMARY KEY,
    solicitacao_id INTEGER NOT NULL REFERENCES solicitacoes(id),
    prestador_id INTEGER NOT NULL REFERENCES prestadores(id),
    valor_ml_minimo FLOAT NOT NULL,
    valor_ml_sugerido FLOAT NOT NULL,
    valor_ml_maximo FLOAT NOT NULL,
    valor_proposto FLOAT NOT NULL,
    prazo_execucao VARCHAR(100) NOT NULL,
    observacoes TEXT,
    condicoes TEXT,
    status status_orcamento DEFAULT 'aguardando',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Criar tabela de avaliações
CREATE TABLE IF NOT EXISTS avaliacoes (
    id SERIAL PRIMARY KEY,
    orcamento_id INTEGER NOT NULL REFERENCES orcamentos(id),
    cliente_id INTEGER NOT NULL REFERENCES clientes(id),
    prestador_id INTEGER NOT NULL REFERENCES prestadores(id),
    estrelas INTEGER NOT NULL CHECK (estrelas >= 1 AND estrelas <= 5),
    comentario TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Criar índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_clientes_email ON clientes(email);
CREATE INDEX IF NOT EXISTS idx_prestadores_email ON prestadores(email);
CREATE INDEX IF NOT EXISTS idx_solicitacoes_categoria ON solicitacoes(categoria);
CREATE INDEX IF NOT EXISTS idx_solicitacoes_status ON solicitacoes(status);
CREATE INDEX IF NOT EXISTS idx_orcamentos_status ON orcamentos(status);

-- Verificar se as tabelas foram criadas
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
ORDER BY table_name;


ALTER TABLE clientes ADD COLUMN IF NOT EXISTS totp_secret VARCHAR(255);
ALTER TABLE prestadores ADD COLUMN IF NOT EXISTS totp_secret VARCHAR(255);