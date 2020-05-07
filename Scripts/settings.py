import os
import json


class Settings:
    def __init__(self, path):
        self.path = path

    def get(self, key, default):
        if os.path.isfile(self.path):
            with open(self.path, "r") as f:
                j = json.load(f)
                if key in j:
                    return j[key]
        return default

    def set(self, key, value):
        j = {}
        if os.path.isfile(self.path):
            with open(self.path, "r") as f:
                j = json.load(f)
        j[key] = value

        with open(self.path, "w+") as f:
            f.write(json.dumps(j, indent=4, sort_keys=True))
