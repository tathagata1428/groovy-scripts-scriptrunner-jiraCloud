import requests
from requests.auth import HTTPBasicAuth

# Replace the following with your actual values
your_domain = "test.atlassain.net" # enter your Atlassian domain
email = "bogdan.radu@b4it.ro" # enter the email address used to generate the API token
api_token = "ATATT3xFfGF00T1MS82s_Drswgzm4JVSr6xDUIQlwfYFovY0XdncCaSxb2xOCtth1JERxHQXzqN_L8bKv8qx_W71PtFyhuqhv52Cr6XhoCDrtqc4ba2xHbqmV9qAzyxQiqgNTRdJ7VzFr2qQZaPJA7EDHA6jug7orvhvMp5SI31dfpHonpQoJ8k=9653A108"
user_email = "remove.user@userToremove.ro"  # The email address of the user to be removed

# Search for the user based on their email address
user_search_url = f"https://{your_domain}/rest/api/3/user/search"
user_response = requests.get(user_search_url, params={"query": user_email}, auth=HTTPBasicAuth(email, api_token))

if user_response.status_code == 200 and user_response.json():
    user_account_id = user_response.json()[0]["accountId"]
    
    # Form the group URL
    group_url = f"https://{your_domain}/rest/api/3/user/groups"
    
    # Get the list of groups the user is a member of
    group_response = requests.get(group_url, params={"accountId": user_account_id}, auth=HTTPBasicAuth(email, api_token))
    
   # Check if the request was successful
if group_response.status_code == 200:
    groups = group_response.json()  # Directly use the list returned
    
    # Iterate over all groups and try to remove the user from each group
    for group in groups:
        group_name = group['name']
        url = f"https://{your_domain}/rest/api/3/group/user"
        
        query = {
            'groupname': group_name,
            'accountId': user_account_id
        }

        response = requests.request("DELETE", url, params=query, auth=HTTPBasicAuth(email, api_token))
        
        if response.status_code == 204:
            print(f"Successfully removed user {user_account_id} from group {group_name}")
        elif response.status_code == 404:
            print(f"Warning: Group {group_name} does not exist or is not accessible")
        else:
            print(f"Done removing user {user_account_id} from group {group_name}: {response.status_code} - {response.text}")
else:
    print(f"Error getting groups for user {user_account_id}: {group_response.text}")
