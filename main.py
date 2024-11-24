import time
from modules.workflow import WorkflowManager
# Configuração inicial
qdrant_url = "http://localhost:6333"
qdrant_collection = "content"

# Inicializar o WorkflowManager
workflow = WorkflowManager(qdrant_url, qdrant_collection)

# Testando com uma sessão
session_id = "user123"
print(workflow.handle_question(session_id, "Olá, como vai você?"))
time.sleep(1)
print(workflow.handle_question(session_id, "Porque empresas empresas icnlusivas são vistas como boas para trabalhar?"))
