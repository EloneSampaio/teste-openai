from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
class AnswerGenerator:
    '''
    Classe para gerar respostas com base na mensagem do usuário e no contexto.
       param llm: Modelo OpenAI
       variavel llm: Modelo OpenAI
       func generate: Gera uma resposta baseada na mensagem do usuário e no contexto.
       
    '''
    def __init__(self, openai_model="gpt-4"):
        self.llm = ChatOpenAI(model=openai_model, temperature=0)

    def generate(self, user_message, context_text):
        """Gera uma resposta baseada na mensagem do usuário e no contexto."""
        prompt = (
            "User asked: {message}\n"
            "Here is the relevant context:\n{context}\n"
            "Provide a helpful and accurate response based on the context."
        )
        messages = [
            HumanMessage(content=prompt.format(message=user_message, context=context_text))
        ]
        response = self.llm(messages)
        return response.content.strip()
