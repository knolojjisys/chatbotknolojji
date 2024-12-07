import openai
import logging
import pdfplumber
import threading  # Importa threading para configurar o temporizador
import sys  # Importa sys para encerrar o programa
import nltk
import os

import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"tesseract.exe"

import pytesseract
from PIL import Image
print("Instalação concluída e Tesseract configurado corretamente!")

# Verifica se os pacotes do NLTK já estão disponíveis antes de baixar
nltk_data_path = os.path.join(os.path.expanduser("~"), "nltk_data")
if not os.path.exists(nltk_data_path):
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('stopwords')
else:
    print("Pacotes do NLTK já estão disponíveis.")

from pdf_utils import extrair_texto_com_pdfplumber as extrair_texto_pdf, extrair_imagens_pdf, extrair_graficos_pdf
from utils import validar_saida, gerar_resposta_aleatoria, gerar_mensagem_despedida, gerar_mensagem_contato
from api_interaction import buscar_trecho_no_conteudo
from data_storage import salvar_interacao_txt
from config import CHAT_MODEL
from nlp_utils import normalizar_pergunta  # Importa a função de normalização

import pytesseract
from PIL import Image

# Configura o tempo limite (em segundos)
TEMPO_LIMITE = 5 * 60  # 5 minutos

# Certifique-se de que a chave da API está configurada corretamente
if not openai.api_key:
    logging.error("Erro: A chave da API não está configurada corretamente. Verifique o arquivo .env.")
    print("Erro: A chave da API não está configurada corretamente. Verifique o arquivo .env.")
    sys.exit()

# Função para encerrar o chat automaticamente
def encerrar_chat():
    print(gerar_mensagem_despedida())
    print(gerar_mensagem_contato())
    sys.exit()  # Encerra o programa completamente

def interagir_com_usuario(conteudo):
    """Controla o loop de interação com o usuário."""
    print("Olá! Estou aqui para ajudar você. Pergunte o que quiser sobre o documento!")
    cache_respostas = {}
    
    # Inicializa o temporizador
    temporizador = threading.Timer(TEMPO_LIMITE, encerrar_chat)
    temporizador.start()

    while True:
        pergunta = input("O que você gostaria de saber sobre o conteúdo? (Digite 'sair' para encerrar) ").strip().lower()
        
        # Reinicia o temporizador sempre que o usuário faz uma pergunta
        temporizador.cancel()
        temporizador = threading.Timer(TEMPO_LIMITE, encerrar_chat)
        temporizador.start()

        # Validação de saída
        if validar_saida(pergunta):
            print(gerar_mensagem_despedida())
            print(gerar_mensagem_contato())  # Exibe a mensagem de contato antes de sair
            break

        # Normaliza a pergunta para análise mais precisa
        pergunta_normalizada = normalizar_pergunta(pergunta)

        print(gerar_resposta_aleatoria())

        # Busca a resposta com a pergunta normalizada
        resposta = buscar_trecho_no_conteudo(conteudo, pergunta_normalizada, cache_respostas)
        if resposta:
            print(f"Resposta: {resposta}")
            # Salva a interação no arquivo de texto
            salvar_interacao_txt(pergunta, resposta)
        else:
            logging.error("Erro ao gerar a resposta. Verifique sua conexão com a API ou tente novamente mais tarde.")
            print("Erro ao gerar a resposta. Verifique sua conexão com a API ou tente novamente mais tarde.")

    # Cancela o temporizador ao sair do loop
    temporizador.cancel()
    sys.exit()  # Encerra o programa completamente

def main():
    """Função principal que coordena o fluxo do chatbot."""
    caminho_pdf = "teste.pdf"
    conteudo = extrair_texto_pdf(caminho_pdf)

    # Interruptor baseado na versão do modelo GPT
    print(f"Modelo configurado: {CHAT_MODEL}")  # Linha para debug
    usar_ocr = CHAT_MODEL.startswith("gpt-4o")  # Ativa o OCR e a extração de gráficos apenas se o modelo for gpt-4o

    # Log para verificar se o OCR e a extração de gráficos estão ativados ou não
    if usar_ocr:
        logging.info("OCR e extração de gráficos ativados porque o modelo GPT-4o foi detectado.")
    else:
        logging.info("OCR e extração de gráficos desativados porque o modelo GPT-3.5 está em uso.")

    if not conteudo and usar_ocr:  # Se não conseguiu extrair o texto e o OCR está ativado
        print("Tentando extrair texto das imagens com OCR...")
        imagens = extrair_imagens_pdf(caminho_pdf)
        conteudo = ""
        for imagem_path in imagens:
            conteudo += pytesseract.image_to_string(Image.open(imagem_path)) + "\n"

        # Tentando extrair gráficos
        print("Tentando extrair gráficos do PDF...")
        graficos = extrair_graficos_pdf(caminho_pdf)
        if graficos:
            print(f"Gráficos extraídos: {len(graficos)} gráficos salvos na pasta 'graficos_extraidos'.")

    if conteudo and conteudo.strip():  # Verifica se há algum texto extraído
        interagir_com_usuario(conteudo)
    else:
        logging.error(f"Não foi possível extrair texto do PDF: {caminho_pdf}")
        print(f"Não foi possível extrair texto do PDF: {caminho_pdf}")

if __name__ == "__main__":
    main()