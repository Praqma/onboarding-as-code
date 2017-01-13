from __future__ import print_function
import httplib2
import os
import json

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/admin-directory_v1-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/admin.directory.user'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Directory API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    print('Looking for already obtained credentials')
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'admin-directory_v1-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    print('Creating new credentials')
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Google Admin SDK Directory API.

    Creates a Google Admin SDK API service object and outputs a list of first
    10 users in the domain.
    """
    print('###########################')
    print('Getting credentials.')
    credentials = get_credentials()
    
    print('Authorizing credentials.')
    http = credentials.authorize(httplib2.Http())

    print('Building service.')
    service = discovery.build('admin', 'directory_v1', http=http)

    print('###########################')
    print('Getting the first 10 users in the domain')
    results = service.users().list(customer='my_customer', maxResults=10,
        orderBy='email').execute()
    users = results.get('users', [])

    if not users:
        print('No users in the domain.')
    else:
        print('Users:')
        for user in users:
            print('{0} ({1})'.format(user['primaryEmail'],
                user['name']['fullName']))
    
    print('###########################')
    print('Getting specific user.')
    
    user = service.users().get(userKey='lakrus@sysdevprosup.org',projection='basic',customFieldMask='None',viewType='admin_view').execute()
    if not user:
        print('No such user')
    else:
        print('{0} ({1})'.format(user['primaryEmail'],
                user['name']['fullName']))
    print('###########################')
    print('Create user')
    #user = service.users().insert(body=json.dumps({'id':'jeb','':)).execute()
    if not user:
        print('No such user')
    else:
        print('{0} ({1})'.format(user['primaryEmail'],
                user['name']['fullName']))


if __name__ == '__main__':
    main()
