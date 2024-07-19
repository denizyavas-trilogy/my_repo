import json
import zendesk_source
import tempo_source
import gsheet_ops
import dotenv


def lambda_handler(event, context):
    dotenv.load_dotenv()

    body = event.get("body", None)
    if body is None:
        body = event

    if not isinstance(body, dict):
        body = json.loads(body)

    action_type = body.get("action_type", "")

    if action_type == "backlog_refresh":
        zendesk_tickets = zendesk_source.get_zendesk_tickets(zendesk_source.my_product_list)
        if zendesk_tickets:
            gsheet_ops.refresh_my_backlog(zendesk_tickets)
    elif action_type == "update_priority":
        zendesk_tickets = zendesk_source.get_zendesk_tickets(zendesk_source.my_product_list)
        if zendesk_tickets:
            tempo_source.update_tempo_priority(zendesk_tickets, 40)

    message = f"{action_type} is completed."

    print(message)

    return {
        'statusCode': 200,
        'body': message
    }


if __name__ == '__main__':
    lambda_handler({"action_type": "backlog_refresh"}, None)
    # lambda_handler({"action_type": "update_priority"}, None)
    # lambda_handler({"action_type": "team_refresh"}, None)
