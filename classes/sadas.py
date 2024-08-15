import streamlit as st
from utils.utils import head_db as head
from classes.db_manager import DatabaseManager
from utils.utils import CacheManager
from classes.gclient import GoogleClient
import uuid

class StudentApp:
    def __init__(self):
        """
        Initializes the StudentApp with the necessary configurations and Google client.
        """
        self.sheet_name_map = {
            'Alunos (gênero, LinkedIn...)': 'dAlunos',
            'Premiações (escola, cidade, medalha, série...)': 'DB_Olimpiadas_Sprint3'
        }
        self.cred_keys = st.secrets["gcp_service_account"]
        self.google_client = GoogleClient(self.cred_keys, scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ])

    def display_student_info(self, student_name, width=800):
        """
        Displays information of the specified student.

        :param student_name: Name of the student whose information is to be displayed.
        :type student_name: str
        """
        student_container = st.container()
        with student_container:
            st.dataframe(st.session_state.df[st.session_state.df['Nome'] == student_name], width=width)

    def update_student_info(self, student_name, df, backlog):
        """
        Updates the information of the specified student in the dataframe and backlog.

        :param student_name: Name of the student to update.
        :type student_name: str
        :param df: Dataframe containing student data.
        :type df: pandas.DataFrame
        :param backlog: List containing the backlog of changes.
        :type backlog: list
        :return: Updated dataframe and backlog.
        :rtype: tuple
        """
        columns_to_drop = ['Nome', 'Escola_Original', 'IDAluno', 'IndicePrivilegio', 'Olimpíada', 'IndiceDesempenho']
        columns_to_drop = [col for col in columns_to_drop if col in df.columns]
        if st.session_state.db.check_student(student_name):
            st.subheader("⏫ Selecione a coluna para editar e insira o novo valor:")
            with st.form(key='update_form'):
                column = st.selectbox("Selecione a coluna para editar:", df.drop(columns=columns_to_drop).columns)
                new_value = st.text_input("Insira o novo valor:")
                submit_button = st.form_submit_button(label='Atualizar aluno')

                if submit_button and new_value:
                    row = df.index[df['Nome'] == student_name][0]
                    col = df.columns.get_loc(column)
                    backlog.append({"row": int(row), "col": int(col), "value": new_value, "old_value": df.loc[row, column], "column": column, "student_name": student_name})
                    df.loc[df['Nome'] == student_name, column] = new_value
                    st.success(f"As informações do aluno {student_name} foram atualizadas com sucesso!")
        return df, backlog

    def main(self):
        """
        Main function to run the Streamlit app.
        """
        head()

        st.subheader("➡️ Selecione o database abaixo:")
        option = st.selectbox('Database:', list(self.sheet_name_map.keys()), on_change=CacheManager.clear_cache)
        db = self.sheet_name_map[option]
        spread_name = st.secrets[db]["filename"]
        backup_ID = st.secrets["folders"]["backup_folderID"]

        if 'df' not in st.session_state or st.session_state.df is None:
            if st.button('Carregar Dados'):
                try:
                    st.session_state.db = DatabaseManager(spread_name, client=self.google_client.client)
                    st.session_state.df = st.session_state.db.df
                    st.session_state.backlog = st.session_state.db.backlog
                except Exception as e:
                    st.error(f"Erro ao carregar dados: {e}")

        if 'df' not in st.session_state or st.session_state.df is None:
            if st.button('Carregar Dados'):
                try:
                    st.session_state.db = DatabaseManager(spread_name, client=self.google_client.client)
                    st.session_state.df = st.session_state.db.df
                    st.session_state.backlog = st.session_state.db.backlog
                    st.session_state.spread_name = spread_name
                except Exception as e:
                    st.error(f"Erro ao carregar dados: {e}")

        if 'df' in st.session_state and st.session_state.df is not None:
            df = st.session_state.df
            backlog = st.session_state.backlog

            columns_to_drop = ['IDAluno', 'IndicePrivilegio', 'IndiceDesempenho']
            columns_to_drop = [col for col in columns_to_drop if col in df.columns]
            st.subheader("🗂️ Database carregado:")
            st.dataframe(df.drop(columns=columns_to_drop).reset_index(drop=True), height=250, width=800)

            st.subheader("📝 Atualização de dados")
            with st.form("input_user"):
                st.markdown(
                    """ <div style="font-size: 20px;"> 1️⃣ <strong> Digite o nome completo do(a) aluno(a):</div>""",
                    unsafe_allow_html=True)
                name = st.text_input("Nome completo do(a) aluno(a):").upper()
                st.form_submit_button("Buscar")

            if name and st.session_state.db.check_student(name):
                st.success(f"{name} encontrado(a) no database!")
                st.subheader("📌 Informações do(a) aluno(a):")
                self.display_student_info(name)

                df, backlog = self.update_student_info(name, df, backlog)
                self.display_student_info(name)
                st.session_state.df = df
                st.session_state.backlog = backlog

                if st.button('Salvar', key='save_button'):
                    st.session_state.db.create_spread_backup(backup_ID, self.google_client.creds)
                    st.session_state.db.save_db_backlog()
                    st.session_state.backlog = []  # Limpar backlog após salvar
                    CacheManager.clear_cache()
            else:
                if name.strip() == "":
                    st.info("O campo de nome está vazio. Por favor, insira um nome.")
                else:
                    st.error(f"O aluno {name} não foi encontrado no database. Veja sugestões abaixo:")
                    suggestions = st.session_state.db.suggest_names(name)
                    for suggestion in suggestions:
                        st.markdown(f"**{suggestion.rstrip()}**")

        if st.button('Cancelar'):
            CacheManager.clear_cache()