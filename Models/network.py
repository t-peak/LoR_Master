from Models.process import isSimulation
import locale
API_KEY = '?api_key=' + 'RGAPI-5cfa0b1c-8d06-4d65-b9f7-3738e745fc7b'  #ios new github release
API_KEY0 = '?api_key=' + 'RGAPI-5cfa0b1c-8d06-4d65-b9f7-3738e745fc7b'  #ios new github release
API_KEY1 = '?api_key=' + 'RGAPI-693e34b0-9890-4591-a22d-36df07ccde53'  #ios product development
API_KEY2 = '?api_key=' + 'RGAPI-3dd1641a-6d80-458d-9fb5-357253d7674b'  #product github release
API_KEY3 = '?api_key=' + 'RGAPI-3b5bde16-66b4-4943-b8fa-241d27b29344'  #personal qq release
MATCH_KEY = '.api.riotgames.com/lor/match/v1/matches/by-puuid/'
DETAILS_KEY = '.api.riotgames.com/lor/match/v1/matches/'
NAME_KEY = '.api.riotgames.com/riot/account/v1/accounts/by-puuid/'
PUUID_KEY = '.api.riotgames.com/riot/account/v1/accounts/by-riot-id/'

sysLanguage = locale.getdefaultlocale()[0]
print('System Language: ', sysLanguage)

if 'en' in sysLanguage:
    API_KEY = API_KEY0
elif 'zh' in sysLanguage:
    API_KEY = API_KEY3
else:
    API_KEY = API_KEY2

if isSimulation():
    API_KEY = API_KEY1

print('API_KEY Used: ', API_KEY, isSimulation())


class Network():
    def __init__(self, setting) -> None:
        self.setting = setting
        self.key = API_KEY
        return

    def getHeadLink(self):
        return 'https://' + self.setting.getServer()

    def getMatchsLink(self, ppid):
        return self.getHeadLink() + MATCH_KEY + ppid + '/ids' + self.key

    def getDetailsLink(self, matchId):
        return self.getHeadLink() + DETAILS_KEY + matchId + self.key

    def getNameLink(self, ppid):
        return self.getHeadLink() + NAME_KEY + ppid + self.key

    def getPUUID(self, name, tag):
        return self.getHeadLink() + PUUID_KEY + name + '/' + tag + self.key
