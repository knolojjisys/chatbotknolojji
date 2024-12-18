import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pdf_utils import extrair_texto_com_pdfplumber as extrair_texto_pdf
from api_interaction import buscar_trecho_no_conteudo
from utils import normalizar_pergunta

app = Flask(__name__)
CORS(app)

# Caminho base onde os PDFs estão armazenados
BASE_PDF_PATH = "pdfs/"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    question = data.get("question")
    product = data.get("product")  # Pega o nome do produto enviado

    if not question:
        return jsonify({"answer": "Pergunta inválida!"}), 400
    
    if not product:
        return jsonify({"answer": "Nenhum produto foi selecionado!"}), 400

    # Monta o caminho do PDF com base no produto selecionado
    caminho_pdf = os.path.join(BASE_PDF_PATH, f"{product}.pdf")
    
    if not os.path.exists(caminho_pdf):
        return jsonify({"answer": f"Arquivo PDF para '{product}' não encontrado."}), 404

    # Carrega o conteúdo do PDF
    conteudo = extrair_texto_pdf(caminho_pdf)

    if not conteudo:
        return jsonify({"answer": "Não foi possível extrair o conteúdo do PDF."}), 500

    # Normaliza a pergunta e busca a resposta
    pergunta_normalizada = normalizar_pergunta(question)
    resposta = buscar_trecho_no_conteudo(conteudo, pergunta_normalizada, cache_respostas={})

    if resposta:
        return jsonify({"answer": resposta})
    else:
        return jsonify({"answer": "Desculpe, não consegui encontrar uma resposta adequada."})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)


