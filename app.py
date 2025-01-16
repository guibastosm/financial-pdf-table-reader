import streamlit as st
import pandas as pd
import camelot
import PyPDF2
import tempfile
import os

st.set_page_config(page_title="Extrator de Extratos Bancários")
st.title("Extrator de Extratos Bancários para CSV")

def obter_numero_de_paginas(pdf_path):
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        numero_de_paginas = len(pdf_reader.pages)
    return numero_de_paginas

def ignorar_tabela(df):
    condicao = (
        (df == "Fone Fácil Bradesco").any(axis=1)
        | (df == "Se Preferir, fale com a BIA pelo").any(axis=1)
        | (df == "Saldo Invest Fácil").any(axis=1)
    )
    return not (condicao == False).all()

def converter_data_para_dois_digitos(data):
    if pd.isna(data) or data == "":
        return data
    try:
        partes = data.split('/')
        if len(partes) == 3 and len(partes[2]) == 4:
            partes[2] = partes[2][2:]
            return '/'.join(partes)
        return data
    except:
        return data

def processar_pdf(pdf_path):
    try:
        num_paginas = obter_numero_de_paginas(pdf_path)
        formato = ["90, 220, 320, 420, 520"] * num_paginas

        tables = camelot.read_pdf(
            pdf_path,
            pages="all",
            row_tol=15,
            flavor="stream",
            columns=formato,
        )

        extrato = pd.DataFrame(
            columns=["Data", "Histórico", "Docto.", "Crédito (R$)", "Débito (R$)", "Saldo (R$)"]
        )

        with st.spinner('Processando tabelas...'):
            progress_bar = st.progress(0)
            for i, table in enumerate(tables):
                df = table.df

                if ignorar_tabela(df):
                    continue

                check_start = (df == "Data").any(axis=1)
                if any(check_start):
                    idx = check_start.idxmax()
                    df = df[idx + 1:]

                df.columns = [
                    "Data", "Histórico", "Docto.",
                    "Crédito (R$)", "Débito (R$)", "Saldo (R$)"
                ]

                extrato = pd.concat([extrato, df], ignore_index=True)
                progress_bar.progress((i + 1) / len(tables))

        extrato["Data"] = extrato["Data"].replace("", method="ffill")
        extrato["Data"] = extrato["Data"].apply(converter_data_para_dois_digitos)
        
        return extrato
    except Exception as e:
        st.error(f"Erro ao processar o PDF: {str(e)}")
        return None

def main():
    uploaded_file = st.file_uploader("Escolha um arquivo PDF de extrato bancário", type="pdf")
    
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        try:
            df = processar_pdf(tmp_file_path)
            if df is not None:
                st.success("PDF processado com sucesso!")
                st.dataframe(df)

                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Baixar CSV",
                    data=csv,
                    file_name="extrato.csv",
                    mime="text/csv",
                )
        finally:
            os.unlink(tmp_file_path)

if __name__ == "__main__":
    main()