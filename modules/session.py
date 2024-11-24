from langchain.schema import AIMessage, HumanMessage


class SessionManager:
    
    '''
    Classe para gerenciamento de sessões
      variavel sessions: dicionário para armazenar sessões
      func get_context: Recupera o contexto da sessão ou inicializa uma nova.
      func update_context: Adiciona uma mensagem ao contexto da sessão.
      func get_formatted_context: Retorna o contexto formatado como string
    '''
    def __init__(self):
        # Dicionário para armazenar sessões
        self.sessions = {}

    def get_context(self, session_id):
        """Recupera o contexto da sessão ou inicializa uma nova."""
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        return self.sessions[session_id]

    def update_context(self, session_id, role, message):
        """Adiciona uma mensagem ao contexto da sessão."""
        context = self.get_context(session_id)
        msg = AIMessage(content=message) if role == "assistant" else HumanMessage(content=message)
        context.append(msg)
        self.sessions[session_id] = context
        return context

    def get_formatted_context(self, session_id):
        """Retorna o contexto formatado como string."""
        context = self.get_context(session_id)
        if not context:
            return "No context"
        return "\n\n".join([f"{msg.type}: {msg.content}" for msg in context])
