# -*- coding: utf-8 -*-

import re
import time
import urllib

from module.common.json_layer import json_loads
from module.plugins.internal.MultiHoster import MultiHoster, create_getInfo


class RealdebridCom(MultiHoster):
    __name__    = "RealdebridCom"
    __type__    = "hoster"
    __version__ = "0.68"

    __pattern__ = r'https?://((?:www\.|s\d+\.)?real-debrid\.com/dl/|[\w^_]\.rdb\.so/d/)[\w^_]+'
    __config__  = [("use_premium", "bool", "Use premium account if available", True)]

    __description__ = """Real-Debrid.com multi-hoster plugin"""
    __license__     = "GPLv3"
    __authors__     = [("Devirex Hazzard", "naibaf_11@yahoo.de")]


    def setup(self):
        self.chunkLimit = 3


    def handlePremium(self, pyfile):
        user = self.account.accounts.keys()[0]
        apitoken = self.account.accounts[user]["password"]

        url = "https://api.real-debrid.com/rest/1.0/unrestrict/link?auth_token={0}".format(apitoken)

        payload = {
            "link":     pyfile.url,
            "password": self.getPassword()
        }

        json = self.load(url, post=payload)
        data = json_loads(json)

        self.logDebug("Returned Data: %s" % data)
        
        if "error" in data:
            self.fail("{0} (code: {1})".format(data["error"], data["error_code"]))
        else:
            if data['filename']:
                pyfile.name = data['filename']
            pyfile.size = data['filesize']
            self.link = data['download']

        #if self.getConfig('ssl'):
        #    self.link = self.link.replace("http://", "https://")
        #else:
        #    self.link = self.link.replace("https://", "http://")


getInfo = create_getInfo(RealdebridCom)
