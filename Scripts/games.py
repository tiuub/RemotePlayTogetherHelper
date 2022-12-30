import json
import os


class Games:
    games = []

    def __init__(self, path):
        self.path = path
        if os.path.isfile(path):
            self.loadgames()

    def loadgames(self):
        if os.path.isfile(self.path):
            with open(self.path, "r") as f:
                self.games = json.load(f)

    def savegames(self):
        with open(self.path, "w+") as f:
            f.write(json.dumps(self.games))
        if os.path.isfile(self.path):
            return True
        return False

    def addgame(self, name, path, host=False):
        game = {"name": name, "path": path, "host": host}
        self.games.append(game)
        if self.savegames():
            return True
        return False

    def deletegame(self, index):
        if 0 <= index < len(self.games):
            del self.games[index]
            if self.savegames():
                return True
        return False

    def getname(self, index):
        if 0 <= index < len(self.games) and "name" in self.games[index]:
            return self.games[index]["name"]
        return False

    def getpath(self, index):
        if 0 <= index < len(self.games) and "path" in self.games[index]:
            return self.games[index]["path"]
        return False

    def gethost(self, index):
        if 0 <= index < len(self.games) and "host" in self.games[index]:
            return self.games[index]["host"]
        return False

    def setname(self, index, name):
        if 0 <= index < len(self.games) and "name" in self.games[index]:
            self.games[index]["name"] = name
            if self.savegames():
                return True
        return False

    def setpath(self, index, path):
        if 0 <= index < len(self.games) and "path" in self.games[index]:
            self.games[index]["path"] = path
            if self.savegames():
                return True
        return False

    def sethost(self, index, host):
        if 0 <= index < len(self.games) and "host" in self.games[index]:
            self.games[index]["host"] = host
            if self.savegames():
                return True
        return False
