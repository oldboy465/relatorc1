CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS bases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    caminho_pasta TEXT NOT NULL UNIQUE,
    store_id TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sincronizado_em TIMESTAMP
);

CREATE TABLE IF NOT EXISTS documentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    base_id INTEGER NOT NULL,
    nome TEXT NOT NULL,
    caminho_completo TEXT NOT NULL UNIQUE,
    extensao TEXT NOT NULL,
    tamanho INTEGER NOT NULL,
    hash_sha256 TEXT NOT NULL,
    data_modificacao TIMESTAMP NOT NULL,
    gemini_file_uri TEXT,
    status TEXT DEFAULT 'pendente',
    indexado_em TIMESTAMP,
    FOREIGN KEY (base_id) REFERENCES bases (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS historico_consultas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    base_id INTEGER NOT NULL,
    pergunta TEXT NOT NULL,
    resposta TEXT NOT NULL,
    fontes_json TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (base_id) REFERENCES bases (id) ON DELETE CASCADE
);
"""