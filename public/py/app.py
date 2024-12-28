import os
from flask import Flask, request, jsonify
from flask_cors import CORS
# Importar suas funções
from pdf_utils import extrair_texto_com_pdfplumber as extrair_texto_pdf  
from api_interaction import buscar_trecho_no_conteudo
from utils import normalizar_pergunta

app = Flask(__name__)
CORS(app)

# Configuração do caminho para os PDFs
CAMINHO_PDFS = "public/pdfs/"

@app.route('/', methods=['GET'])
def home():
    return "Bem-vindo ao Chatbot Knolojji! O backend está funcionando."

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    question = data.get("question")
    product = data.get("product")

    print(f"Recebido: question={question}, product={product}")

    if not question or not product:
        return jsonify({"answer": "Pergunta ou produto inválido!"}), 400

    # Gera o caminho completo para o arquivo PDF
    nome_arquivo = f"{product}.pdf"
    caminho_completo = os.path.join(CAMINHO_PDFS, nome_arquivo)

    print(f"Procurando arquivo em: {caminho_completo}")

    # Verifica se o arquivo PDF existe
    if not os.path.exists(caminho_completo):
        print("Arquivo não encontrado!")
        return jsonify({"answer": f"PDF do produto '{product}' não encontrado!"}), 404

    # Extrai o conteúdo do PDF
    try:
        conteudo = extrair_texto_pdf(caminho_completo)
    except Exception as e:
        print(f"Erro ao processar o PDF: {str(e)}")
        return jsonify({"answer": f"Erro ao processar o PDF: {str(e)}"}), 500

    print("PDF processado com sucesso!")
    
    # Normaliza a pergunta e busca a resposta
    pergunta_normalizada = normalizar_pergunta(question)
    resposta = buscar_trecho_no_conteudo(conteudo, pergunta_normalizada, cache_respostas={})

    if resposta:
        return jsonify({"answer": resposta})
    else:
        return jsonify({"answer": "Desculpe, não consegui encontrar uma resposta adequada."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
