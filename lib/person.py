#!/usr/bin/env python

import yaml

"""
Data class to hold info about a person in Praqma
pid - Praqma id, i.e. Google Suite id
gid - GitHub id, i.e. GitHub handle
fname - first name
lname - last name
email - private email
"""

class Person:
    def __init__(self, pid, gid, fname, lname, email):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.gid = gid
        self.pid = pid
    def __repr__(self):
        return "{}(pid={}, gid={}, email={}, fname={}, lname={})".format(
            self.__class__.__name__,
            self.pid,
            self.gid,
            self.email,
            self.fname,
            self.lname)
