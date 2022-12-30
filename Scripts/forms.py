import os
import shutil
import subprocess
import sys
import time
import datetime
import shlex


from const import Const
from pathlib import Path


class Forms:
    def __init__(self, updater, games, settings):
        self.updater = updater
        self.games = games
        self.settings = settings

    def cls(self):
        os.system('cls')
        print(Const.banner)

    def printc(self, text, color=Const.W):
        print(color + text + Const.W)

    def newline(self):
        print()

    def showAddGame(self):
        self.cls()
        self.printc("Adding a new game:")
        self.newline()
        name = input(" Please enter the name of the game: ")
        while True:
            path = input(" Please enter the path to the .exe of the game: ")
            if os.path.isfile(path):
                break
            self.printc(" Please enter a valid file.", Const.R)
        args = input(
            " Enter any command-line args, or just press enter to skip: ")
        self.games.addgame(name=name, path=path, args=args)

    def showAddedGame(self, name):
        self.cls()
        self.printc(" Added %s to the list!" % name)

    def showRenameGame(self, index):
        self.cls()
        self.printc(" Additional commands:", Const.BB)
        self.printc("\tback or quit (Must be equals)", Const.BB)
        self.newline()
        c = input(" Type in the new name for %s: " %
                  (self.games.getname(index=index)))
        if c.lower() == "quit":
            sys.exit(0)
        elif c.lower() != "back":
            self.games.setname(index=index, name=c)

    def showUpdateArgsGame(self, index):
        self.cls()
        self.printc(" Additional commands:", Const.BB)
        self.printc("\tback or quit (Must be equals)", Const.BB)
        self.newline()
        self.printc(
            f" Current args for {self.games.getname(index=index)}: {self.games.getargs(index=index)}")
        c = input(" Type in the new args for %s: " %
                  (self.games.getname(index=index)))
        if c.lower() == "quit":
            sys.exit(0)
        elif c.lower() != "back":
            self.games.setargs(index=index, args=c)

    def showDeleteGame(self, index):
        self.cls()
        self.printc(" Selected Game:")
        self.printc("\tID:\t%i" % (index + 1), Const.G)
        self.printc("\tName:\t%s" % self.games.getname(index=index), Const.G)
        self.printc("\tPath:\t\"%s\"" %
                    (self.games.getpath(index=index)), Const.BB)
        if self.games.getargs(index=index):
            self.printc(
                f"\tArgs:\t{self.games.getargs(index=index)}", Const.BB)
        self.newline()

        c = input(Const.R + " Do you really want to delete \"%s\" (yes|no)?: " % (
            self.games.getname(index=index)) + Const.W).lower()
        if c[0] == "y":
            self.games.deletegame(index=index)

    def showGamelist(self, help=False):
        self.cls()
        self.printc(" Games list:")

        self.games.loadgames()
        games = self.games.games

        for i in range(0, len(games)):
            if self.games.gethost(index=i):
                self.printc("\t[%i]\t%s [HOST]" %
                            (i + 1, self.games.getname(index=i)), Const.G)
            else:
                self.printc("\t[%i]\t%s" %
                            (i + 1, self.games.getname(index=i)), Const.G)

        self.newline()
        self.printc(" Additional commands:")
        self.printc("\t[%i]\tAdd new game - Enter also \"add\"" %
                    (len(games) + 1), Const.O)
        self.printc("\t[%i]\tUninstall - Enter also \"uninstall\"" %
                    (len(games) + 2), Const.O)
        self.printc("\t[%i]\tSettings - Enter also \"settings\"" %
                    (len(games) + 3), Const.O)
        self.printc("\t[%i]\tQuit - Enter also \"quit\"" %
                    (len(games) + 4), Const.O)
        self.printc("\t[%i]\tHelp - Enter also \"help\"" %
                    (len(games) + 5), Const.O)
        self.newline()

        if help:
            self.printc(" Help page:", Const.BB)
            self.printc(
                "\t<ID>\t\t- Entering the ID of a game, will select it", Const.BB)
            self.printc(
                "\tadd\t\t\t- Will provide a form, to easily add an game", Const.BB)
            self.printc(
                "\tuninstall\t- Will uninstall the Helper and all its data", Const.BB)
            self.printc(
                "\tquit\t\t- Will instantly close the application", Const.BB)

        while True:
            index = input(" Enter a number (1, 2, 3...): ").lower()

            if index.isdigit():
                index = int(index)

            if isinstance(index, int) and 0 <= int(index) - 1 < len(games):
                self.showGame(int(index) - 1)
                break
            elif index == len(games) + 1 or str(index)[0] == "a":
                self.showAddGame()
                break
            elif index == len(games) + 2 or str(index)[0] == "u":
                self.showUninstall()
                break
            elif index == len(games) + 3 or str(index)[0] == "s":
                self.showSettings()
                break
            elif index == len(games) + 4 or str(index)[0] == "q":
                sys.exit(0)
            elif index == len(games) + 5 or str(index)[0] == "h":
                self.showGamelist(True)
                break
            else:
                self.printc(" Please enter a valid game id!", Const.R)

    def showGame(self, index):
        self.cls()
        self.printc(" Selected Game:")
        self.printc("\tID:\t%i" % (index + 1), Const.G)
        self.printc("\tName:\t%s" % self.games.getname(index=index), Const.G)
        self.printc("\tPath:\t\"%s\"" %
                    self.games.getpath(index=index), Const.BB)
        if self.games.getargs(index=index):
            self.printc(
                f"\tArgs:\t{self.games.getargs(index=index)}", Const.BB)
        self.newline()
        self.printc(" Choose a action:")
        self.printc("\t(s)tart\t\t- Will start the game", Const.G)
        self.printc(
            "\t(a)rgs\t\t- Will update command-line args for the game", Const.O)
        self.printc("\t(d)elete\t- Will remove the game from the list", Const.O)
        self.printc("\t(r)ename\t- Will rename the game", Const.O)
        self.printc("\t(b)ack\t\t- Will go back to the game selection", Const.O)
        self.printc(
            "\t(q)uit\t\t- Will instantly close the application", Const.O)
        self.newline()

        while True:
            action = input(" Please enter your action here: ").lower()
            if action[0] == "s":
                self.showStartGame(index)
                break
            elif action[0] == "a":
                self.showUpdateArgsGame(index)
                break
            elif action[0] == "d":
                self.showDeleteGame(index)
                break
            elif action[0] == "r":
                self.showRenameGame(index)
                break
            elif action[0] == "b":
                break
            elif action[0] == "q":
                sys.exit(0)
            else:
                self.printc(
                    " Wrong action! Please enter one of the given options!", Const.R)

    def showStartGame(self, index):
        self.cls()
        self.printc("%s will started now!" % self.games.getname(index=index))
        if os.path.isfile(self.games.getpath(index=index)):
            path = Path(self.games.getpath(index=index))
            os.chdir(path.parent)
            if self.games.getargs(index=index):
                subprocess.Popen([path.__str__()] + shlex.split(self.games.getargs(index=index)), stdin=None,
                                 stderr=None, close_fds=None)
            else:
                subprocess.Popen([path.__str__()], stdin=None,
                                 stderr=None, close_fds=None)
            sys.exit(0)

    ##################
    # Tool utilities #
    ##################

    def showUninstall(self):
        self.cls()
        self.printc("Uninstalling Guide:")
        hostgame = None
        for game in self.games.games:
            if "host" in game and game["host"] == True:
                hostgame = game
                break
        if hostgame is not None:
            self.printc(
                " The hostgame %s will be moved back to its original folder." % hostgame["name"])
            self.printc(" Current path:\t%s" % hostgame["path"], Const.O)
            self.printc(" New Path:\t%s" % Const.reldir, Const.G)
            self.newline()
        else:
            self.printc(
                " No hostgame found. Cant restore the original game!", Const.R)
            self.newline()

        self.printc(
            " The following folder an all its components will be deleted!:")
        self.printc(" %s" % Const.reldir, Const.R)
        for file in Const.reldir.rglob("*"):
            self.printc(" %s" % file.__str__(), Const.R)
        self.newline()

        self.printc(" Additional commands:")
        self.printc(
            "\tback - Will go back to the Gamelist and cancel the process", Const.O)
        self.printc(
            "\tquit - Will close the tool immediately and cancel the process", Const.O)
        self.newline()

        while True:
            c = input(
                " Please type \"uninstall\" to confirm the process: ").lower()
            if c[0] == "b":
                break
            elif c[0] == "q":
                sys.exit(0)
            elif c == "uninstall":
                path = Path(os.getenv("TEMP"))
                if hostgame is not None:
                    modifiedpath = Path(hostgame["path"])
                os.chdir(Const.reldir.parent)
                with open("%s/RemotePlayTogetherHelperUninstaller.bat" % path.__str__(), "w") as f:
                    f.write(("@echo off\r\n"
                             "echo This .bat file is written to the TEMP directory and will delete the RemotePlayTogetherHelper\r\n"
                             "timeout 5 /nobreak\r\n"
                             "echo. & echo Killing now the RemotePlayTogetherHelper task.\r\n"
                             "TASKKILL /F /pid {pid}\r\n"
                             "echo. & echo Deleting the RemotePlayTogetherHelper executable and all its components.\r\n"
                             "rmdir /Q /S \"{parentpath}\"\r\n"
                             + (("timeout 5 /nobreak\r\n"
                                 "echo. & echo Moving the Host game back to the original folder.\r\n"
                                 "move /Y \"{modifiedpath}\" \"{parentpath}\"\r\n").format(parentpath=Const.reldir,
                                                                                           modifiedpath=modifiedpath.parent) if hostgame is not None else "")
                             + "echo. & echo. & echo. & echo. & echo The RemotePlayTogetherHelper is now uninstalled!\r\n"
                               "echo. & echo. & echo. & Pause\r\n"
                               "echo. & echo Deleting now the uninstaller file itself. Ignore the following error message and press Enter or close the window.\r\n"
                               "DEL \"%~f0\"\r\n"
                               "Pause").format(pid=os.getpid(), parentpath=Const.reldir))
                if os.path.isfile("%s/RemotePlayTogetherHelperUninstaller.bat" % path.__str__()):
                    subprocess.Popen(["%s/RemotePlayTogetherHelperUninstaller.bat" % path.__str__()], shell=True,
                                     stdin=None, stderr=None, close_fds=None)
                    sys.exit(0)
                else:
                    input(
                        Const.R + " Error! Cant uninstall the Tool. Press Enter." + Const.W)

    def showUpdate(self, force=False):
        self.cls()
        self.printc(" Checking for an update.", Const.O)
        self.newline()
        if self.settings.get(Const.settingsEnableUpdatesKey, True) or force:
            if (datetime.datetime.now() - datetime.datetime.fromtimestamp(float(self.settings.get(Const.settingsLastUpdatePollStampKey, 0)))).days >= int(self.settings.get(Const.settingsUpdateIntervalKey, 7)) or force:
                self.settings.set(
                    Const.settingsLastUpdatePollStampKey, datetime.datetime.now().timestamp())
                if self.updater.poll():
                    self.printc(
                        " There is a new version of the tool available!", Const.G)
                    self.newline()
                    c = input(
                        " Do you want to download the newer version (yes|no)?: ").lower()
                    if c[0] == "y":
                        self.newline()
                        self.printc(" Updating the tool now!", Const.O)
                        self.updater.update()
                else:
                    self.printc(
                        " There is no newer version available!", Const.R)
                    self.newline()

    def showSetup(self):
        self.cls()
        c = input(" Do you want to use the setup guide (yes|no)?: ").lower()
        if c[0] == "y":
            self.newline()
            self.printc(
                " To use this tool, you have to install a RemotePlayTogether compatibel game via steam.")
            self.newline()
            self.printc(
                " If you have done this, please enter the complete path to the .exe of the game.")
            self.printc(" Example: \"C:/Program Files (x86)/Steam/steamapps/common/Lego Batman/LEGBatman.exe\"",
                        Const.BB)
            while True:
                path = input(" Please enter the path (or (q)uit): ")
                if os.path.isfile(path):
                    path = Path(path)
                    break
                elif path.lower()[0] == "q":
                    sys.exit(0)
                else:
                    self.printc(
                        " You have entered a wrong path. Look at the example.", Const.R)
            parentpath = Path(path).parent
            modifiedpath = str(parentpath) + \
                "RPTH_%s" % (time.strftime("%Y%m%d_%H%M%S"))
            os.rename(parentpath, modifiedpath)
            if not os.path.exists(parentpath):
                os.makedirs(parentpath)
            shutil.copy(sys.executable, path)
            time.sleep(3)
            subprocess.call(
                [str(path), '--name', path.stem, '--path', "%s/%s" % (modifiedpath, path.name), '--host', '--noui'])
            self.newline()
            self.printc(
                " Setup finished successfully. You can now start %s via steam to start the RemotePlayTogetherHelper." % path.stem,
                Const.G)
            self.newline()
            input(Const.G + " Press Enter to exit." + Const.W)
            sys.exit(0)
        else:
            self.printc(" The manual installation process takes x steps.")
            self.printc(
                "\t1. Go to the files of a RemotePlayTogehter compatible game. Right click in Steam -> Properties -> Local files -> Browse local files.")
            self.printc(
                "\t2. Copy all the gamefiles to another place and remember the .exe name.")
            self.printc(
                "\t3. Copy the RemotePlayTogether.exe to the emptied folder of the game and rename it like the remembered .exe name.")
            self.printc(
                "\t4. Open the renamed .exe, type in \"no\" and press Enter afterwards.")
            self.printc("\t5. Now you can add games to the list.")
            self.printc(
                "\t6. To use it, go into Steam to the Game you choose at beginning and press Play.")
            self.printc("\t7. You can close this guide now.")
            input("Press Enter to continue...")

    ############
    # Settings #
    ############

    def showSettings(self):
        while True:
            self.cls()
            self.printc(" Settings:")
            self.newline()
            self.printc("\t[1] Enable updates (1=Yes|0=No):\t%i" % self.settings.get(
                Const.settingsEnableUpdatesKey, 1), Const.G)
            self.printc("\t[2] Update interval (in days):\t\t%i" % self.settings.get(
                Const.settingsUpdateIntervalKey, 2), Const.G)
            self.printc("\t[3] Last update poll (read only):\t%s" % datetime.datetime.fromtimestamp(float(
                self.settings.get(Const.settingsLastUpdatePollStampKey, 0))).strftime("%Y-%m-%d %H:%M:%S"), Const.G)
            self.printc("\t[4] Checking for updates", Const.G)
            self.newline()
            self.printc(" Additional commands:")
            self.printc("\t(b)ack - Goes back to the game list", Const.O)
            self.printc("\t(q)uit - Closes the tool immediately.", Const.O)
            self.newline()

            c = input(" Enter the number you want to change: ").lower()

            self.newline()
            if c[0] == "q":
                sys.exit(0)
            elif c[0] == "b":
                break
            elif c.isdigit() and int(c) == 1:
                while True:
                    c = input(
                        " Enter 1 for enabling or 0 for disabling updates: ")
                    if c.isdigit() and 0 <= int(c) <= 1:
                        self.settings.set(
                            Const.settingsEnableUpdatesKey, int(c))
                        break
            elif c.isdigit() and int(c) == 2:
                while True:
                    c = input(
                        " Enter a value for the update interval (in days): ")
                    if c.isdigit() and 0 <= int(c):
                        self.settings.set(
                            Const.settingsUpdateIntervalKey, int(c))
                        break
            elif c.isdigit() and int(c) == 4:
                self.showUpdate(force=True)
                input(" Press Enter to continue...")
            else:
                self.printc(
                    " Please enter a valid number or type quit or back!", Const.R)
