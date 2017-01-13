#!/usr/bin/env python

import sys
import argparse
import logging as log

from lib.person import Person
from lib.organisation import Organisation
from lib.yamlad import YamlAD

def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="print debug info", dest="debug",
                        action="store_true")
    parser.add_argument("-n", "--dry-run", help="only print what would be executed", dest="dry",
                        action="store_true")
    parser.add_argument("-p", "--path", help="path to the organisation directory", dest="path",
                        required=True)
    subparsers = parser.add_subparsers(help="This is what you can do")
    parser_add = subparsers.add_parser("add", help="Go through the records and add all new users")
    parser_del = subparsers.add_parser("del", help="Go through recodrs and remove ones that are registred but not present in our records")

    return parser.parse_args()

def main(argv):
    args = parse_args(argv)

    log_format = "%(levelname)7s: [%(filename)s:%(lineno)s - %(funcName)s() ] - %(message)s"
    if args.debug == True:
        log.basicConfig(level=log.DEBUG, format=log_format)
    else:
        log.basicConfig(level=log.INFO, format=log_format)

    person = Person("ady",
                "andrey9kin",
                "Andrey",
                "Devyatkin",
                "andrey.a.devyatkin@gmail.com")
    ad = YamlAD(args.path)
    org = ad.get_org()
    ad.add_person(person)
    print ad.get_person(person.pid)

if __name__ == "__main__":
    main(sys.argv)
