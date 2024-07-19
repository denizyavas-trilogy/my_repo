import dotenv

import graphql_ops

products = ['Central Saas', '@Hand', 'Acorn', 'AnswerHub', 'Auto-Trol', 'Computron', 'CoreTrac', 'DNN', 'EPM Live',
            'Everest',
            'Field Force Manager', 'FogBugz', 'Gensym', 'Infobright DB', 'Jive Cloud', 'Jive HOP', 'Knova',
            'NorthPlains - Xinet', 'NuView', 'ObjectStore', 'Olive Software', 'OneSCM', 'Prologic', 'ScaleArc',
            'Skyvera', 'Smartroutines', 'Sococo', 'StreetSmart/FFM', 'SupportSoft', 'TradeBeam', 'Verdiem', 'Placeable',
            'GoMembers', 'Firm58']


def update_priority(work_unit_id, priority):
    graphql_ops.GraphqlAgent("work_unit_update", work_unit_id=work_unit_id, priority=priority).execute_query()


def update_tempo_priority(zendesk_tickets, new_priority):
    def get_tempo_tickets():
        def get_tickets_filtered(product_id, status, tickets):
            for item in graphql_ops.GraphqlAgent("work_unit_items", product_id=product_id,
                                                 status=status).fetch_all_data():
                work_id = item['workId'].replace("ZD-", "")
                ticket_info = {
                    "tempo_id": item['id'],
                    "tempo_priority": item['priority'],
                    "tempo_status": item['status'],
                    "tempo_date": item['createdAt']
                }

                if work_id not in tickets:
                    tickets[work_id] = []
                tickets[work_id].append(ticket_info)

            return tickets

        tickets = {}
        for product in graphql_ops.GraphqlAgent("product").fetch_all_data():
            if product['name'] in products:
                product_id = product['id']
                for status in ["SCHEDULED", "PENDING", "IN_PROGRESS"]:
                    tickets = get_tickets_filtered(product_id, status, tickets)
        return tickets

    tempo_tickets = get_tempo_tickets()

    tickets = {}
    for zendesk_ticket in zendesk_tickets:
        zendesk_id = zendesk_ticket[1]
        if zendesk_id and zendesk_id in tempo_tickets:
            for tempo_ticket in tempo_tickets[zendesk_id]:
                tempo_id = tempo_ticket.get('tempo_id', '')
                old_priority = tempo_ticket.get('tempo_priority', 1000)
                if old_priority > new_priority:
                    update_priority(tempo_id, new_priority)
                    print(f"Changed priority of {tempo_id} to {new_priority} from {old_priority}")
                    tempo_ticket['tempo_priority'] = new_priority
    return tickets


if __name__ == '__main__':
    dotenv.load_dotenv()
    update_priority("01J20RZMAPY420ZGTJRD7EH0TA", 21)
