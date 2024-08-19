import json
import datetime
import gspread
import gspread.utils
import streamlit as st

from rapidfuzz import process
from gspread_pandas import Spread
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload


class DatabaseManager:
    def __init__(self, spread_name, client):
        """
        Initializes the DatabaseManager with the provided spreadsheet name and client.

        :param spread_name: Name of the Google Spreadsheet.
        :type spread_name: str
        :param client: Google API client.
        :type client: Client
        """
        self.spread = Spread(spread_name, client=client)
        self.df = self.load_data(st.secrets[spread_name]["sheet_name"])
        self.sheet_name = st.secrets[spread_name]["sheet_name"]
        self.backlog = []

    def load_data(self, sheet_name):
        """
        Loads data from the specified Google Spreadsheet sheet.

        :param sheet_name: Name of the sheet to load data from.
        :type sheet_name: str
        :return: Dataframe containing the loaded data.
        :rtype: pandas.DataFrame
        """
        try:
            return self.spread.sheet_to_df(sheet=sheet_name).reset_index()
        except Exception as e:
            st.error(f"Erro ao carregar dados: {e}")
            return None

    def save_db_backlog(self):
        """
        Saves the backlog of changes to the Google Spreadsheet.
        """

        sheets = self.spread.sheets
        sheet = next((s for s in sheets if s.title == self.sheet_name), None)
        updates = []

        for change in self.backlog:
            row = change['row']
            col = change['col']
            value = change['value']
            cell_address = gspread.utils.rowcol_to_a1(row + 2, col + 1)
            updates.append({
                "range": cell_address,
                "values": [[value]]
            })

        if updates:
            try:
                sheet.batch_update(updates)
                st.success("Alterações salvas com sucesso!")
            except Exception as e:
                st.error(f"Erro ao salvar alterações: {e}")
        else:
            st.info("Nenhuma alteração encontrada para salvar.")

    def create_spread_backup(self, backup_folder_id, creds):
        """
        Creates a backup of the Google Spreadsheet and logs the modifications.

        :param backup_folder_id: ID of the folder to save the backup in Google Drive.
        :type backup_folder_id: str
        :param creds: Google API credentials.
        :type creds: google.oauth2.service_account.Credentials
        """
        mod_time = f"{datetime.datetime.now():%Y%m%d_%H%M%S}"
        backup_name = f"backup_{mod_time}_{self.spread.spread.title}"
        try:
            self.spread.client.copy(self.spread.spread.id, title=backup_name, folder_id=backup_folder_id)
            st.write(f"Backup criado com sucesso: {backup_name}")
        except Exception as e:
            st.error(f"Erro ao criar backup: {e}")

        if len(self.backlog) > 0:
            backlog_json = json.dumps(self.backlog, indent=4).encode('utf-8')
            drive_service = build('drive', 'v3', credentials=creds)
            file_name = f"log_{mod_time}_{self.spread.spread.title}.json"
            file_metadata = {
                'name': file_name,
                'parents': [backup_folder_id],
                'mimeType': 'application/json'
            }
            media = MediaInMemoryUpload(backlog_json, mimetype='application/json')
            try:
                drive_service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id'
                ).execute()
                st.write(f"Log de modificações salvo como {file_name} na pasta de backup.")
            except Exception as e:
                st.error(f"Erro ao salvar log de modificações: {e}")

    def check_student(self, student_name):
        """
        Checks if a student is present in the database.

        :param student_name: Name of the student to check.
        :type student_name: str
        :return: True if the student is present, False otherwise.
        :rtype: bool
        """
        return student_name in self.df['Nome'].values

    def suggest_names(self, user_input, limit=3):
        """
        Suggests names based on the user input using fuzzy matching.

        :param user_input: Input provided by the user.
        :type user_input: str
        :param limit: Number of suggestions to return.
        :type limit: int
        :return: List of suggested names.
        :rtype: list
        """
        names = self.df['Nome'].unique()
        suggestions = process.extract(user_input, names, limit=limit)
        suggested_names = [suggestion[0] for suggestion in suggestions]
        return suggested_names

    def save_sheet_to_df(self):
        """
        Substitutes the current df to the Google Spreadsheet.
        """
        try:
            sheets = self.spread.sheets
            sheet = next((s for s in sheets if s.title == self.sheet_name), None)
            self.spread.df_to_sheet(st.session_state.df, index=False, sheet=sheet)
            st.success("Alterações salvas com sucesso!")
        except Exception as e:
            st.error(f"Erro ao salvar alterações: {e}")