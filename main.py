import time
from modules.workflow import WorkflowManager
# Configuração inicial
qdrant_url = "http://localhost:6333"
qdrant_collection = "content"
session_id = "user123"

def chat(session_id: str, user_message: str):
# Inicializar o WorkflowManager
    workflow = WorkflowManager(qdrant_url, qdrant_collection)

    # Testando com uma sessão
    
    print(workflow.handle_question(session_id, user_message))
    
    
# Testando função principal
""" 
from flask import Flask

app = Flask(__name__)

@app.route("/chat")
def start_conversatation(session_id: str, user_message: str):
    return chat(session_id, user_message) """
    
#chat(session_id, "Olá, bom dia")
chat(session_id, "Porque empresas icnlusivas são vistas como boas para trabalhar?")

