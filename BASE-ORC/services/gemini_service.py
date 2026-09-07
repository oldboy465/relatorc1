import os
import time
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, DEFAULT_MODEL

def get_client() -> genai.Client:
    api_key = GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Chave da API Gemini não encontrada. Verifique api.txt ou as variáveis de ambiente.")
    return genai.Client(api_key=api_key)

def upload_file_to_gemini(filepath: str):
    client = get_client()
    uploaded_file = client.files.upload(file=filepath)
    
    # Aguarda o processamento do arquivo pelo Gemini (necessario para PDFs e planilhas)
    while uploaded_file.state.name == "PROCESSING":
        time.sleep(2)
        uploaded_file = client.files.get(name=uploaded_file.name)
        
    if uploaded_file.state.name == "FAILED":
        raise RuntimeError(f"Falha no processamento do arquivo no Gemini: {filepath}")
        
    return uploaded_file

def query_gemini_with_context(prompt: str, gemini_files: list, model: str = DEFAULT_MODEL) -> dict:
    client = get_client()
    
    system_instruction = (
        "Você é um assistente técnico e analista orçamentário. "
        "Responda exclusivamente com base nos dados presentes nos documentos anexados. "
        "Se a informação exata não constar nos arquivos, afirme categoricamente que o dado não foi localizado. "
        "Nunca deduza, extrapole ou invente números, valores ou rubricas orçamentárias. "
        "Sempre indique expressamente em quais arquivos ou trechos a informação foi encontrada."
    )
    
    contents = list(gemini_files) + [prompt]
    
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.1
        )
    )
    
    return {
        "text": response.text,
        "raw_response": response
    }