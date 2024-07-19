import boto3
import sys


def list_api_gateway_endpoints(profile_name):
    session = boto3.Session(profile_name=profile_name)
    client = session.client('apigateway')
    apis = client.get_rest_apis()

    api_details = []

    for api in apis['items']:
        api_id = api['id']
        api_name = api['name']
        stages = client.get_stages(restApiId=api_id)

        for stage in stages['item']:
            stage_name = stage['stageName']
            endpoint_url = f"https://{api_id}.execute-api.{session.region_name}.amazonaws.com/{stage_name}"
            api_details.append({
                'API Name': api_name,
                'API ID': api_id,
                'Stage': stage_name,
                'Endpoint URL': endpoint_url
            })

    return api_details


def main(profile_name):
    api_details = list_api_gateway_endpoints(profile_name)
    for api in api_details:
        print(f"{api['API Name']}; {api['API ID']}; {api['Stage']}; {api['Endpoint URL']}")


if __name__ == "__main__":
    main("trilogy")
