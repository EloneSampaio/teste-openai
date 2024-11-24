import os

import qdrant_client
from qdrant_client.models import Filter, FieldCondition, MatchValue, FilterSelector
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from pprint import pprint
from langchain_openai import ChatOpenAI



from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

PDFS_TO_LOAD = "./data/pdfs"
CATEGORIES = [
    "additional_topics",
    "challenges_and_solutions",
    "laws_and_regulations",
    "types_of_disabilities",
    "workplace_inclusion",
]

# Configuração do modelo GPT
llm = ChatOpenAI(
    model="gpt-3.5-turbo", 
    temperature=0  # Ajuste de temperatura para respostas consistentes
)

prompt = PromptTemplate(
    template="""Conduct a comprehensive analysis of the CONTENT provided and categorize into one of the following categories:
    additional_topics: 
    - Refere-se a temas que abrangem tópicos gerais ou adicionais relacionados à inclusão de pessoas com deficiência, como a história das lutas e conquistas dessas pessoas, e a diferença entre emprego e inclusão verdadeira.

    challenges_and_solutions: 
    - Envolve a discussão sobre os desafios enfrentados na inclusão de pessoas com deficiência, como a remoção de barreiras físicas e atitudinais, além de apresentar possíveis soluções para aumentar a retenção de empregados com deficiência.

    laws_and_regulations: 
    - Trata dos aspectos legais que garantem a inclusão de pessoas com deficiência, como a Lei de Cotas, e enfatiza a responsabilidade das empresas em seguir essas leis, além da importância de políticas públicas que assegurem igualdade de oportunidades.

    types_of_disabilities: 
    - Discute os diferentes tipos de deficiências, incluindo físicas, auditivas, visuais, mentais e múltiplas, e a importância de compreender essas condições para promover inclusão e acessibilidade.

    workplace_inclusion: 
    - Foca nas práticas e estratégias que promovem a inclusão de pessoas com deficiência no ambiente de trabalho, abordando modalidades de contratação e a necessidade de um ambiente acessível e inclusivo.


    Output a single category only from the types ('additional_topics', 'challenges_and_solutions', 'laws_and_regulations', 'types_of_disabilities' e 'workplace_inclusion') and no preamble or explanation.

    CONTENT: {content}
        """,
        input_variables=["content"]
)

# Parser para formatar a saída do modelo
output_parser = StrOutputParser()


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=3950,
    chunk_overlap=200,
    separators=["\n\n", "\n", "(?<=. )", " ", ""]
)

qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")

# Criando o cliente Qdrant
client = qdrant_client.QdrantClient(qdrant_url)

# Verifica se a coleção existe. Se não, cria a coleção
try:
    if "content" not in client.get_collections():
        client.create_collection(
            collection_name="content",
            vectors_config=qdrant_client.models.VectorParams(
                size=768,  # Substitua pelo tamanho correto do seu vetor
                distance='Cosine'
            )
        )
        pprint("Collection 'content' created.")
    else:
        pprint("Collection 'content' already exists.")
except Exception as e:
    pprint(f"Error checking or creating collection: {e}")

# Configuração do Qdrant com LangChain
db = Qdrant(
    client=client,
    embeddings=embeddings,
    collection_name="content"
)

# Criação do Snapshot (backup) da coleção 'content'
try:
    if "content" not in client.get_collections():
        snapshot_info = client.create_snapshot(collection_name="content")
        snapshot_url = f"{qdrant_url}/collections/content/snapshots/{snapshot_info.name}"

        pprint(f"Snapshot created! You can download it from: {snapshot_url}")
    else:
      pass
except Exception as e:
    pprint(f"Error creating snapshot: {e}")

# Processamento dos PDFs
for category in CATEGORIES:
    category_path = os.path.join(PDFS_TO_LOAD, category)
    
    # Verificar se o caminho da categoria existe
    if not os.path.exists(category_path):
        pprint(f"Directory does not exist: {category_path}")
        continue  # Pular para a próxima categoria

    pdf_files = [os.path.join(category_path, file) for file in os.listdir(category_path) if file.endswith('.pdf')]

    for pdf_file in pdf_files:
        chunks = []
        pprint(f"Deleting previous {pdf_file}...")
        file_name = pdf_file.split("/")[-1]
        db.client.delete(
            collection_name="content", 
            points_selector= FilterSelector(
                filter=Filter(
                    must=[
                        FieldCondition(
                            key="metadata.source",
                            match=MatchValue(value=file_name),
                        ),
                    ],
                )
            ))

        pprint(f"Loading {pdf_file}...")
        loader = PyPDFLoader(pdf_file)
        file_chunks = loader.load_and_split(text_splitter=text_splitter)
        
        # Preparar os chunks para enviar ao Qdrant
        for chunk in file_chunks:

            category = llm(prompt.format(content=chunk.page_content))

            chunk.metadata["source"] = file_name
            chunk.metadata["category"] = category
            chunks.append(chunk)

        pprint(f"Loading {len(chunks)} to Qdrant...")
        # Carregar os chunks no Qdrant
        qdrant = Qdrant.from_documents(
            documents=chunks,
            embedding=embeddings,
            url="http://localhost:6333",
            collection_name="content"
        )