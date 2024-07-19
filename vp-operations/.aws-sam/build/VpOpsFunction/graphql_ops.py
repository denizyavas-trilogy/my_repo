from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import os
import requests
import base64


class GraphqlAgent:
    def __init__(self, agent_type, **kwargs):
        response = requests.post(
            url=f"https://cognito-idp.{os.getenv('aws_region')}.amazonaws.com/",
            json={
                "AuthFlow": "USER_PASSWORD_AUTH",
                "ClientId": os.getenv('aws_client'),
                "AuthParameters": {
                    "USERNAME": os.getenv('aws_username'),
                    "PASSWORD": base64.b64decode(os.getenv('aws_password')).decode('utf-8')
                }
            },
            headers={
                "Content-Type": "application/x-amz-json-1.1",
                "X-Amz-Target": "AWSCognitoIdentityProviderService.InitiateAuth"
            })
        access_token = response.json().get("AuthenticationResult", {}).get("AccessToken", None)

        self.client = Client(
            transport=RequestsHTTPTransport(
                url=os.getenv('graphql_apiUrl'),
                verify=True,
                retries=3,
                headers={'Authorization': access_token}),
            fetch_schema_from_transport=True)

        self.query = None
        self.edge = None
        self.variables = None

        agent_configurations = {
            "product": self.configure_product,
            "work_unit_items": self.configure_work_unit_items,
            "work_unit_update": self.configure_work_unit_update
        }

        config_function = agent_configurations.get(agent_type)
        if not config_function:
            raise ValueError(f"Unsupported agent type: {agent_type}")
        config_function(**kwargs)

    def configure_product(self):
        self.query = """
            query Products($input: ProductsInput) {
              products(input: $input) {
                edges {
                  node {
                    id
                    name
                  }
                }
                pageInfo {
                  hasNextPage
                  endCursor
                }
              }
            }
        """
        self.variables = {"input": {"limit": 100, "active": True}}
        self.edge = 'products'

    def configure_work_unit_items(self, **kwargs):
        required_params = ['product_id', 'status']
        if not all(param in kwargs for param in required_params):
            raise ValueError("Missing required parameters for 'work_unit_items'")
        self.query = """
    query WorkProductsList($input: WorkProductsFastInput) {
      workProductsFast(input: $input) {
        edges {
          node {
            id
            workId
            priority
            status
            createdAt
            nodeStatuses {
              type
              completionStatus
              tasks {
                fetchedBy
                fetchedAt
              }
            }
          }
          cursor
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
    """
        self.variables = {
                "input": {
                    "assemblyLineId": "01GKQYKKZ65AZHWTR84Y516A73",
                    "productId": kwargs['product_id'],
                    "limit": 20,
                    "after": "",
                    "priorityFilterParameters": {
                        "operator": "NOT_EQUAL",
                        "value": -1
                    },
                    "statusFilterParameters": {
                        "operator": "EQUAL",
                        "value": kwargs['status']
                    }
                }
            }
        self.edge = "workProductsFast"

    def configure_work_unit_update(self, **kwargs):
        required_params = ['work_unit_id', 'priority']
        if not all(param in kwargs for param in required_params):
            raise ValueError("Missing required parameters for 'work_unit_update'")
        self.query = """
            mutation EditWorkProduct($input: EditWorkProductInput!) {
              editWorkProduct(input: $input) {
                ...WorkProductBasic
              }
            }

            fragment WorkProductBasic on WorkProduct {
              id
              priority
            }
        """
        self.variables = {
            "input": {
                "id": kwargs['work_unit_id'],
                "priority": kwargs['priority']
            }
        }

    def fetch_all_data(self):
        copy_variables = self.variables.copy()
        all_edges = []
        has_next = True
        retry_count = 0
        max_retries = 5

        while has_next:
            try:
                response = self.execute_query()
                if response:
                    edges = response[self.edge]['edges']
                    all_edges.extend(edge['node'] for edge in edges)
                    page_info = response[self.edge]['pageInfo']
                    has_next = page_info['hasNextPage']
                    if has_next:
                        copy_variables['input']['after'] = page_info['endCursor']
                    retry_count = 0
                else:
                    raise Exception("No response from the server.")

            except Exception as e:
                retry_count += 1
                if retry_count >= max_retries:
                    print(copy_variables)
                    print(f"Failed to fetch data after {max_retries} attempts: {str(e)}")
                    break
                else:
                    print(copy_variables)
                    print(f"Attempt {retry_count} failed, retrying...")
                    has_next = True
        return all_edges

    def execute_query(self):
        return self.client.execute(gql(self.query), variable_values=self.variables)
