#!/usr/bin/env python

import os
import yaml
import logging as log
from person import Person
from organisation import Organisation

# This is what we need for onboarding https://github.com/Praqma/onboarding-as-code/issues/1

"""
Class to handle Yaml based "AD" records
path - path to directory which contains AD records

AD structure
- <pid>.yaml - one file per person
"""

class YamlAD:
    def __init__(self, path):
        self.path = path
        self.org_file_name = "org"

    def __get_filename(self, pid):
        return os.path.join(self.path, "{}.yaml".format(pid))

    def add_person(self, person):
        file_name = self.__get_filename(person.pid)
        log.info("Saving {} on disk {}".format(person.pid, file_name))
        log.debug("Writing: {}".format(person))
        with open(file_name, "w") as file_obj:
            file_obj.write(yaml.dump(person, default_flow_style=False))

    def get_person(self, pid):
        file_name = self.__get_filename(pid)
        log.info("Reading {} from disk {}".format(pid, file_name))
        with open(file_name, "r") as file_obj:
            person = yaml.load(file_obj)
            return Person(person.pid,
                          person.gid,
                          person.fname,
                          person.lname,
                          person.email)

    def get_all_accounts(self):
        log.info("Reading all records from {}".format(self.path))
        result = []
        for _dirname, _suddirlist, flist in os.walk(self.path):
            for fname in flist:
                log.debug("Found record: {}".format(fname))
                result.append(fname.replace(".yaml", ""))
        return result

    def add_org(self, org):
        file_name = self.__get_filename(self.org_file_name)
        log.info("Saving {} on disk {}".format(org.goid, file_name))
        log.debug("Writing: {}".format(org))
        with open(file_name, "w") as file_obj:
            file_obj.write(yaml.dump(org, default_flow_style=False))

    def get_org(self):
        file_name = self.__get_filename(self.org_file_name)
        log.info("Reading org {} from the disk".format(file_name))
        with open(file_name, "r") as file_obj:
            pyaml = yaml.load(file_obj)
            return Organisation(pyaml.goid, pyaml.ghoid)
