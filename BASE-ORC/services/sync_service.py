from datetime import datetime
from database.database import get_db_connection
from services.file_service import scan_directory
from services.gemini_service import upload_file_to_gemini

def sync_base_documents(base_id: int) -> dict:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bases WHERE id = ?", (base_id,))
    base = cursor.fetchone()
    if not base:
        conn.close()
        raise ValueError("Base informada não foi encontrada.")

    pasta = base["caminho_pasta"]
    arquivos_locais = scan_directory(pasta)

    cursor.execute("SELECT * FROM documentos WHERE base_id = ?", (base_id,))
    registrados = {row["caminho_completo"]: dict(row) for row in cursor.fetchall()}

    stats = {"novos": 0, "atualizados": 0, "inalterados": 0, "removidos": 0}
    caminhos_vistos = set()

    for item in arquivos_locais:
        caminho = item["caminho_completo"]
        caminhos_vistos.add(caminho)

        if caminho not in registrados:
            upload_info = upload_file_to_gemini(caminho)
            cursor.execute("""
                INSERT INTO documentos 
                (base_id, nome, caminho_completo, extensao, tamanho, hash_sha256, data_modificacao, gemini_file_uri, status, indexado_em)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'indexado', ?)
            """, (
                base_id, item["nome"], caminho, item["extensao"], item["tamanho"],
                item["hash_sha256"], datetime.fromtimestamp(item["data_modificacao"]),
                upload_info.name, datetime.now()
            ))
            stats["novos"] += 1

        elif registrados[caminho]["hash_sha256"] != item["hash_sha256"]:
            upload_info = upload_file_to_gemini(caminho)
            cursor.execute("""
                UPDATE documentos 
                SET tamanho = ?, hash_sha256 = ?, data_modificacao = ?, 
                    gemini_file_uri = ?, status = 'indexado', indexado_em = ?
                WHERE caminho_completo = ?
            """, (
                item["tamanho"], item["hash_sha256"], 
                datetime.fromtimestamp(item["data_modificacao"]),
                upload_info.name, datetime.now(), caminho
            ))
            stats["atualizados"] += 1
        else:
            stats["inalterados"] += 1

    for caminho, doc in registrados.items():
        if caminho not in caminhos_vistos:
            cursor.execute("DELETE FROM documentos WHERE id = ?", (doc["id"],))
            stats["removidos"] += 1

    cursor.execute("UPDATE bases SET sincronizado_em = ? WHERE id = ?", (datetime.now(), base_id))
    conn.commit()
    conn.close()
    return stats