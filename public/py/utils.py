import random
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import textwrap
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

# Inicializa o lematizador
lemmatizer = WordNetLemmatizer()

# Certifique-se de que os pacotes necessários do NLTK foram baixados
nltk.download('stopwords')
nltk.download('wordnet')

def validar_saida(pergunta):
    """Valida se o usuário deseja sair do chatbot."""
    palavras_de_saida = ["sair", "encerrar", "tchau", "fechar", "quero sair"]
    return any(palavra in pergunta.lower().strip() for palavra in palavras_de_saida)


def gerar_resposta_aleatoria():
    """Retorna uma resposta aleatória para interação com o usuário."""
    respostas_aleatorias = [
        "Entendi, deixe-me ajudar você com isso.",
        "Boa pergunta! Olha só como isso funciona.",
        "Claro! Deixe-me esclarecer para você.",
        "Ótima pergunta.",
        "Vou verificar as informações para você, um momento."
    ]
    return random.choice(respostas_aleatorias)

def gerar_mensagem_despedida():
    """Retorna uma mensagem de despedida aleatória."""
    mensagens_despedida = [
        "Agradecemos por conversar com a Tech4Con! Se precisar de mais alguma coisa, estamos à disposição. Tenha um excelente dia!",
        "Obrigado por entrar em contato com a Tech4Con. Esperamos ter ajudado! Se tiver mais dúvidas, não hesite em nos procurar. Até a próxima!",
        "Foi um prazer falar com você! A equipe Tech4Con está sempre aqui para ajudar. Tenha um ótimo dia!",
        "Agradecemos seu contato com a Tech4Con! Qualquer dúvida futura, conte com a gente. Até logo!"
    ]
    return random.choice(mensagens_despedida)

def gerar_mensagem_contato():
    """Retorna uma mensagem com informações de contato para um vendedor."""
    mensagem_contato = (
        "Se precisar de mais informações ou desejar falar com um de nossos vendedores, "
        "entre em contato pelo e-mail: vendas@tech4con.com ou ligue para (11) 1234-5678. "
        "Estamos aqui para ajudar com o que precisar!"
    )
    return mensagem_contato

def normalizar_pergunta(pergunta):
    """Normaliza a pergunta removendo stopwords e lematizando as palavras."""
    stop_words = set(stopwords.words('portuguese'))
    palavras = pergunta.lower().split()
    palavras_filtradas = [lemmatizer.lemmatize(palavra) for palavra in palavras if palavra not in stop_words]
    return ' '.join(palavras_filtradas)

def format_response(response, width=80):
    """
    Formata o texto para torná-lo mais legível, respeitando quebras de linha e listas.
    """
    lines = response.split("\n")
    formatted_lines = []
    for line in lines:
        if line.strip().startswith("-") or line.strip().startswith("*"):  # Detecta listas
            formatted_lines.append(f"• {line.strip()[1:].strip()}")
        elif line.strip():
            formatted_lines.append(textwrap.fill(line.strip(), width=width))  # Quebra linhas longas
    return "\n".join(formatted_lines)

def truncate_response(response, max_length=500):
    """
    Limita o comprimento da resposta para evitar textos muito extensos.
    """
    if len(response) > max_length:
        return response[:max_length] + "\n\n...[Resposta truncada para brevidade]"
    return response

