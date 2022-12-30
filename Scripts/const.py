import sys
from pathlib import Path


class Const:
    version = "1.0.0"
    updateurl = "https://raw.githubusercontent.com/tiuub/RemotePlayTogetherHelper/master/VERSION"

    reldir = Path(sys.executable).parent
    gamesjsonpath = "%s/RPTH_games.json" % reldir
    settingsjsonpath = "%s/RPTH_settings.json" % reldir

    banner = "\n"
    banner = banner + " #################################\n"
    banner = banner + " #                               #\n"
    banner = banner + " #  Remote Play Together Helper  #\n"
    banner = banner + " #                               #\n"
    banner = banner + " #################################\n"

    W = '\033[0m'  # white (normal)
    R = '\033[31m'  # red
    G = '\033[32m'  # green
    O = '\033[33m'  # orange
    B = '\033[34m'  # blue
    P = '\033[35m'  # purple
    BB = '\033[90m'  # bright black

    settingsEnableUpdatesKey = "ENABLEUPDATES"
    settingsLastUpdatePollStampKey = "LASTUPDATEPOLLSTAMP"
    settingsUpdateIntervalKey = "UPDATEINTERVAL"
