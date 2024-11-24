from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from jinja2 import Environment, FileSystemLoader



# Carregar o template de um arquivo externo
def load_template(template_file):
    env = Environment(loader=FileSystemLoader("."))  # Carrega templates do diretório atual
    return env.get_template(template_file)

def get_category_generator(template_file,llm):
    template = load_template("../templates/categorizer_prompt.jinja")
    prompt = PromptTemplate(
        template=template.render(),
        input_variables=["context", "message"],
    )
    return prompt | llm | StrOutputParser()