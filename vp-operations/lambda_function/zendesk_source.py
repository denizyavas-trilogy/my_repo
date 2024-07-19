import json
from datetime import datetime

import db_ops
import jira_ops

ZENDESK_URL = "https://central-supportdesk.zendesk.com/agent/tickets/"

my_product_list = ['cs_central_saas', 'hand', 'acorn', 'answerhub', 'autotrol', 'avolin_computron', 'avolin_coretrac',
                   'dnn', 'epm', 'everest', 'ffm', 'fogbugz', 'gensym', 'infobright', 'jive_cloud', 'jive_hop',
                   'avolin_knova', 'northplains_pdct_xinet', 'nuview', 'objectstore', 'olive_software', 'onescm',
                   'prologic', 'scalearc', 'skyvera', 'smartroutines', 'sococo', 'streetsmart', 'avolin_supportsoft',
                   'avolin_tradebeam', 'avolin_verdiem', 'placeable', 'avolin_4gov', 'firm58']


def get_zendesk_tickets(products):
    def determine_team(status, github_incident, external_team, jira_key, group, product, ticket_id):
        if status == "On-hold":
            if github_incident and "github.com" in github_incident:
                return "Engineering"
            elif external_team == "central_saas":
                return "Support"
            elif external_team == "central_finance_new":
                return "Finance"
            elif jira_key and "CFIN" not in jira_key:
                return "BU"
            elif external_team and external_team.startswith("bu"):
                return "BU"
            elif external_team == "central_engineering":
                print(f"Central Engineering ticket w/o GHI: {ticket_id}")
                return "Engineering"
        else:
            if external_team == "bu_ps":
                return "PS"
            if group and not ("ZD Routing - Level" in group) and not ("chat department" in group.lower()):
                return "BU"
            if product == "cs_central_finance" and "BU" in group:
                return "Collections"
        return "Support"

    def extract_cloud_jira_id(data):
        if not data or 'custom_fields' not in data:
            return None

        cloud_bu_field = next((field for field in data['custom_fields'] if field['id'] == 4412704649490), None)

        if not cloud_bu_field:
            return None

        return cloud_bu_field.get('value')

    def extract_escalation_target(data):
        if not data or 'custom_fields' not in data:
            return None

        escalation_target_field = next((field for field in data['custom_fields'] if field['id'] == 10340593262482),
                                       None)

        if not escalation_target_field:
            return None

        return escalation_target_field.get('value')

    def extract_external_team(data):
        if not data or 'custom_fields' not in data:
            return None

        external_team_field = next((field for field in data['custom_fields'] if field['id'] == 360018492214), None)

        if not external_team_field:
            return None

        return external_team_field.get('value')

    def map_status(status):
        if status == "open":
            return "Open"
        elif status == "new":
            return "New"
        elif status == "hold":
            return "On-hold"
        else:
            print(f"Invalid status: {status}")
            return "Open"

    def extract_github_issue(data):
        if not data or 'custom_fields' not in data:
            return None

        ds_field = next((field for field in data['custom_fields'] if field['id'] == 10340637165202), None)

        if not ds_field:
            return None

        return ds_field.get('value')

    def transform_ticket_data(ticket_data):
        status = map_status(ticket_data.get('ticket_status', ''))
        group = ticket_data.get('groupName')
        data = json.loads(ticket_data.get('rawData', '{}'))  # Handle missing rawData safely
        product = ticket_data.get('product')
        ticket_id = ticket_data['ticketId']
        tags = ticket_data['ticketTags']

        ghi = extract_github_issue(data)
        jira = extract_cloud_jira_id(data)
        external_team = extract_external_team(data)

        team = determine_team(status, ghi, external_team, jira, group, product, ticket_id)

        if team == "Support":
            support_team = None
            if group:
                support_team = "L1" if "Level 1" in group else "L2" if "Level 2" in group else None

            raw_data = json.loads(ticket_data.get('rawData'))

            blocker_key = extract_cloud_jira_id(raw_data)
            blocker_link = ""
            blocker_status = ""
            if blocker_key:
                jira_split = blocker_key.split('-')
                if len(jira_split) > 1:
                    jira_connection = jira_ops.JiraConnection()
                    jira_project = jira_split[0]
                    jira_project = jira_connection.project_url_mapping.get(jira_project)
                    blocker_link = f"=HYPERLINK(\"{jira_project}/browse/{str(blocker_key)}\",\"{str(blocker_key)}\")" if jira_project else str(
                        blocker_key)
                    blocker_status = jira_connection.find_status(blocker_key)
                else:
                    blocker_link = f"=HYPERLINK(\"https://central-supportdesk.zendesk.com/agent/tickets/{str(blocker_key)}\",\"{str(blocker_key)}\")"
                    blocker_status = db_ops.get_ticket_status(blocker_key).get('status')

            splitted_tags = tags.split(',')

            today = datetime.now()
            created_since = (today - ticket_data.get("createdAt")).days
            updated_since = (today - ticket_data.get("updatedAt")).days

            return [
                f"=HYPERLINK(\"{ZENDESK_URL}{str(ticket_id)}\",\"{str(ticket_id)}\")",
                str(ticket_id),
                product,
                ticket_data.get('priority', ''),
                status,
                ticket_data.get('subject'),
                f"{created_since} days" if created_since >= 1 else "today",
                f"{updated_since} days" if updated_since >= 1 else "today",
                support_team,
                'qc_pending' in splitted_tags,
                external_team,
                extract_escalation_target(raw_data),
                blocker_link,
                blocker_status,
                ticket_data.get("skills")
            ]

    tickets = []
    zd_tickets = db_ops.fetch_zendesk_tickets(', '.join([f"'{product}'" for product in products]))
    for one_zd_ticket in zd_tickets:
        ticket = transform_ticket_data(one_zd_ticket)
        if ticket:
            tickets.append(ticket)
    return tickets
