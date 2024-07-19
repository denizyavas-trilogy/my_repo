import requests
from requests.auth import HTTPBasicAuth
import base64
import os


class JiraConnection:
    def __init__(self):
        self.username = os.getenv('jira_username')
        self.api_token = base64.b64decode(os.getenv('jira_token')).decode('utf-8')
        self.project_url_mapping = {
            'IBUENG': 'https://workstation-df.atlassian.net',
            'IGBIZOPS': 'https://workstation-df.atlassian.net',
            'CFIN': 'https://workstation-df.atlassian.net',
            'IPCST': 'https://workstation-df.atlassian.net',
            'ITPEF': 'https://workstation-df.atlassian.net',
            'JVCLD': 'https://trilogy-eng.atlassian.net',
            'DFSERVERS': 'https://trilogy-eng.atlassian.net',
            'OSCMENT': 'https://trilogy-eng.atlassian.net',
            'STREETSMART': 'https://trilogy-eng.atlassian.net',
            'PBEYOND': 'https://trilogy-eng.atlassian.net',
            'FIRM58': 'https://trilogy-eng.atlassian.net',
            'MANUSCRIPT': 'https://trilogy-eng.atlassian.net'
        }

    def find_status(self, issue_key):
        if issue_key:
            jira_url = self.project_url_mapping.get(issue_key.split('-')[0])
            if jira_url:
                response = requests.get(f'{jira_url}/rest/api/3/issue/{issue_key}',
                                        auth=HTTPBasicAuth(self.username, self.api_token))
                if response.status_code == 200:
                    return response.json()['fields']['status']['statusCategory']['id']
            print(f"Can't get link to jira: {issue_key}")
        return ""
