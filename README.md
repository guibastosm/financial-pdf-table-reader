# Extrator de Extratos Bancários Bradesco

Aplicação web para converter extratos bancários do Bradesco de PDF para CSV.

## Funcionalidades

- Upload de extratos bancários (PDF)
- Extração automática dos dados
- Visualização dos dados extraídos
- Download em formato CSV

## Requisitos

- Python 3.8+
- Ghostscript ([Download](https://ghostscript.com/releases/gsdnld.html))
- Microsoft Visual C++ Redistributable

## Instalação

```bash
# Instalar dependências
pip install -r requirements.txt
```

## Como Usar

1. Execute a aplicação:
```bash
streamlit run app.py
```

2. Abra o navegador (geralmente http://localhost:8501)
3. Faça upload do extrato do Bradesco em PDF
4. Baixe o arquivo CSV com os dados extraídos

## Tecnologias

- Streamlit (interface web)
- Camelot (extração de PDF)
- Pandas (manipulação de dados)
- PyPDF2 (processamento de PDF)