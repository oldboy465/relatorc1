import json
from database.database import get_db_connection
from services.gemini_service import get_client, query_gemini_with_context

def execute_rag_query(base_id: int, prompt: str) -> dict:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM documentos WHERE base_id = ? AND status = 'indexado'", (base_id,))
    documentos = cursor.fetchall()

    if not documentos:
        conn.close()
        return {
            "resposta": "Nenhum documento indexado encontrado nesta base. Por favor, execute a sincronização primeiro.",
            "fontes": []
        }

    client = get_client()
    gemini_file_objects = []
    fontes_disponiveis = []

    for doc in documentos:
        try:
            remote_file = client.files.get(name=doc["gemini_file_uri"])
            gemini_file_objects.append(remote_file)
            fontes_disponiveis.append(doc["nome"])
        except Exception:
            continue

    resultado = query_gemini_with_context(prompt, gemini_file_objects)
    resposta_texto = resultado["text"]

    cursor.execute("""
        INSERT INTO historico_consultas (base_id, pergunta, resposta, fontes_json)
        VALUES (?, ?, ?, ?)
    """, (base_id, prompt, resposta_texto, json.dumps(fontes_disponiveis)))
    
    conn.commit()
    conn.close()

    return {
        "resposta": resposta_texto,
        "fontes": fontes_disponiveis
    }