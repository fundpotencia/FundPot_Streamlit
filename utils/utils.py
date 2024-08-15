import streamlit as st
import base64

def head_db():
    st.set_page_config(page_title="Atualizar Database", page_icon="📶")
    with open('./utils/front.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    try:
        with open('./utils/logo_jr.png', 'rb') as logo_file:
            logo_base64 = base64.b64encode(logo_file.read()).decode('utf-8')
            st.markdown(f'<p align="center"><img src="data:image/png;base64,{logo_base64}" width="500"></p>',
                        unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("Logo file not found")

    st.markdown(
        "<h1 style='text-align: center; font-size: 38px;'>Formulário de atualização de database<br>Fundação Potência</h1>",
        unsafe_allow_html=True)

    st.markdown(
        "<p style='text-align: center;'>>>> Aplicativo desenvolvido para atualização de informações de medalhistas olímpicos <<<</p>",
        unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center; font-size: 30px;'> Banco de dados: Alunos/Olimpíadas</h1>",
                unsafe_allow_html=True)

    st.markdown(
        """<div style="text-align: center; font-size: 19px;"> 
        Nessa página, é possível editar os bancos de dados referentes à algumas informações pessoais dos alunos como: 
        <strong>LinkedIn, escola, medalha recebida, série escolar...</strong>
        </div>""",
        unsafe_allow_html=True)

    st.markdown(
        """<div style="text-align: center; font-size: 20px;">
        <br>Primeiramente, escolha o database de acordo com o que quer modificar:<br>
        <ul style="text-align: left; font-size: 18px;">
            <li><strong>Alunos</strong>: gênero, LinkedIn e biografia do LinkedIn</li>
            <li><strong>Olimpíadas</strong>: escola, cidade, estado, medalha, série, ano</li>
        </ul>
        </div>""",
        unsafe_allow_html=True)

def head_ev():
    st.set_page_config(page_title="Entrevistas", page_icon="🎤")
    with open('./utils/front.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    try:
        with open('./utils/logo_jr.png', 'rb') as logo_file:
            logo_base64 = base64.b64encode(logo_file.read()).decode('utf-8')
            st.markdown(f'<p align="center"><img src="data:image/png;base64,{logo_base64}" width="500"></p>',
                        unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("Logo file not found")
    st.markdown(
        "<h1 style='text-align: center; font-size: 38px;'>Formulário de atualização de entrevistas<br>Fundação Potência</h1>",
        unsafe_allow_html=True)

    st.markdown(
        "<p style='text-align: center;'>>>> Aplicativo desenvolvido para atualização de informações de medalhistas olímpicos <<<</p>",
        unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 30px;'>Banco de dados: Entrevistas</h1>",
                unsafe_allow_html=True)
    st.markdown(
        """ <div style="text-align: center; font-size: 20px;"> Nessa página, é possível adicionar/alterar informações referentes às entrevistas no banco de dados adicionando um arquivo excel com as informações no mesmo padrão do arquivo excel de entrevistas original</div>""",
        unsafe_allow_html=True)


def head_new_data():
    st.set_page_config(page_title="Adicionar Olimpíadas", page_icon="📁")
    with open('./utils/front.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    try:
        with open('./utils/logo_jr.png', 'rb') as logo_file:
            logo_base64 = base64.b64encode(logo_file.read()).decode('utf-8')
            st.markdown(f'<p align="center"><img src="data:image/png;base64,{logo_base64}" width="500"></p>',
                        unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("Logo file not found")
    st.markdown(
            "<h1 style='text-align: center; font-size: 38px;'>Adicionar novas entrevistas no database<br>Fundação Potência</h1>",
        unsafe_allow_html=True)

    st.markdown(
        "<p style='text-align: center;'>>>> Aplicativo desenvolvido para atualização de informações de medalhistas olímpicos <<<</p>",
        unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 30px;'>Banco de dados: Olimpíadas</h1>",
                unsafe_allow_html=True)
    st.markdown(
        """ <div style="text-align: center; font-size: 20px;"> Nessa página, é possível adicionar novos dados de olimpíadas</div>""",
        unsafe_allow_html=True)


class CacheManager:
    @staticmethod
    def clear_cache():
        for key in st.session_state.keys():
            del st.session_state[key]
        st.cache_data.clear()
        #st.session_state.clear()
        #st.rerun()
        st.success("Cache limpo com sucesso!")
