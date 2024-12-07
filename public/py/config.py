import openai
import os
from dotenv import load_dotenv
import logging


# Configuração do logger
logging.basicConfig(
    filename='chatbot.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações da API da OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")  # Use a chave da API do arquivo .env
CHAT_MODEL = "gpt-3.5-turbo"

# Verificação se a chave da API foi carregada corretamente
if openai.api_key:
    logging.info("Chave da API carregada com sucesso!")
else:
    logging.error("Erro: Chave da API não encontrada! Verifique se está definida corretamente no arquivo .env.")


