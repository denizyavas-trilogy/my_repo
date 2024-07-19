import datetime

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import os

class gsheet_agent:
    def __init__(self, spreadsheet_id):
        self.service = build(
            'sheets',
            'v4',
            credentials=Credentials.from_service_account_file(
                os.getenv('gsheet_service_file'),
                scopes=['https://www.googleapis.com/auth/spreadsheets']))
        self.spreadsheet_id = spreadsheet_id

    def clear_sheet(self, range_to_clear):
        try:
            self.service.spreadsheets().values().batchClear(spreadsheetId=self.spreadsheet_id,
                                                            body={
                                                                'ranges': [range_to_clear]
                                                            }).execute()
        except Exception as e:
            print('Failed to clear the sheet:', e)

    def write_to_sheet(self, data_with_range):
        try:
            self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.spreadsheet_id,
                                                             body={
                                                                 'data': data_with_range,
                                                                 'valueInputOption': 'USER_ENTERED'}).execute()
        except Exception as e:
            print('Failed to write to sheet:', e)

    def read_column(self, sheet_range):
        try:
            sheet = self.service.spreadsheets()
            result = sheet.values().get(spreadsheetId=self.spreadsheet_id, range=sheet_range).execute()
            return result.get('values', [])
        except Exception as e:
            print('Failed to read sheet:', e)

    def overwrite_sheet_range(self, sheet_range, data):
        self.clear_sheet(sheet_range)
        self.write_to_sheet([{
            'range': sheet_range,
            'values': data
        }])



