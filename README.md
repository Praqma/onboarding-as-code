[![Build Status](https://api.travis-ci.org/Praqma/onboarding-as-code.svg?branch=master)](https://travis-ci.org/Praqma/onboarding-as-code)

# onboarding-as-code

Automating the onboarding process. Because we can :D

### Current state

Implemented yaml based directory, support for automated creation/deletion of google account, setting email aliases
Running CI with Travis (protected master, building pushes and pull requests + cron builds to spot changes in API's)
Dockerized distribution through Docker Hub

### Setup

Setup assumes that you are running Python 2.7, have curl and tar installed

```
bash setup.sh # will download virtualenv, create virtualenv and install all necessary libs there
source env/bin/activate
```

### How to setup service account and necessary permissions

You will have to create service account and authorize it to use google api's for you Google Suite. See instruction below

* Go to https://console.developers.google.com/apis/credentials
* Select Create credentials -> Service Account Key. In the next window Drop down list -> New Service Account -> Any name -> Role: Project, Owner -> Type: Json -> Create
* Again Credentials -> Manage service accounts -> Edit service account -> Enable G Suite Domain Wide delegation
* G Suite Admin console -> Security -> Show more -> Advanced settings -> Manage API client access -> Use service account client id in the Name field and authorize the following scopes https://www.googleapis.com/auth/admin.directory.user, https://www.googleapis.com/auth/admin.directory.domain
* Read more here https://developers.google.com/api-client-library/python/auth/service-accounts

### Script help

```
python main.py --help

sage: main.py [-h] [-d] [-n] -p PATH -k KEY -e EMAIL {add,del} ...

positional arguments:
  {add,del}             This is what you can do
    add                 Go through all records in the directory and create all
                        users that are not registred yet in Google and other
                        services
    del                 Go through all recodrs in the direcoty and remove ones
                        that are registred in Google and other services but
                        not present in our records

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           print debug info
  -n, --dry-run         only print what would be executed
  -p PATH, --path PATH  path to the organisation directory
  -k KEY, --google-key KEY
                        path to Google service account private key
  -e EMAIL, --email EMAIL
                        email to autorize, i.e. service account will be acting
                        on behalf of this user
```
Note! There is a dry run option that you can use to test your changes before applying them

### Workflow examples

Add new user:

* add new record to the directory (currently, test_directory). Simply copy existing file and fill in your values. Note! We intentionaly haven't implemented support for taken account names - you should be able to figure it out your self from the file names in directory.
* run the script: python main.py -d -p $PWD/test_directory -k < your service accoint key > -e admin@sysdevprosup.org add

Remove user:

* remove file from the directory (currently, test_directory). ***Please do not remove lakrus and admin!***
* run the script: python main.py -d -p $PWD/test_directory -k < your service accoint key >  -e admin@sysdevprosup.org del

Examples:

```
# Added file
(env) Andreys-MacBook-Pro:onboarding-as-code andrey9kin$ cat test_directory/ady.yaml
!!python/object:lib.person.Person
email: andrey.a.devyatkin@gmail.com
fname: Andrey
gid: andrey9kin
lname: Devyatkin
pid: ady

# Creating account
(env) Andreys-MacBook-Pro:onboarding-as-code andrey9kin$ python main.py -d -p $PWD/test_directory -k $PWD/test_credentials/google_service_account_private_key.json -e admin@sysdevprosup.org add
   INFO: [google_client.py:16 - authorize() ] - Authorizing credentials
   INFO: [google_client.py:23 - authorize() ] - Building service
WARNING: [_helpers.py:132 - positional_wrapper() ] - build() takes at most 2 positional arguments (3 given)
WARNING: [__init__.py:44 - autodetect() ] - file_cache is unavailable when using oauth2client >= 4.0.0
Traceback (most recent call last):
  File "/Users/andrey9kin/code/onboarding-as-code/env/lib/python2.7/site-packages/googleapiclient/discovery_cache/__init__.py", line 41, in autodetect
    from . import file_cache
  File "/Users/andrey9kin/code/onboarding-as-code/env/lib/python2.7/site-packages/googleapiclient/discovery_cache/file_cache.py", line 41, in <module>
    'file_cache is unavailable when using oauth2client >= 4.0.0')
ImportError: file_cache is unavailable when using oauth2client >= 4.0.0
   INFO: [discovery.py:268 - _retrieve_discovery_doc() ] - URL being requested: GET https://www.googleapis.com/discovery/v1/apis/admin/directory_v1/rest
   INFO: [transport.py:157 - new_request() ] - Attempting refresh to obtain initial access_token
  DEBUG: [crypt.py:100 - make_signed_jwt() ] - ['eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImQxYjEwOGFjYWM1MDNkNGMyMWU3ODJiZTk5MGQwYTE3ZmVlMmNiZGUifQ', 'eyJhdWQiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20vby9vYXV0aDIvdG9rZW4iLCJleHAiOjE0ODQzNDk4MDYsImlhdCI6MTQ4NDM0NjIwNiwiaXNzIjoic2VydmljZS1hY2NvdW50QGVuZHVyaW5nLWJ5dGUtMTU1NTEyLmlhbS5nc2VydmljZWFjY291bnQuY29tIiwic2NvcGUiOiJodHRwczovL3d3dy5nb29nbGVhcGlzLmNvbS9hdXRoL2FkbWluLmRpcmVjdG9yeS51c2VyIGh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL2F1dGgvYWRtaW4uZGlyZWN0b3J5LmRvbWFpbiIsInN1YiI6ImFkbWluQHN5c2RldnByb3N1cC5vcmcifQ', 'ZdyROpgjBckGfHjnuVmUq1ZBvMtZ8o-gq8Z7iQKEOMxrqjA1-kJA6Xb0eIodNZBDf-Iv-0Pu_ZLwuTSJunqxYVPpdntdY9FodvvAr6HvqD3YbYX0OD6K6CVWyQSFyNLhj1J3uppN1p00VLIhTzGWAz5Y5dDI0ytJrjOgePOUTn22QgApqAotrpMhrUuwmfNqR1v4OWo0kEYasKt2LFAVsWtCRrWGHtExQpkOVSdThUboq5hgXi3UdgOojDQwB8lU6jPrTPBH48QFPlKyvwOeDIXnY9THvwRFTVM-4vuvOOcfWYhSmzcdFpk5HYXkCHuQ-AiUw_OPtdyMDS9HCd9pIQ']
   INFO: [client.py:772 - _do_refresh_request() ] - Refreshing access_token
   INFO: [google_client.py:25 - authorize() ] - Looking for domains
   INFO: [discovery.py:857 - method() ] - URL being requested: GET https://www.googleapis.com/admin/directory/v1/customer/my_customer/domains?alt=json
  DEBUG: [google_client.py:28 - authorize() ] - Found domains: [u'sysdevprosup.org']
   INFO: [yamlad.py:46 - get_all_accounts() ] - Reading all records from /Users/andrey9kin/code/onboarding-as-code/test_directory
  DEBUG: [yamlad.py:50 - get_all_accounts() ] - Found record: admin.yaml
  DEBUG: [yamlad.py:50 - get_all_accounts() ] - Found record: ady.yaml
  DEBUG: [yamlad.py:50 - get_all_accounts() ] - Found record: lakrus.yaml
   INFO: [google_client.py:31 - get_all_users() ] - Getting all users
   INFO: [discovery.py:857 - method() ] - URL being requested: GET https://www.googleapis.com/admin/directory/v1/users?customer=my_customer&orderBy=email&alt=json
  DEBUG: [google_client.py:36 - get_all_users() ] - Found user: admin
  DEBUG: [google_client.py:36 - get_all_users() ] - Found user: lakrus
   INFO: [main.py:34 - create_added_google_accounts() ] - Accounts that exists in directory but not in google: set(['ady'])
   INFO: [yamlad.py:36 - get_person() ] - Reading ady from disk /Users/andrey9kin/code/onboarding-as-code/test_directory/ady.yaml
   INFO: [google_client.py:43 - create_user() ] - Creare user ady in domain sysdevprosup.org
  DEBUG: [google_client.py:48 - create_user() ] - Creation params: {'primaryEmail': 'ady@sysdevprosup.org', 'password': 'AndreyDevyatkin', 'name': {'givenName': 'Andrey', 'familyName': 'Devyatkin'}, 'changePasswordAtNextLogin': True}
   INFO: [discovery.py:857 - method() ] - URL being requested: POST https://www.googleapis.com/admin/directory/v1/users?alt=json
  DEBUG: [google_client.py:51 - create_user() ] - Created user: {u'kind': u'admin#directory#user', u'name': {u'givenName': u'Andrey', u'familyName': u'Devyatkin'}, u'creationTime': u'2017-01-13T22:23:27.000Z', u'primaryEmail': u'ady@sysdevprosup.org', u'changePasswordAtNextLogin': True, u'isDelegatedAdmin': False, u'isMailboxSetup': False, u'isAdmin': False, u'etag': u'"lC5l2xZhzgy1zYIWApDice-fN_A/BBYy4tgUcevUjVxA60BrDYep_4c"', u'customerId': u'C03z1mtdc', u'id': u'107930582025231265723', u'orgUnitPath': u'/'}
   INFO: [google_client.py:68 - add_alias() ] - Add alias andrey9kin for user ady in domain sysdevprosup.org
   INFO: [discovery.py:857 - method() ] - URL being requested: POST https://www.googleapis.com/admin/directory/v1/users/ady%40sysdevprosup.org/aliases?alt=json
   INFO: [google_client.py:68 - add_alias() ] - Add alias andrey.devyatkin for user ady in domain sysdevprosup.org
   INFO: [discovery.py:857 - method() ] - URL being requested: POST https://www.googleapis.com/admin/directory/v1/users/ady%40sysdevprosup.org/aliases?alt=json

# Move account away
(env) Andreys-MacBook-Pro:onboarding-as-code andrey9kin$ mv test_directory/ady.yaml .

# Delete account in Google
(env) Andreys-MacBook-Pro:onboarding-as-code andrey9kin$ python main.py -d -p $PWD/test_directory -k $PWD/test_credentials/google_service_account_private_key.json -e admin@sysdevprosup.org del
   INFO: [google_client.py:16 - authorize() ] - Authorizing credentials
   INFO: [google_client.py:23 - authorize() ] - Building service
WARNING: [_helpers.py:132 - positional_wrapper() ] - build() takes at most 2 positional arguments (3 given)
WARNING: [__init__.py:44 - autodetect() ] - file_cache is unavailable when using oauth2client >= 4.0.0
Traceback (most recent call last):
  File "/Users/andrey9kin/code/onboarding-as-code/env/lib/python2.7/site-packages/googleapiclient/discovery_cache/__init__.py", line 41, in autodetect
    from . import file_cache
  File "/Users/andrey9kin/code/onboarding-as-code/env/lib/python2.7/site-packages/googleapiclient/discovery_cache/file_cache.py", line 41, in <module>
    'file_cache is unavailable when using oauth2client >= 4.0.0')
ImportError: file_cache is unavailable when using oauth2client >= 4.0.0
   INFO: [discovery.py:268 - _retrieve_discovery_doc() ] - URL being requested: GET https://www.googleapis.com/discovery/v1/apis/admin/directory_v1/rest
   INFO: [transport.py:157 - new_request() ] - Attempting refresh to obtain initial access_token
  DEBUG: [crypt.py:100 - make_signed_jwt() ] - ['eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImQxYjEwOGFjYWM1MDNkNGMyMWU3ODJiZTk5MGQwYTE3ZmVlMmNiZGUifQ', 'eyJhdWQiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20vby9vYXV0aDIvdG9rZW4iLCJleHAiOjE0ODQzNDk4NTAsImlhdCI6MTQ4NDM0NjI1MCwiaXNzIjoic2VydmljZS1hY2NvdW50QGVuZHVyaW5nLWJ5dGUtMTU1NTEyLmlhbS5nc2VydmljZWFjY291bnQuY29tIiwic2NvcGUiOiJodHRwczovL3d3dy5nb29nbGVhcGlzLmNvbS9hdXRoL2FkbWluLmRpcmVjdG9yeS51c2VyIGh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL2F1dGgvYWRtaW4uZGlyZWN0b3J5LmRvbWFpbiIsInN1YiI6ImFkbWluQHN5c2RldnByb3N1cC5vcmcifQ', 'UcAXk-HDPOzQcun0tJXb7tOiK3KZt6QWX_bQivj_J3p0SsTZW8rW_LM1TJbN1fH9DX6Moy6AX5_vGVLvV2jPM3STHdgEw0ObFQWBzW2ff2bhsrQbhfDEBizAvVZWq02MjoYEYoaB6B49TX-juPB_PdgtWky5zvwof83m0wpx1HG2yxO0BaJ5E1V93o4IsFaJXDn834d25cfR3IftOin2SKSuPbHjewb3pyZSM4wivbHHGCFUDHG_i1TtqyJT1yyalgHnEx0FfdOE6JCjtYx9eX8zpS75sXiw_MDGednfrd5gd7HT7tOh8Iz-qv3r86PBFWcnB2Ty9YqeuWjmnURU2A']
   INFO: [client.py:772 - _do_refresh_request() ] - Refreshing access_token
   INFO: [google_client.py:25 - authorize() ] - Looking for domains
   INFO: [discovery.py:857 - method() ] - URL being requested: GET https://www.googleapis.com/admin/directory/v1/customer/my_customer/domains?alt=json
  DEBUG: [google_client.py:28 - authorize() ] - Found domains: [u'sysdevprosup.org']
   INFO: [google_client.py:31 - get_all_users() ] - Getting all users
   INFO: [discovery.py:857 - method() ] - URL being requested: GET https://www.googleapis.com/admin/directory/v1/users?customer=my_customer&orderBy=email&alt=json
  DEBUG: [google_client.py:36 - get_all_users() ] - Found user: admin
  DEBUG: [google_client.py:36 - get_all_users() ] - Found user: ady
  DEBUG: [google_client.py:36 - get_all_users() ] - Found user: lakrus
   INFO: [yamlad.py:46 - get_all_accounts() ] - Reading all records from /Users/andrey9kin/code/onboarding-as-code/test_directory
  DEBUG: [yamlad.py:50 - get_all_accounts() ] - Found record: admin.yaml
  DEBUG: [yamlad.py:50 - get_all_accounts() ] - Found record: lakrus.yaml
   INFO: [main.py:47 - delete_removed_google_accounts() ] - Accounts that exists in google but not in directory: set([u'ady'])
   INFO: [google_client.py:58 - delete_user() ] - Delete user ady in domain sysdevprosup.org
   INFO: [discovery.py:857 - method() ] - URL being requested: DELETE https://www.googleapis.com/admin/directory/v1/users/ady%40sysdevprosup.org?
```

### Test bed

* Google suite: sysdevprosup.org, details: https://github.com/Praqma/onboarding-as-code/issues/4
* GitHub test org: https://github.com/sysdevprosup
* We have service account created for the automated tests. Encrypted key stored in test_credentials. Read more about encrypted secrets here https://docs.travis-ci.com/user/encrypting-files/
