import pandas as pd
import streamlit as st
from utils.utils import head_ev as head, CacheManager
from classes.db_manager import DatabaseManager
from classes.gclient import GoogleClient

class StudentApp:
    def __init__(self):
        self.cred_keys = st.secrets["gcp_service_account"]
        self.google_client = GoogleClient(self.cred_keys, scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ])

    def main(self):
        head()
        db = 'dEntrevistas'
        spread_name = st.secrets[db]["filename"]
        backup_ID = st.secrets["folders"]["backup_folderID"]

        if 'df_cloud' not in st.session_state:
            st.session_state.db_manager = DatabaseManager(spread_name, client=self.google_client.client)
            st.session_state.df_cloud = st.session_state.db_manager.df

        if 'df' not in st.session_state:
            st.session_state.df = None

        with st.form("input_user"):
            uploaded_file = st.file_uploader("Escolha um arquivo Excel", type=["xlsx", "xls"])
            st.form_submit_button('Continuar')

            try:
                tabela = pd.read_excel(uploaded_file)
                if st.session_state.df is None:
                    st.session_state.df = tabela
            except Exception as e:
                if uploaded_file is not None:
                    st.error(f"Erro ao ler o arquivo Excel: {e}")
                else:
                    st.warning("Por favor, insira um arquivo Excel (formatos: .xlsx ou .xls).")

        try:
            if tabela is not None:
                st.success("Os nomes das colunas foram encontrados no database! Clique em continuar novamente.")

                intersection_names = pd.DataFrame(
                    {'Nome': list(
                        set(st.session_state.db_manager.df['Nome'].dropna()) & set(tabela['Nome'].dropna()))})

                if not intersection_names.empty:
                    st.markdown('Os seguintes nomes estão duplicados:')
                    st.dataframe(intersection_names)
                    st.markdown('As informações repetidas do primeiro serão sobrepostas com as do segundo')

                merged_df = pd.concat([st.session_state.db_manager.df, tabela]).drop_duplicates('Nome', keep='last')
                merged_df = merged_df.sort_values(by='IDPessoa').reset_index(drop=True).dropna(subset=['Nome'])

                st.markdown('Os 10 últimos elementos da database ficarão assim:')
                st.dataframe(merged_df)
                st.markdown('Verifique se não há nada fora do padrão...')

                if st.button('Salvar'):
                    st.session_state.df = self.format_df(merged_df)
                    st.session_state.db_manager.create_spread_backup(backup_ID, self.google_client.creds)
                    st.session_state.db_manager.save_sheet_to_df()
                    CacheManager.clear_cache()
                elif st.button('Cancelar'):
                    CacheManager.clear_cache()
                    st.session_state.clear()
                    st.rerun()

        except Exception as e:
            if uploaded_file is not None:
                st.error(f"Erro ao processar tabela: {e}")

    def format_df(self, df):
        df.sort_values(by='IDPessoa', inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.dropna(subset=['Nome'], inplace=True)
        return df
