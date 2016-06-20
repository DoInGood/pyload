# -*- coding: utf-8 -*-

import time
import xml.dom.minidom

from module.common.json_layer import json_loads
from module.plugins.internal.Account import Account


class RealdebridCom(Account):
    __name__    = "RealdebridCom"
    __type__    = "account"
    __version__ = "0.47"

    __description__ = """Real-Debrid.com account plugin"""
    __license__     = "GPLv3"
    __authors__     = [("Devirex Hazzard", "naibaf_11@yahoo.de")]


    def loadAccountInfo(self, user, req):
        json = req.load("https://api.real-debrid.com/rest/1.0/user?auth_token={0}".format(self.accounts[user]["password"]))
        account = json_loads(json)

        validuntil = time.time() + account["premium"]

        return {'validuntil' : validuntil,
                'trafficleft': -1        ,
                'premium'    : True      }


    def login(self, user, data, req):
        json = req.load("https://api.real-debrid.com/rest/1.0/user?auth_token={0}".format(data["password"]))
        account = json_loads(json)

        if not user == account["username"]:
            self.wrongPassword()
        else:
            self.logWarning("logged in")
