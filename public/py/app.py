import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pdf_utils import extrair_texto_com_pdfplumber as extrair_texto_pdf
from api_interaction import buscar_trecho_no_conteudo
from utils import normalizar_pergunta

app = Flask(__name__, static_folder="public", static_url_path="")
CORS(app)

# Configuração do caminho para os PDFs
CAMINHO_PDFS = "public/pdfs/"

@app.route('/')
def serve_index():
    # Servir o index.html da pasta public
    return send_from_directory(app.static_folder, "index.html")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    question = data.get("question")
    product = data.get("product")

    if not question or not product:
        return jsonify({"answer": "Pergunta ou produto inválido!"}), 400

    # Gera o caminho completo para o arquivo PDF
    nome_arquivo = f"{product}.pdf"
    caminho_completo = os.path.join(CAMINHO_PDFS, nome_arquivo)

    # Verifica se o arquivo PDF existe
    if not os.path.exists(caminho_completo):
        return jsonify({"answer": f"PDF do produto '{product}' não encontrado!"}), 404

    # Extrai o conteúdo do PDF
    try:
        conteudo = extrair_texto_pdf(caminho_completo)
    except Exception as e:
        return jsonify({"answer": f"Erro ao processar o PDF: {str(e)}"}), 500

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
