from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer
from typing import List, Dict

class QdrantSearch:
    '''
    Classe para realizar buscas no Qdrant.
          param qdrant_url: URL do Qdrant.
          param collection_name: Nome da coleção no Qdrant.
          variavel qdrant: Cliente Qdrant.
          variavel collection_name: Nome da coleção no Qdrant.
          variavel embedding_model: modelo de embedding.
          
          func search: Realiza uma busca no Qdrant com base no query e categoria.
          
    '''
    def __init__(self, qdrant_url, collection_name):
        self.qdrant = QdrantClient(url=qdrant_url)
        self.collection_name = collection_name
        self.embedding_model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

    def search(self, query: str, category_filter: str, limit: int = 5) -> List[Dict]:
        """Realiza uma busca no Qdrant com base no query e categoria."""
        '''
          return
           [{
                source: Nome do arquivo
                page: Numero da pagina
                category: Categoria da pagina
                additional_info: Dicionario com informacoes adicionais
                response_metadata: Dicionario com metadados da resposta
                page_content: Conteudo da pagina
          }]
        '''
        query_vector = self.embedding_model.encode(query)
        
        query_filter = Filter(
            must=[
                FieldCondition(
                    key="metadata.category.content",  # Usamos o campo correto da categoria
                    match=MatchValue(value=category_filter),
                )
            ]
        )
        
        results = self.qdrant.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            query_filter=query_filter,
            with_payload=True,
            limit=limit,
        )
        
        # Retorna uma lista de payloads relevantes
        
        return [
            {
                "source": result.payload.get("metadata", {}).get("source"),
                "page": result.payload.get("metadata", {}).get("page"),
                "category": result.payload.get("metadata", {}).get("category", {}).get("content"),
                "additional_info": result.payload.get("metadata", {}).get("category", {}).get("additional_kwargs", {}),
                "response_metadata": result.payload.get("metadata", {}).get("response_metadata", {}),
                "page_content": result.payload.get("page_content", "No content found"),
                }

            for result in results
        ]