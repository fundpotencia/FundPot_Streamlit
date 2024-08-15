import os
import streamlit as st
import base64

def head():
    """
    Displays the header and the logo of the application
    """
    st.set_page_config(page_title="Como usar?", page_icon="📖")
    with open('./utils/front.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    try:
        with open('./utils/logo_jr.png', 'rb') as logo_file:
            logo_base64 = base64.b64encode(logo_file.read()).decode('utf-8')
            st.markdown(f'<p align="center"><img src="data:image/png;base64,{logo_base64}" width="500"></p>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("Logo file not found")

    st.markdown(""" <div style="text-align: center; font-size: 21px; margin: 20px;"> <strong>  
                        Você pode baixar o arquivo de tutorial de uso abaixo!
                        Também são encontrados dois arquivos Excel para uso apenas na atualização de Entrevistas e adição de novos dados de olimpíadas!
                        <br></div>""", unsafe_allow_html=True)



    # Caminhos dos arquivos
    pdf_filename = "./utils/Tutorial de uso.pdf"
    xlsx_filename1 = "./utils/dbOlimpiadas_EXEMPLO.xlsx"
    xlsx_filename2 = "./utils/dEntrevistas_EXEMPLO.xlsx"

    # Leitura do arquivo PDF
    with open(pdf_filename, "rb") as pdf_file:
        pdf_content = pdf_file.read()

    # Leitura do primeiro arquivo .xlsx
    with open(xlsx_filename1, "rb") as xlsx_file1:
        xlsx_content1 = xlsx_file1.read()

    # Leitura do segundo arquivo .xlsx
    with open(xlsx_filename2, "rb") as xlsx_file2:
        xlsx_content2 = xlsx_file2.read()

    # Dividindo a tela em três colunas
    col1, col2, col3 = st.columns(3)

    with col1:
        # Caixa para baixar o PDF
        st.download_button(
            label="Baixar Tutorial de uso",
            data=pdf_content,
            file_name="Tutorial de uso.pdf",
            mime='application/pdf'
        )

    with col2:
        # Caixa para baixar o primeiro arquivo .xlsx
        st.download_button(
            label="Baixar Excel de Olimpíadas",
            data=xlsx_content1,
            file_name="dbOlimpiadas_EXEMPLO.xlsx",
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    with col3:
        # Caixa para baixar o segundo arquivo .xlsx
        st.download_button(
            label="Baixar Excel de Entrevistas",
            data=xlsx_content2,
            file_name="dEntrevistas_EXEMPLO.xlsx",
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    st.markdown(""" <div style="text-align: center; font-size: 21px; margin: 20px;"> <strong>  
                            OBS: em caso de problemas para utilizar o site, tente primeiramente recarrega-lo, caso isso não resolva, tente contatar algum responsável pelo projeto.
                            <br></div>""", unsafe_allow_html=True)
head()
