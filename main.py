#!/usr/bin/env python

import sys
import argparse
import logging as log

from lib.yamlad import YamlAD
from lib.google_client import GoogleSuiteClient

def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="print debug info", dest="debug",
                        action="store_true")
    parser.add_argument("-n", "--dry-run", help="only print what would be executed", dest="dry_run",
                        action="store_true")
    parser.add_argument("-p", "--path", help="path to the organisation directory", dest="path",
                        required=True)
    parser.add_argument("-k", "--google-key", help="path to Google service account private key", dest="key",
                        required=True)
    parser.add_argument("-e", "--email", help="email to autorize, i.e. service account will be acting on behalf of this user", dest="email",
                        required=True)
    subparsers = parser.add_subparsers(help="This is what you can do")
    parser_add = subparsers.add_parser("add", help="Go through all records in the directory and create all users that are not registred yet in Google and other services")
    parser_add.set_defaults(which='add')
    parser_del = subparsers.add_parser("del", help="Go through all recodrs in the direcoty and remove ones that are registred in Google and other services but not present in our records")
    parser_del.set_defaults(which='del')

    return parser.parse_args()

def create_added_google_accounts(client, ad, dry_run):
    # diff will contain set with elements that are present in ad_accounts
    # but not in google_accounts
    diff = set(ad.get_all_accounts()).difference(client.get_all_users())
    log.info("Accounts that exists in directory but not in google: {}".format(diff))
    for account in diff:
        person = ad.get_person(account)
        client.create_user(account, person.fname, person.lname, dry_run)
        client.add_alias(account, person.gid, dry_run)
        client.add_alias(account,
                         str("{}.{}".format(person.fname, person.lname)).lower(),
                         dry_run)

def delete_removed_google_accounts(client, ad, dry_run):
    # diff will contain set with elements that are present in google_accounts
    # but not in ad_accounts
    diff = set(client.get_all_users()).difference(ad.get_all_accounts())
    log.info("Accounts that exists in google but not in directory: {}".format(diff))
    for account in diff:
        client.delete_user(account, dry_run)

def main(argv):
    args = parse_args(argv)

    log_format = "%(levelname)7s: [%(filename)s:%(lineno)s - %(funcName)s() ] - %(message)s"
    if args.debug == True:
        log.basicConfig(level=log.DEBUG, format=log_format)
    else:
        log.basicConfig(level=log.INFO, format=log_format)

    client = GoogleSuiteClient(args.key)
    client.authorize(args.email)
    ad = YamlAD(args.path) 

    if args.which == "add":
        create_added_google_accounts(client, ad, args.dry_run)
    elif args.which == "del":
        delete_removed_google_accounts(client, ad, args.dry_run)
    else:
        log.error("Unsupported command: {}".format(args.which))
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv)
