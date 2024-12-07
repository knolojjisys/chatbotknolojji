import pdfplumber
import fitz  # PyMuPDF
from PIL import Image
import io
import os
import logging

def extrair_texto_com_pdfplumber(caminho_arquivo_pdf):
    """Tenta extrair texto de um arquivo PDF usando pdfplumber."""
    texto = ""
    try:
        with pdfplumber.open(caminho_arquivo_pdf) as pdf:
            for pagina in pdf.pages:
                texto += pagina.extract_text() + "\n"
        return texto if texto.strip() else None
    except Exception as e:
        logging.error(f"Erro ao extrair texto do PDF com pdfplumber: {e}")
        return None

def extrair_imagens_pdf(caminho_arquivo_pdf):
    """Extrai imagens de um arquivo PDF e as salva em uma pasta."""
    pdf_documento = fitz.open(caminho_arquivo_pdf)
    imagens_extraidas = []

    # Cria uma pasta chamada 'imagens_extraidas' se ela não existir
    pasta_imagens = "imagens_extraidas"
    if not os.path.exists(pasta_imagens):
        os.makedirs(pasta_imagens)

    try:
        for numero_pagina in range(len(pdf_documento)):
            pagina = pdf_documento.load_page(numero_pagina)
            imagens = pagina.get_images(full=True)

            for img_index, img in enumerate(imagens):
                xref = img[0]
                base_imagem = pdf_documento.extract_image(xref)
                imagem_bytes = base_imagem["image"]
                imagem = Image.open(io.BytesIO(imagem_bytes))
                imagem_path = os.path.join(pasta_imagens, f"pagina_{numero_pagina + 1}_imagem_{img_index + 1}.png")
                imagem.save(imagem_path)
                imagens_extraidas.append(imagem_path)
        
        return imagens_extraidas
    except Exception as e:
        logging.error(f"Erro ao extrair imagens do PDF: {e}")
        return []

def extrair_graficos_pdf(caminho_arquivo_pdf):
    """Extrai gráficos (se forem armazenados como imagens) de um PDF e os salva em uma pasta."""
    pdf_documento = fitz.open(caminho_arquivo_pdf)
    graficos_extraidos = []

    # Cria uma pasta chamada 'graficos_extraidos' se ela não existir
    pasta_graficos = "graficos_extraidos"
    if not os.path.exists(pasta_graficos):
        os.makedirs(pasta_graficos)

    try:
        for numero_pagina in range(len(pdf_documento)):
            pagina = pdf_documento.load_page(numero_pagina)
            imagens = pagina.get_images(full=True)

            for img_index, img in enumerate(imagens):
                xref = img[0]
                base_imagem = pdf_documento.extract_image(xref)
                imagem_bytes = base_imagem["image"]
                imagem = Image.open(io.BytesIO(imagem_bytes))
                grafico_path = os.path.join(pasta_graficos, f"grafico_pagina_{numero_pagina + 1}_imagem_{img_index + 1}.png")
                imagem.save(grafico_path)
                graficos_extraidos.append(grafico_path)
        
        return graficos_extraidos
    except Exception as e:
        logging.error(f"Erro ao extrair gráficos do PDF: {e}")
        return []
