@echo off
chcp 65001 > nul
echo ======================================================
echo   Inicializando Estrutura RAG RelatOrc
echo ======================================================

:: Criacao das pastas
if not exist "services" mkdir services
if not exist "database" mkdir database
if not exist "templates" mkdir templates
if not exist "static\css" mkdir static\css
if not exist "static\js" mkdir static\js
if not exist "data" mkdir data

echo Diretórios validados.

:: Criacao de arquivos raiz
if not exist "app.py" (type nul > "app.py" & echo Criado: app.py)
if not exist "config.py" (type nul > "config.py" & echo Criado: config.py)
if not exist "requirements.txt" (type nul > "requirements.txt" & echo Criado: requirements.txt)
if not exist ".gitignore" (
    (
        echo venv/
        echo __pycache__/
        echo *.pyc
        echo .env
        echo api.txt
        echo data/*.db
    ) > ".gitignore"
    echo Criado: .gitignore
)

:: Criacao dos servicos
if not exist "services\gemini_service.py" (type nul > "services\gemini_service.py" & echo Criado: services\gemini_service.py)
if not exist "services\rag_service.py" (type nul > "services\rag_service.py" & echo Criado: services\rag_service.py)
if not exist "services\file_service.py" (type nul > "services\file_service.py" & echo Criado: services\file_service.py)
if not exist "services\sync_service.py" (type nul > "services\sync_service.py" & echo Criado: services\sync_service.py)

:: Criacao dos modulos de banco
if not exist "database\database.py" (type nul > "database\database.py" & echo Criado: database\database.py)
if not exist "database\models.py" (type nul > "database\models.py" & echo Criado: database\models.py)

:: Criacao dos arquivos de interface
if not exist "templates\index.html" (type nul > "templates\index.html" & echo Criado: templates\index.html)
if not exist "static\css\style.css" (type nul > "static\css\style.css" & echo Criado: static\css\style.css)
if not exist "static\js\app.js" (type nul > "static\js\app.js" & echo Criado: static\js\app.js)

echo ======================================================
echo   Estrutura criada com sucesso!
echo ======================================================
pause