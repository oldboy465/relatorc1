import hashlib
from pathlib import Path

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".xlsx", ".txt", ".pptx"}

def compute_sha256(filepath: Path) -> str:
    sha = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            sha.update(chunk)
    return sha.hexdigest()

def scan_directory(directory_path: str | Path) -> list[dict]:
    path = Path(directory_path)
    if not path.is_dir():
        raise ValueError(f"Diretório inexistente ou inacessível: {directory_path}")

    documents = []
    for item in path.iterdir():
        if item.is_file() and item.suffix.lower() in SUPPORTED_EXTENSIONS:
            stat = item.stat()
            documents.append({
                "nome": item.name,
                "caminho_completo": str(item.resolve()),
                "extensao": item.suffix.lower(),
                "tamanho": stat.st_size,
                "data_modificacao": stat.st_mtime,
                "hash_sha256": compute_sha256(item)
            })
    return documents