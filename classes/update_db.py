import pandas as pd
import streamlit as st
from utils.utils import head_new_data as head, CacheManager
from classes.db_manager import DatabaseManager
from classes.gclient import GoogleClient



class StudentApp:
    def __init__(self):
        self.cred_keys = st.secrets["gcp_service_account"]
        self.google_client = GoogleClient(self.cred_keys, scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ])
        self.id = 'add_olimpiadas'

    def main(self):
        if 'id' not in st.session_state:
            st.session_state.id = self.id
        if self.id != st.session_state.id:
            CacheManager.clear_cache()
            st.session_state.id = self.id
        head()
        db = 'DB_Olimpiadas'
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
                if st.session_state.df is None or not tabela.equals(st.session_state.df):
                    st.session_state.df = tabela
                    st.success("Tabela carregada com sucesso!")
            except Exception as e:
                if uploaded_file is not None:
                    st.error(f"Erro ao ler o arquivo Excel: {e}")
                else:
                    st.warning("Por favor, insira um arquivo Excel (formatos: .xlsx ou .xls).")

        try:
            if tabela is not None and st.session_state.df_cloud.columns.equals(st.session_state.df.columns):
                st.success("Os nomes das colunas foram encontrados no database! Clique em continuar novamente.")
                merged_df = pd.concat([st.session_state.df_cloud, tabela], ignore_index=True)
                duplicate_mask = merged_df.duplicated(keep=False)
                new_entries = tabela[~tabela.apply(tuple, 1).isin(st.session_state.df_cloud.apply(tuple, 1))]

                if new_entries.empty:
                    st.warning("#### Nenhum novo registro foi encontrado para adicionar ao banco de dados.")
                else:
                    st.markdown('##### Os novos registros que serão adicionados ao banco de dados são:')
                    st.dataframe(new_entries)

                    # Exibir uma amostra dos novos dados que serão adicionados
                    final_df = pd.concat([st.session_state.df_cloud, new_entries]).sort_values(
                        by='Nome').reset_index(drop=True)

                    st.markdown('##### O Database final é mostrado abaixo. Caso queira, é possivel pesquisar por nomes no database pela lupa no canto superior direito.')
                    st.dataframe(final_df)
                    st.markdown(
                        '##### Caso esteja tudo em conformidade com o esperado, clique no botão **Salvar**. Caso contrário, cancele a operação.')

                    if st.button('Salvar'):
                        st.session_state.df = self.format_df(final_df)
                        st.session_state.db_manager.create_spread_backup(backup_ID, self.google_client.creds)
                        st.session_state.db_manager.save_sheet_to_df()
                        CacheManager.clear_cache()
                    elif st.button('Cancelar'):
                        CacheManager.clear_cache()
                        st.session_state.clear()
                        st.rerun()
            if not st.session_state.df_cloud.columns.equals(st.session_state.df.columns):
                st.error(f"Erro: As colunas do arquivo passado não são iguais às colunas do database. "
                         f"Por favor, verifique se o arquivo passado possui as colunas corretas. Caso seja necessário, a página *Como Usar* possui um tutorial de uso bem como o arquivo base para adicionar olimpíadas.")
        except Exception as e:
            if uploaded_file is not None and 'df_cloud' in st.session_state:
                st.error(f"Erro ao processar tabela: {e}")

    def format_df(self, df):
        df.sort_values(by='Nome', inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.dropna(subset=['Nome'], inplace=True)

        # Corrigir tipos de colunas que podem causar problemas na conversão
        if 'Ano' in df.columns:
            df['Ano'] = df['Ano'].astype(str)  # Converte a coluna 'Ano' para string

        return df
