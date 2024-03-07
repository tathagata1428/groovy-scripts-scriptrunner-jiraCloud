import requests

group_name = "m-users"
jira_url = "https://<sitename>.atlassian.net"
auth = ("email", "<api_token>")

# Get all permission schemes
permission_schemes_url = jira_url + "/rest/api/3/permissionscheme?expand=group"
response = requests.get(permission_schemes_url, auth=auth)
permission_schemes = response.json()

# Iterate over all permission schemes
for permission_scheme in permission_schemes["permissionSchemes"]:
    # Get all permissions for a permission scheme
    permission_url = jira_url + "/rest/api/3/permissionscheme/{}/permission?expand=group".format(permission_scheme["id"])
    response = requests.get(permission_url, auth=auth)
    permissions = response.json()
    #print(permissions)

    # Check if the specific group is used in the permission scheme
    for permission in permissions["permissions"]:
        #try:
        if "group" in permission ["holder"]:
            if permission["holder"]["parameter"] == group_name:
                print("Permission scheme '{}' uses group '{}'".format(permission_scheme["name"], group_name))
                break
        #except KeyError:
           # print("key error in permission")

#Bogdan Radu
          