from os import name
from Models.setting import Server
import constants
import requests
from Models.network import API_KEY

class Leaderboard():
    def __init__(self):
        self.leaderboards = {}
        self.leaderboardDicts = {}
        self.session = requests.Session()
        self.updateAll()

    def updateAll(self):
        for server in list(Server):
            self.updateLeaderboard(server.value)

    def updateLeaderboard(self, server):
        if server not in self.leaderboards:
            self.leaderboards[server] = None
        try:
            leaderboardRequest = self.session.get(self.getLeaderboardLink(server))
        except requests.exceptions.RequestException as e:
            print('getPlayerName error: ', e)
            return
        leaderboard = leaderboardRequest.json().get('players')
        headers = leaderboardRequest.headers
        if not leaderboardRequest.ok:
            print('getPlayerName error with status', leaderboardRequest.headers)
            if 'Retry-After' in headers:
                print('server is busy', headers['Retry-After'], 'seconds')
            return
        if leaderboard is not None:
            self.leaderboards[server] = leaderboard
            self.leaderboardDicts[server] = {board['name'].lower():{'rank':board['rank'], 'lp':board['lp']} for board in leaderboard}

    def getLeaderboard(self, server):
        if self.leaderboards[server] is None:
            self.updateLeaderboard(server)
        return self.leaderboards[server]

    def checkRank(self, name, server):
        rank = ''
        lp = ''
        if name is None:
            print('checkRank: empty name')
            return rank, lp
        board = self.getLeaderboard(server)
        if board is None:
            return rank, lp
        info = self.leaderboardDicts[server][name.lower()]
        # for playerRank in board:
        #     if playerRank['name'].lower() == name.lower():
        #         rank = str(playerRank['rank'] + 1)
        #         lp = str(int(playerRank['lp']))
        return info['rank'], info['lp']
    def getLeaderboardLink(self, server):
        return 'https://' + server + constants.LEADERBOARD_KEY + API_KEY
