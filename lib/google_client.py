import httplib2
import os
import json
import logging as log

from oauth2client.service_account import ServiceAccountCredentials
from apiclient import discovery

# TODO: add support for https://developers.google.com/drive/v3/web/handle-errors

# API reference
# https://developers.google.com/resources/api-libraries/documentation/admin/directory_v1/python/latest/index.html

class GoogleSuiteClient:
    def __init__(self, json_key=""):
        self.json_key = json_key
        self.service = None
        self.domains = None

    def authorize(self, user_email):
        log.info("Authorizing credentials")
        # See list of all scopes here https://developers.google.com/identity/protocols/googlescopes
        scopes = ["https://www.googleapis.com/auth/admin.directory.user",
                  "https://www.googleapis.com/auth/admin.directory.domain"]
        # Read more here https://developers.google.com/api-client-library/python/auth/service-accounts
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.json_key,scopes)
        # https://developers.google.com/admin-sdk/directory/v1/guides/delegation
        credentials = credentials.create_delegated(user_email)
        http = credentials.authorize(httplib2.Http())
        log.info("Building service")
        self.service = discovery.build('admin', 'directory_v1', http)
        log.info("Looking for domains")
        results = self.service.domains().list(customer="my_customer").execute()
        self.domains = [domain_obj["domainName"] for domain_obj in results.get("domains", [])]
        log.debug("Found domains: {}".format(self.domains))

    def get_all_users(self):
        log.info("Getting all users")
        results = self.service.users().list(customer="my_customer", orderBy="email").execute()
        userlist = []
        for user in results.get("users", []):
            username = user["primaryEmail"].split("@")[0]
            log.debug("Found user: {}".format(username))
            userlist.append(username)
        return userlist

    def create_user(self, uid, fname, lname, dry_run=False):
        for domain in self.domains:
            email = "{}@{}".format(uid, domain)
            log.info("Creare user {} in domain {}".format(uid, domain))
            userinfo = { "primaryEmail": email,
                         "name": { "givenName": fname, "familyName": lname },
                         "password": fname+lname,
                         "changePasswordAtNextLogin": True }
            log.debug("Creation params: {}".format(userinfo))
            if not dry_run:
                user = self.service.users().insert(body=userinfo).execute()
                log.debug("Created user: {}".format(user))
            else:
                log.info("DRY RUN: Create user with parameters: {}".format(userinfo))

    def delete_user(self, uid, dry_run=False):
        for domain in self.domains:
            email = "{}@{}".format(uid, domain)
            log.info("Delete user {} in domain {}".format(uid, domain))
            if not dry_run:
                self.service.users().delete(userKey=email).execute()
            else:
                log.info("DRY RUN: Delete user {}".format(email))

    def add_alias(self, uid, alias, dry_run=False):
        for domain in self.domains:
            email = "{}@{}".format(uid, domain)
            email_alias = "{}@{}".format(alias, domain)
            log.info("Add alias {} for user {} in domain {}".format(alias, uid, domain))
            aliasinfo = { "alias": email_alias, "primaryEmail": email }
            if not dry_run:
                self.service.users().aliases().insert(userKey=email, body=aliasinfo).execute()
            else:
                log.info("DRY RUN: Create alias with parameters: {}".format(aliasinfo))
