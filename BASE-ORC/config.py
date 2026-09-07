import os
from pathlib import Path

# Raiz do projeto (onde o app.py reside)
BASE_DIR = Path(__file__).resolve().parent

# Busca da chave em api.txt (no diretorio atual ou na pasta pai 'Projeto Relatorc')
API_KEY_PATHS = [
    BASE_DIR / "api.txt",
    BASE_DIR.parent / "api.txt"
]

if not os.getenv("GEMINI_API_KEY"):
    for key_file in API_KEY_PATHS:
        if key_file.exists():
            with open(key_file, "r", encoding="utf-8") as f:
                chave = f.read().strip()
                if chave:
                    os.environ["GEMINI_API_KEY"] = chave
                    break

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Diretorio padrao da base documental
DEFAULT_STORAGE_DIR = BASE_DIR / "storage" / "bases" / "BASE-ORC"

# Banco SQLite local
DATABASE_PATH = BASE_DIR / "data" / "rag.db"

# Modelo base para geracao e busca semantica
DEFAULT_MODEL = "gemini-1.5-pro"