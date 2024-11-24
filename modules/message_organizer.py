from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from jinja2 import Environment, FileSystemLoader

class MessageCategorizer:
    def __init__(self, openai_model="gpt-4"):
        self.llm = ChatOpenAI(model=openai_model, temperature=0)

# Carregar o template de um arquivo externo
    def load_template(self,template_file):
        env = Environment(loader=FileSystemLoader("templates"))  # Carrega templates do diretório atual
        return env.get_template(template_file)
    def categorize(self, message,context):
        """Classifica uma mensagem em categorias como saudação, agradecimento ou off-topic."""
        """ prompt = (
            "Classify the following message into one of the following categories:\n"
            "- 'saudação': The message is a greeting.\n"
            "- 'agradecimento': The message is a thank-you.\n"
            "- 'off-topic': The message is unrelated to the context.\n"
            "Message: {message}\n"
            "Respond with only the category name."
        ) """
        template = self.load_template("categorizer_prompt.jinja")
        # Renderiza o template com os dados fornecidos
        prompt = template.render(message=message,context=context)
        
        response = self.llm([HumanMessage(content=prompt)])
        return response.content.strip()
    
    
    def categorize_greeting_or_thanks(self, message):
        """Verifica se a mensagem é uma saudação ou agradecimento."""
        # Carrega o template Jinja específico para saudações e agradecimentos
        template = self.load_template("greetings_thanks_prompt.jinja")

        # Renderiza o template com os dados fornecidos
        prompt = template.render(message=message)

        # Envia o prompt para o modelo
        response = self.llm([HumanMessage(content=prompt)])
        return response.content.strip()
