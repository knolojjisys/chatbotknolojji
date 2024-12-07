import openai
import logging
from config import CHAT_MODEL

def buscar_trecho_no_conteudo(conteudo, pergunta, cache_respostas):
    """Busca um trecho do conteúdo com base na pergunta usando a API da OpenAI."""
    
    # Verifica se a pergunta já está no cache
    if pergunta in cache_respostas:
        print("Buscando resposta no cache...")
        return cache_respostas[pergunta]

    # Limita o conteúdo do pdf se for muito longo (por exemplo, 4000 caracteres)
    max_conteudo_len = 10000
    if len(conteudo) > max_conteudo_len:
        print("O conteúdo é muito longo. Respondendo com base em um trecho parcial.")
        conteudo = conteudo[:max_conteudo_len] + "..."

    try:
        response = openai.ChatCompletion.create(
            model=CHAT_MODEL,
            messages=[
                {"role": "system", "content": "Você é um assistente que pode buscar e fornecer informações baseadas em textos."},
                {"role": "user", "content": f"Baseado no seguinte texto:\n\n{conteudo}\n\nResponda à pergunta: {pergunta}?"}
            ],
            max_tokens=800  # Limite de tokens para resposta
        )
        resposta = response['choices'][0]['message']['content'].strip()
        cache_respostas[pergunta] = resposta  # Armazenando a resposta no cache
        return resposta
    except openai.error.OpenAIError as e:
        logging.error(f"Erro na API da OpenAI: {e}")
        return "Desculpe, ocorreu um problema ao gerar a resposta. Tente novamente mais tarde."
    except Exception as e:
        logging.error(f"Erro inesperado: {e}")
        return "Um erro inesperado ocorreu. Verifique sua conexão ou tente novamente."
