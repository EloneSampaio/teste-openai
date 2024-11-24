from modules.session import SessionManager
from content.retriever import QdrantSearch
from modules.message_organizer import MessageCategorizer
from content.generator import AnswerGenerator

class WorkflowManager:
    def __init__(self, qdrant_url, collection_name, openai_model="gpt-4"):
        """
        Inicializa o gerenciador de fluxo de trabalho.

        Args:
            qdrant_url (str): URL do Qdrant.
            collection_name (str): Nome da coleção no Qdrant.
            openai_model (str): Modelo OpenAI a ser utilizado.
        """
        self.session_manager = SessionManager()
        self.qdrant_search = QdrantSearch(qdrant_url, collection_name)
        self.categorizer = MessageCategorizer(openai_model)
        self.answer_generator = AnswerGenerator(openai_model)

    def handle_question(self, session_id, user_message):
        """
        Fluxo principal para processar uma pergunta.

        Args:
            session_id (str): ID da sessão.
            user_message (str): Mensagem do usuário.

        Returns:
            dict: Resposta gerada e categoria identificada.
        """
        # Recuperar ou inicializar o contexto da sessão
        context = self.session_manager.get_context(session_id)
        if context:
            context_text = self.session_manager.get_formatted_context(session_id)
        else:
            context_text = "O usuário acabou de iniciar a conversa com o assistente."
            print(context_text)

        # Classificar a mensagem do usuário como saudação ou agradecimento
        greeting_or_thanks_category = self.categorizer.categorize_greeting_or_thanks(user_message)
        # remove '' on string
        greeting_or_thanks_category = greeting_or_thanks_category.replace("'", "")
        self.session_manager.update_context(session_id, "user", user_message)
        print(f"Categoria identificada: {greeting_or_thanks_category}")

        # Processar saudações ou agradecimentos
        if greeting_or_thanks_category == "saudacao":
            response = "Olá! Como posso ajudar?"
            self.session_manager.update_context(session_id, "assistant", response)
            return {"resposta": response, "categoria": greeting_or_thanks_category}

        elif greeting_or_thanks_category == "agradecimento":
            response = "De nada! Sempre à disposição."
            self.session_manager.update_context(session_id, "assistant", response)
            return {"resposta": response, "categoria": greeting_or_thanks_category}

        # Caso não seja saudação ou agradecimento, processar como outra categoria
        print("Categoria inicial não identificada como saudação ou agradecimento.")
        category = self.categorizer.categorize(user_message, context_text)
        # remove '' on string
        category = category.replace("'", "")
        print(f"Categoria identificada: {category}")

        # Responder a mensagens fora do tópico
        if category == "off-topic":
            response = "Isso parece estar fora do tópico. Você pode fornecer mais detalhes?"
            self.session_manager.update_context(session_id, "assistant", response)
            return {"resposta": response, "categoria": category}

        # Buscar informações no Qdrant para categorias relevantes
        search_results = []
        if category not in ["none", "off-topic"]:
            print("Buscando no Qdrant...")
            search_results = self.qdrant_search.search(user_message, category)
            print("Resultados encontrados no Qdrant:", search_results)

            if search_results:
                # Formatar o contexto para a geração de resposta
                context_text = "\n".join(
                    [
                        f"Fonte: {res['source']} (Página {res['page']})\nConteúdo: {res['page_content']}\n"
                        for res in search_results
                    ]
                )
                answer = self.answer_generator.generate(user_message, context_text)
                print("Resposta gerada com sucesso:", answer)
            else:
                print("Nenhum resultado relevante encontrado no Qdrant.")
                answer = "Desculpe, não consegui encontrar informações relevantes."
        else:
            print("Categoria inválida para busca no Qdrant.")
            answer = "Desculpe, não consegui processar sua solicitação."

        # Atualizar o contexto da sessão com a resposta gerada
        self.session_manager.update_context(session_id, "assistant", answer)
        return {
            "resposta": answer,
            "categoria": category,
            "resultados": search_results,
        }