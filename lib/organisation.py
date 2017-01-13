#!/usr/bin/env python

"""
Data class to hold info about organisations in Praqma
goid - Google Suite id
ghoid - GitHub org id
"""

class Organisation:
    def __init__(self, goid, ghoid):
        self.goid = goid
        self.ghoid = ghoid
    def __repr__(self):
        return "{}(goid={}, ghoid={})".format(
            self.__class__.__name__,
            self.goid,
            self.ghoid)
