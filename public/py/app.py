from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from pdf_utils import extrair_texto_com_pdfplumber
from api_interaction import buscar_trecho_no_conteudo
from utils import normalizar_pergunta

app = Flask(__name__)
CORS(app)

# Caminho dinâmico do PDF
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    question = data.get("question")
    product = data.get("product")  # Recebe o produto selecionado
    if not question or not product:
        return jsonify({"answer": "Pergunta ou produto inválido!"}), 400

    # Caminho do PDF baseado no produto selecionado
    caminho_pdf = f"pdfs/{product}.pdf"
    if not os.path.exists(caminho_pdf):
        return jsonify({"answer": "PDF do produto não encontrado!"}), 404

    # Extrai o conteúdo do PDF
    conteudo = extrair_texto_com_pdfplumber(caminho_pdf)

    # Normaliza a pergunta e busca a resposta
    pergunta_normalizada = normalizar_pergunta(question)
    resposta = buscar_trecho_no_conteudo(conteudo, pergunta_normalizada, cache_respostas={})

    if resposta:
        return jsonify({"answer": resposta})
    else:
        return jsonify({"answer": "Desculpe, não consegui encontrar uma resposta adequada."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
