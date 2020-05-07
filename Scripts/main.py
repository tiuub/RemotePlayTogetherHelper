# The executable was compiled with pyinstaller

import os
import sys
import argparse
from pathlib import Path
from const import Const
from forms import Forms
from games import Games
from updater import Updater
from settings import Settings


updater = Updater(Const.updateurl, Const.version)
games = Games(Const.gamesjsonpath)
settings = Settings(Const.settingsjsonpath)
forms = Forms(updater=updater, games=games, settings=settings)

parser = argparse.ArgumentParser()
parser.add_argument('--noui', action='store_true')
parser.add_argument('--name')
parser.add_argument('--path')
parser.add_argument('--host', action='store_true')
args = parser.parse_args()


if __name__ == "__main__":
    if args.name is not None and args.path is not None:
        if args.host is not None:
            games.addgame(args.name, args.path, args.host)
        else:
            games.addgame(args.name, args.path)
    if not args.noui:
        if not os.path.isfile(Const.gamesjsonpath):
            if "RemotePlayTogetherHelper" in Path(sys.executable).stem:
                forms.showSetup()
            else:
                forms.showUpdate()
                forms.showAddGame()
        forms.showUpdate()
        while True:
            forms.showGamelist()

# C:\Python\Python3.7.2\Scripts\pyinstaller.exe --onefile main.py