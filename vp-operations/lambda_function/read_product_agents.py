from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

MY_SHEET = "1v9lYDQvkN65S1-_UeE10XTgxWvfTi4Vz2G1qrPuUUw8"
AGENTS_RANGE = "GPT_Allocations!A1:D"

product = "DNN"

gsheet_service_account_info = {
  "type": "service_account",
  "project_id": "client-requests-421814",
  "private_key_id": "59856c5b47bb6f1bd29dc09a95467cc34c3cc58e",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCF9Evg9yrLQNZ3\n/afmxI0lBtLHCf2t8/0ktmcj4ZAsRnlbU6U1bTz3FS1Nrg571tlaRkFYuLS9Jqeg\nyXIqreIEvjh5V+qeSl1NU17O75WTeocBtpSD6qJucKQ17wzOyGpJ5yIZ6jwBGXqz\nQET4I+4PH1tp+kmiB1siG2m2KhGNPKd2y6oacOAmfXe4wr7rXjsbOLVlDgh4ruTN\nXgyM7Ncmw5pOa55Eb+z7Aa8iqc6JSWyeaTJEYnDUphFdQzZDibsk+BJ07tNfDUex\narYWAKl/BgcZOkHeP7AVoCmft/HD+pSlUjXoVKTanX4MyijWe2GZaiLyPiE2H8Y8\nav4kQwG/AgMBAAECggEAMxqU2jIhouJNEAD3DcydlmsofaPbooIraNanuaIjuSh3\nwvZB2ISg1hi/rFuDjg5U5KJZ6smotmLpX6eKxSqKSEnzzKNUUGhJeScdy+/OTjHY\nELjBpyQcLOsPUr4s0jTWi/RAZ8ebdcXtMDaMOWinuSA65U8FyWlqBLSVm1goUwus\nARfdGr+pOEXYWN15Sx8km8Dhcp0eJZvzG0OI99a8vEgaEhgFxoxvOQBA+XWBcDEU\njbQqNNMl46BblF/HPVAyEnNbSCfmu+hctVdH9XrjRBbRVuVvOIZD2gf/YHNytLxi\nxFg5xRjawHfh1dRJqTT3IfcVn5mNFElZSSKIt9NLmQKBgQC6c7laYL79RhRYpiEW\nRTpVJhz7/o7pj74LwvaX5q21b/KoTW+Ymc+V+m0Y+ZCxyCQn2hxdCEGdKikgZhy1\nQnsd4mKDK2j/IbP5yOFF0Jf5zZ6BtuNqqN+1ZsmWBHAVjHSaxHYfKgxpVBZi7KgY\n7EegYxDftmsiPVKPsev1dgsNZwKBgQC365G+YxdEjU94tS6jO0lz1bsnO+Lq2PeO\nqExE0G8oJ3zQLBmOy+AQgKEZTeWtiWToDhm17edo2aQg+93tzCSJgKNlMyN0QE6S\nnBuvFFcX3VQnnQgGYo9GOmwt4LPnyPjguqSPy59NG43/sXF/CdwbCh/TgQxSej5V\nH/9THT1Z6QKBgBkxP68VeVjRWjhsIfZXXj1ZC/uEdpzaPixqqFT35yqnuJrC87wj\ntCeokYsZVVKgHzp/PuvXDL6Gjs4A3gojtGziRLtCZ0pprF6opL+BIreu76bJJkso\nDCn/fGdXrClNNAghWXB2hvzITsoI/eF4M2lZWVNQ24Lh1ED0IlSlIXMrAoGAKroO\nNLWefS167ebhe8hVKxTXEqlF8RsQf9K3TTFC8Ygi5dWo5lSUrCDFzDQdjHAjwgks\njehD30bYa1U33HuVbWA2FVeJAAPEfSjJAaZvCTtAxqcjayBQepct9IaEJO+6abLS\nchly253wIhud605mFN4IQMF1FGATxQDW9v8O9qkCgYAQI0nRBruWYABHziHqj8rS\ndzCMWrjzB9tCcPlvELSP6dMxE1TSDRcX0/rqZcyX5u9EM5vSneRf6iVNKoECml1x\nOe1oJPkVB1SNHmm+VGkTYlmVdRQ9O8c72b4VHEgu7iucWNBncodyp6qNfhJ72hTW\nXggmuV6C4mTraT5jBDgCEg==\n-----END PRIVATE KEY-----\n",
  "client_email": "data-collection@client-requests-421814.iam.gserviceaccount.com",
  "client_id": "102764803676647952768",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/data-collection%40client-requests-421814.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

class gsheet_agent:
    def __init__(self, spreadsheet_id):
        self.service = build(
            'sheets',
            'v4',
            credentials=Credentials.from_service_account_info(
                gsheet_service_account_info,
                scopes=['https://www.googleapis.com/auth/spreadsheets']))
        self.spreadsheet_id = spreadsheet_id

    def read_column(self, sheet_range):
        try:
            sheet = self.service.spreadsheets()
            result = sheet.values().get(spreadsheetId=self.spreadsheet_id, range=sheet_range).execute()
            return result.get('values', [])
        except Exception as e:
            print('Failed to read sheet:', e)


gsheet_client = gsheet_agent(MY_SHEET)
agents = gsheet_client.read_column(AGENTS_RANGE)

for agent in agents:
    if agent[2] == product:
        online_status = "online" if agent[1] == "TRUE" else "offline"
        agent_type = "QC" if agent[3] == "Yes" else "DO"
        name = agent[0]
        print(f"{agent_type} agent {name} is {online_status}")
