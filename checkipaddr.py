
import dns
import dns.resolver
import urllib.request
import re

class CheckIpAddr:
    blacklists = []

    def __init__(self):
        pass

    def readBlacklistFromDB(self):
        pass

    def checkIPinBlackList(self, ipaddr, blacklist):
        ret = False

        try: 
            # document https://www.spamcop.net/fom-serve/cache/351.html
            resolver = dns.resolver.Resolver()
            query = '.'.join(reversed(str(ipaddr).split("."))) + "." + blacklist
            resolver.timeout = 5
            resolver.lifetime = 5
            resp = resolver.query(query, "A")
            resp_txt = resolver.query(query, "TXT")
            print(resp_txt)
            ret = True
        except dns.resolver.NXDOMAIN:
            ret = False
        except dns.resolver.Timeout:
            print("Timeout")
        except Exception as e:
            print(e)


        return ret

    def checkIPsUsingUrl(self, ips, url):
        badIps = []
        with urllib.request.urlopen(url) as f:
            html = f.read().decode("utf-8")
            for ipaddr in ips:
                matches =  re.findall(ipaddr, html)
                goodIP = len(matches) == 0
                if ~goodIP:
                    badIps.append(ipaddr)
        return badIps

    def checkIPurl(self, ipaddr, url):
        goodIP = False
        with urllib.request.urlopen(url) as f:
            html = f.read().decode("utf-8")
            matches =  re.findall(ipaddr, html)
            goodIP = len(matches) == 0

        return goodIP

if __name__ == '__main__':
    cia = CheckIpAddr()

    cia.checkIPinBlackList("1.2.3.4", "bl.spamcop.net")

    #cia.checkIPurl("34.172.237.230", "http://rules.emergingthreats.net/blockrules/compromised-ips.txt")
    cia.checkIPurl("202.164.139.168", "http://reputation.alienvault.com/reputation.data")