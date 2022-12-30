import re
import requests
import sys
import os
import subprocess
import time
from pathlib import Path
from packaging import version


class Updater:
    rawresponse = None
    W = '\033[0m'  # white (normal)
    R = '\033[31m'  # red
    G = '\033[32m'  # green
    O = '\033[33m'  # orange
    B = '\033[34m'  # blue
    P = '\033[35m'  # purple
    BB = '\033[90m'  # bright black

    def __init__(self, updateurl, version):
        self.updateurl = updateurl
        self.version = version

    def printc(self, text="", color=W):
        print(color + text + self.W)

    def poll(self):
        r = requests.get(self.updateurl, timeout=2)

        if r.status_code == 200:
            self.rawresponse = r.text
            self.printc(" Local version: %s - Newes version: %s" %
                        (self.version, r.text.split(":")[0]), self.B)
            self.printc()
            if version.parse(r.text.split(":")[0]) > version.parse(self.version):
                return True
        return False

    def update(self):
        self.printc()
        if self.rawresponse is None:
            self.printc(" Fetching the download url.")
            r = requests.get(self.updateurl)
            if r.status_code == 200:
                self.rawresponse = r.text

        if re.fullmatch("([0-9\.]+(alpha|beta|dev)?)(:)((http[s]?|ftp)://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)", self.rawresponse.rstrip()) is not None:
            self.printc()
            self.printc(" New version: %s" %
                        self.rawresponse.split(":")[0], self.G)
            self.printc()
            self.printc(" Downloading the newer version. (May take a while.)")
            r = requests.get(
                str.join(":", self.rawresponse.split(":")[1:]).rstrip())
            if r.status_code == 200:
                tmpexepath = Path("%s/%s.%s.%s" % (os.getenv("TEMP"), Path(
                    sys.executable).name, time.strftime("%Y%m%d_%H%M%S"), "tmp"))
                self.printc(" Downloaded the newer version.")
                self.printc(" Writing it to a temp directory.")
                with open(tmpexepath, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=128):
                        f.write(chunk)
                self.printc("\t-> %%TEMP%%/%s" % tmpexepath.name, self.BB)

                self.printc()
                self.printc("Running the updater batch file:", self.O)
                batchpath = Path(
                    "%s/%s.%s.%s" % (os.getenv("TEMP"), "PythonUpdater", time.strftime("%Y%m%d_%H%M%S"), "bat"))
                with open(batchpath.__str__(), "w") as f:
                    f.write(("@echo off\r\n"
                             "echo  This batch script will switch the old with the new file.\r\n"
                             "timeout 5 /nobreak\r\n"
                             "echo. & echo  Killing now the running task.\r\n"
                             "TASKKILL /F /pid {pid}\r\n"
                             "echo. & echo  Deleting the old file.\r\n"
                             "DEL \"{exepath}\"\r\n"
                             "timeout 3 /nobreak\r\n"
                             "echo. & echo  Moving the new file to the old location.\r\n"
                             "move \"{tmpexepath}\" \"{exepath}\"\r\n"
                             "timeout 3 /nobreak\r\n"
                             "echo. & echo  Starting the new version!\r\n"
                             "start \"{exepath}\" \"{exepath}\"\r\n"
                             "echo. & echo  The update is now finished. Ignore the following error message and press Enter or close the window.\r\n"
                             "DEL \"%~f0\"\r\n"
                             "Pause\r\n").format(pid=os.getpid(), exepath=sys.executable, tmpexepath=tmpexepath))
                if os.path.isfile(batchpath.__str__()):
                    subprocess.Popen([batchpath.__str__()], shell=True,
                                     stdin=None, stderr=None, close_fds=None)
                    sys.exit(0)
                else:
                    self.printc(
                        " There happened an error, during calling the batch script.", self.R)
            else:
                self.printc(
                    " There was an error, during downloading the new version.", self.R)
        else:
            self.printc(
                " There was an error, during fetching the version.", self.R)
