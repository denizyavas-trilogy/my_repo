from datetime import datetime

import dotenv
import requests

from utils.gsheet_ops import gsheet_agent


def fetch_ticket_history(all_tickets):
    # Base URL for Freshdesk API
    base_url = 'https://contently.freshdesk.com/api/v2'
    # Authentication credentials
    auth = ('QQNh6wApANoiXeNHLuf', 'X')
    # Headers for the request
    headers = {'Content-Type': 'application/json'}

    tickets_with_conversations = []
    for ticket in all_tickets:
        # Fetch conversations for each ticket
        conversation_response = requests.get(f'{base_url}/tickets/{ticket}?include=conversations', auth=auth,
                                             headers=headers)
        if conversation_response.status_code == 200:
            print(ticket)
            conversations = conversation_response.json()
            description = conversations.get('description_text')
            convos = conversations.get('conversations', [])
            body_texts = "\n *** \n".join([conversation['body_text'] for conversation in convos])
            tickets_with_conversations.append([ticket, description[:5000], body_texts[:44500]])
    return tickets_with_conversations


dotenv.load_dotenv()

agent = gsheet_agent("1bP0hoLU9BU1mnlCBmhNDu6j4u4xN8BofzHfqObI9AUA")

start = 5800

# ticket_ids = agent.read_column(f"FreshDesk!A{start}:A{end}")
ticket_ids = [10610,
10679,
10687,
10694,
10703,
10737,
10761,
10767,
10769,
10773,
10783,
10794,
10861,
10865,
10876,
10895,
10902,
10904,
10916,
17564,
17573,
17575,
17579,
17582,
17585,
19742,
19785,
19866,
19876,
19913]

agent.overwrite_sheet_range(f"FreshDesk!B{start}:D", fetch_ticket_history(ticket_ids))
