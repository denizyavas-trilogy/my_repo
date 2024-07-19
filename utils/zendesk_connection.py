import requests
from requests.auth import HTTPBasicAuth
import os
import base64


class ZendeskConnect:
    def __init__(self):
        self.base_url = f"https://{os.getenv('zendesk_domain')}.zendesk.com/api/v2/"
        self.email = os.getenv('zendesk_email')
        self.password = base64.b64decode(os.getenv('zendesk_password')).decode('utf-8')

    def get_response(self, endpoint):
        response = requests.get(self.base_url + endpoint, auth=HTTPBasicAuth(self.email, self.password))
        if response.status_code == 200:
            return response.json()
        else:
            print('Failed to retrieve attributes:', response.status_code)
            return []

    def update_organization_customfield(self, organization_id, customfield_id, value):
        data = {
            'organization': {
                'organization_fields': {str(customfield_id): value}
            }

        }

        response = requests.put(self.base_url + f"organizations/{organization_id}.json", json=data, auth=HTTPBasicAuth(self.email, self.password))

        if response.status_code == 200:
            print(response.json())
        else:
            print("Failed to update custom field:", response.status_code, response.text)

        pass


def get_attribute_values():
    return ZendeskConnect().get_response("routing/attributes?include=attribute_values,agent_count")
