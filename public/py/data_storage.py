import os
import logging
from datetime import datetime

# Configuração de logging para registrar mensagens de informação e erros
logging.basicConfig(level=logging.INFO)

# Define o caminho da pasta onde os arquivos de texto serão salvos
PASTA_TXT = os.path.join(os.getcwd(), "historico_txt")
os.makedirs(PASTA_TXT, exist_ok=True)  # Cria a pasta se ela não existir

# Função para salvar interações em um arquivo de texto separado por dia
def salvar_interacao_txt(pergunta, resposta):
    """Salva a pergunta e a resposta em um arquivo de texto separado por dia, com data e hora."""
    # Captura a data atual para o nome do arquivo
    data_atual = datetime.now().strftime("%Y-%m-%d")
    nome_arquivo = os.path.join(PASTA_TXT, f"historico_{data_atual}.txt")

    # Captura a hora da interação
    horario_interacao = datetime.now().strftime("%H:%M:%S")

    try:
        with open(nome_arquivo, "a", encoding="utf-8") as arquivo:
            arquivo.write(f"Data e Hora: {data_atual} {horario_interacao}\n")
            arquivo.write("Pergunta do Usuário:\n")
            arquivo.write(pergunta + "\n")
            arquivo.write("Resposta do Chat:\n")
            arquivo.write(resposta + "\n")
            arquivo.write("-" * 50 + "\n")  # Separador visual entre interações
        
        logging.info("Interação salva no arquivo de texto.")
    except Exception as e:
        logging.error(f"Erro ao salvar interação no arquivo de texto: {e}")

# Função para exibir o conteúdo do arquivo de texto do dia no console do Jupyter
def exibir_conteudo_txt():
    """Exibe o conteúdo do arquivo de texto do dia no console do Jupyter."""
    data_atual = datetime.now().strftime("%Y-%m-%d")
    caminho_arquivo = os.path.join(PASTA_TXT, f"historico_{data_atual}.txt")
    
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
            print(conteudo)
    else:
        print("O arquivo do dia não foi encontrado.")

# Exemplo de como usar as funções
if __name__ == "__main__":
    # Simulação de interações
    salvar_interacao_txt("Qual é a capital da França?", "A capital da França é Paris.")
    salvar_interacao_txt("Quem escreveu 'Dom Casmurro'?", "O livro 'Dom Casmurro' foi escrito por Machado de Assis.")
    
    # Exibir o conteúdo do arquivo de texto do dia
    exibir_conteudo_txt()
