import os
import requests
from github import Github

token = os.environ["GITHUB_TOKEN"]

# Create a github instance
GITHUB_INSTANCE = Github(token)

def add_new_user_to_organization(organization= "sysdevprosup", username="carmosin"):
    org = GITHUB_INSTANCE.get_organization(organization)
    new_user = GITHUB_INSTANCE.get_user(username)
    print "USER: ", new_user
    url = "{}/memberships/{}".format(org.url, username)
    print "URL: ", url
    req = requests.post(url)
    print req
    members = org.get_members()

    for member in members:
        print member

add_new_user_to_organization()