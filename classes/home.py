import os
import streamlit as st
import base64
def head():
    """
    Displays the header and the logo of the application
    """
    st.set_page_config(page_title="Home", page_icon="🌍")
    with open('./utils/front.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    try:
        with open('./utils/logo_jr.png', 'rb') as logo_file:
            logo_base64 = base64.b64encode(logo_file.read()).decode('utf-8')
            st.markdown(f'<p align="center"><img src="data:image/png;base64,{logo_base64}" width="500"></p>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("Logo file not found")
    st.markdown("<h1 style='text-align: center; font-size: 38px;'> Formulário de atualização <br> Fundação Potência </h1>", unsafe_allow_html=True)

    st.markdown("<p style='text-align: center;'>>>> Aplicativo desenvolvido para atualização de informações de medalhistas olímpicos <<<</p>", unsafe_allow_html=True)

    st.markdown(""" <div style="text-align: center; font-size: 21px; margin: 20px;"> <strong>  
                    Para atualizar algum banco de dados, veja a barra lateral. Você será redirecionado para a página de atualização correspondente. <br>
                    <br></div>""", unsafe_allow_html=True)

    st.markdown(""" <div style="text-align: center; font-size: 21px; margin: 20px;"> <strong>  
                        1. Um tutorial de uso pode ser encontrado na aba "Como usar" <br>
                        2. Para atualizar informações sobre os alunos ou olimpíadas, clique em "Alunos e Olimpíadas"<br>
                        3. Para atualizar as entrevistas (adicionar novas entrevistas ou sobreescrever entrevistas existentes) clique em "Entrevistas"<br>
                        4. Para adicionar novos dados de olimpíadas, clique em "Adicionar novas olimpíadas"<br>
                        <br></div>""", unsafe_allow_html=True)

head()


