from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

class HardMessages:
    '''
    Classe para identificar saudações e agradecimentos.
       param llm: Modelo OpenAI
       
    '''
    def __init__(self):
        # Define os prompts de classificação
        #self.openai_llm = llm # Modelo OpenAI
        #self.greeting_system_prompt = "You are a helpful assistant that identifies greetings in any language. Respond with 'yes' or 'no' only, without any explanation."
        #self.thank_system_prompt = "You are a helpful assistant that identifies thanks in any language. Respond with 'yes' or 'no' only, without any explanation."

         # Define o prompt do sistema
        self.system_prompt = (
            "You are a helpful assistant that categorizes user messages into specific categories in multiple languages."
            "and provides an appropriate response in the same language as the input message (português)."
        )
      
            
    def _call_openai(self, user_input):
            """Chama a API da OpenAI com o prompt fornecido."""
            
            try:
                self.human_prompt = (
                f"""Classify the following message into the following categories:
                    - 'saudação': The message is a greeting (e.g., 'hello', 'hi', 'hola', 'olá').
                    - 'agradecimento': The message is an expression of thanks (e.g., 'thank you', 'gracias', 'obrigado').
                    - 'off-topic': The message is unrelated to the context (e.g., asking irrelevant questions).

                    Respond in the following JSON format:
                    {{
                    "saudação": "Sim" or "Não",
                    "agradecimento": "Sim" or "Não",
                    "off-topic": "Sim" or "Não",
                    "resposta": "Provide an appropriate response in the same language as the input."
                    }}

                    Ensure:
                    - If 'saudação' is "Sim", respond with a friendly greeting in the same language, such as "Olá, como posso ajudar?" (Portuguese), "Hola, ¿cómo puedo ayudarte?" (Spanish), or "Hello! How can I help you?" (English).
                    - If 'agradecimento' is "Sim", respond with a polite acknowledgment in the same language, such as "De nada! Estou à disposição." (Portuguese), "De nada, avísame si necesitas algo más." (Spanish), or "You're welcome! Let me know if you need anything else." (English).
                    - If 'off-topic' is "Sim", respond with a clarification request in the same language, such as "Parece estar fora do tópico. Você pode fornecer mais contexto?" (Portuguese), "Parece que esto no está relacionado. ¿Puedes proporcionar más contexto?" (Spanish), or "This seems unrelated. Can you provide more context?" (English).

                    Message: {user_input}
                    """
            )


                # Use o endpoint correto
                openai_llm = ChatOpenAI(model="gpt-4", temperature=0)  # Certifique-se de usar o modelo correto

                # Prepara as mensagens no formato correto
                messages = [
                    SystemMessage(content=self.system_prompt),
                    HumanMessage(content=self.human_prompt),
                ]

                # Chama o modelo
                response = openai_llm(messages=messages)
                return response.content.strip()
            except Exception as e:
                print(f"Erro ao chamar a API OpenAI: {e}")
                return None

    def greetings(self, user_input):
        """Identifica se a entrada do usuário é uma saudação."""
        system_prompt = self.greeting_system_prompt
        prompt = f"Here is the message: {user_input}"
        response = self._call_openai(system_prompt, prompt)

        print(f"Resposta da API: {response}")
        is_greeting = response.lower() == "yes"
        return {"is_greeting": is_greeting, "response": response}

    def thanks(self, user_input):
        """Identifica se a entrada do usuário é um agradecimento."""
        system_prompt = self.thank_system_prompt
        prompt = f"Is this a thank you? {user_input}"
        response = self._call_openai(system_prompt, prompt)

        print(f"Resposta da API: {response}")
        is_thanks = response.lower() == "yes"
        return {"is_thanks": is_thanks, "response": response}
    
    def categorize_message(self, user_input):
        """Identifica se a entrada do usuário é um agradecimento."""
        response = self._call_openai( user_input)

        print(f"Resposta da API: {response}")
        
        return {"response": response}

    def no_content(self):
        return "I'm sorry, I'm not sure what you're asking. Can you rephrase your question?"

    def working(self):
        return "It's working"
