#!/usr/bin/env python

"""
Data class to hold info about organizations in Praqma
goid - Google Suite id
ghoid - GitHub org id
"""
import os
import requests
from github import Github


class Organization:
    token = os.environ["GITHUB_TOKEN"]
    gh = Github(token)

    def __init__(self, goid, ghoid):
        self.goid = goid
        self.ghoid = ghoid
    def add_new_user_to_organization(self, organization, username):
        org = self.gh.get_organization(organization)
        url = "{}/memberships/{}".format(org.url, username)
        req = requests.put(url, headers={'Authorization': 'token %s' % self.token})
    def __repr__(self):
        return "{}(goid={}, ghoid={})".format(
            self.__class__.__name__,
            self.goid,
            self.ghoid)