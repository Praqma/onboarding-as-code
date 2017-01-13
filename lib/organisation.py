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
