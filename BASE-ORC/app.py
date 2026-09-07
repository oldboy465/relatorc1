from flask import Flask, render_template, request, jsonify
from config import DEFAULT_STORAGE_DIR
from database.database import init_db, get_db_connection
from services.sync_service import sync_base_documents
from services.rag_service import execute_rag_query

app = Flask(__name__)

@app.route("/")
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bases ORDER BY criado_em DESC")
    bases = cursor.fetchall()
    
    if not bases and DEFAULT_STORAGE_DIR.exists():
        cursor.execute(
            "INSERT INTO bases (nome, caminho_pasta) VALUES (?, ?)",
            ("Base Orçamento Oficial", str(DEFAULT_STORAGE_DIR))
        )
        conn.commit()
        cursor.execute("SELECT * FROM bases ORDER BY criado_em DESC")
        bases = cursor.fetchall()

    conn.close()
    return render_template("index.html", bases=bases)

@app.route("/api/base/<int:base_id>/stats", methods=["GET"])
def get_base_stats(base_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bases WHERE id = ?", (base_id,))
    base = cursor.fetchone()
    
    if not base:
        conn.close()
        return jsonify({"error": "Base não encontrada"}), 404

    cursor.execute("SELECT COUNT(*) as total FROM documentos WHERE base_id = ?", (base_id,))
    total = cursor.fetchone()["total"]
    
    cursor.execute("SELECT COUNT(*) as indexados FROM documentos WHERE base_id = ? AND status = 'indexado'", (base_id,))
    indexados = cursor.fetchone()["indexados"]
    
    conn.close()
    return jsonify({
        "nome": base["nome"],
        "caminho": base["caminho_pasta"],
        "sincronizado_em": base["sincronizado_em"] or "Nunca",
        "total_documentos": total,
        "indexados": indexados
    })

@app.route("/api/sync/<int:base_id>", methods=["POST"])
def sync_base(base_id):
    try:
        resultado = sync_base_documents(base_id)
        return jsonify({"success": True, "resultado": resultado})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/ask", methods=["POST"])
def ask_question():
    data = request.get_json() or {}
    base_id = data.get("base_id")
    pergunta = data.get("prompt", "").strip()

    if not base_id or not pergunta:
        return jsonify({"error": "Parâmetros 'base_id' e 'prompt' são obrigatórios."}), 400

    try:
        resposta = execute_rag_query(int(base_id), pergunta)
        return jsonify(resposta)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)