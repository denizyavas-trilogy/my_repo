import mysql.connector
from mysql.connector import Error
import os
import base64


class DatabaseConnection:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv('db_host'),
                database=os.getenv('db_name'),
                user=os.getenv('db_username'),
                password=base64.b64decode(os.getenv('db_password')).decode('utf-8')
            )
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")

    def fetch_one(self, sql):
        if self.connection.is_connected():
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(sql)
            result = cursor.fetchone()
            cursor.close()
            return result

    def fetch_all(self, sql):
        if self.connection.is_connected():
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            return result

    def execute(self, sql):
        if self.connection.is_connected():
            cursor = self.connection.cursor()
            cursor.execute(sql)
            cursor.close()

    def insert(self, sql, data):
        if self.connection.is_connected():
            cursor = self.connection.cursor()
            cursor.execute(sql, data)
            self.connection.commit()
            cursor.close()

    def update(self, sql, data):
        if self.connection.is_connected():
            cursor = self.connection.cursor()
            cursor.execute(sql, data)
            self.connection.commit()
            cursor.close()

    def close(self):
        if self.connection.is_connected():
            self.connection.close()


def fetch_zendesk_tickets(products):
    return DatabaseConnection().fetch_all(
        f"SELECT dm.ticketId, dm.product, dm.priority, dm.status as ticket_status, dm.groupName, dm.organizationName, dm.subject, "
        f"dm.skills, dm.createdAt, dm.updatedAt, t.rawData, dm.ticketTags "
        f"FROM dm_ticket_metrics dm "
        f"LEFT JOIN tickets t ON dm.ticketId = t.ticketId "
        f"WHERE dm.status IN ('open', 'new', 'hold') "
        f"AND dm.product IN ({products}) "
        f"AND t.status IS NOT NULL "
        f"AND dm.groupName NOT IN ('PKC', 'Management') "
        f"AND dm.requester NOT IN (378291331394) "
        f"ORDER BY dm.createdAt")


def fetch_organizations():
    return DatabaseConnection().fetch_all(
        """
        SELECT o.organizationId, o.name, o.* FROM prod_cssurvey.organizations o where o.isDeleted =0 and o.organizationId>360048841659;
        """
    )


def get_zendesk_user_by_email(email):
    return DatabaseConnection().fetch_one(
        f"""
        select * from prod_cssurvey.zendeskusers z where z.email='{email}';
        """
    )


def get_ticket_status(ticket_id):
    return DatabaseConnection().fetch_one(
        f"""
        SELECT * FROM prod_cssurvey.dm_ticket_metrics dm where dm.ticketId={ticket_id};
        """
    )

if __name__ == "__main__":
    import dotenv
    import gsheet_ops

    dotenv.load_dotenv()
    organizations = fetch_organizations()
    formatted_accounts = [
        [
            account['sf_id'] if account['sf_id'] and not account['sfId'] else
            account['sfId'] if account['sfId'] and not account['sf_id'] else
            account['sf_id'] if account['sf_id'] == account['sfId'] else
            f"{account['sf_id']}_{account['sfId']}" if account['sf_id'] and account['sfId'] else
            "",
            account['company']
        ] for account in organizations
    ]

    gsheet_agent = gsheet_ops.gsheet_agent("1bP0hoLU9BU1mnlCBmhNDu6j4u4xN8BofzHfqObI9AUA")
    schedule = gsheet_agent.overwrite_sheet_range("Sheet87!A2:B", formatted_accounts)
