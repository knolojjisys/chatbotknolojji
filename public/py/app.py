from flask import Flask, request, jsonify
from flask_cors import CORS
# Importe suas funções do main.py
from pdf_utils import extrair_texto_com_pdfplumber as extrair_texto_pdf
from api_interaction import buscar_trecho_no_conteudo
from utils import normalizar_pergunta

app = Flask(__name__)
CORS(app)

# Carregue o conteúdo do PDF
caminho_pdf = "teste.pdf"
conteudo = extrair_texto_pdf(caminho_pdf)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    question = data.get("question")
    if not question:
        return jsonify({"answer": "Pergunta inválida!"}), 400

    # Normaliza a pergunta e busca a resposta
    pergunta_normalizada = normalizar_pergunta(question)
    resposta = buscar_trecho_no_conteudo(conteudo, pergunta_normalizada, cache_respostas={})

    if resposta:
        return jsonify({"answer": resposta})
    else:
        return jsonify({"answer": "Desculpe, não consegui encontrar uma resposta adequada."})

if __name__ == "__main__":
    app.run(debug=True)