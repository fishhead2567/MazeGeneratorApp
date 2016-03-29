__author__ = 'best'

import json
from os.path import isfile

def CreateConfig():
    config = {
        "maze": {
            "background_color": "#FFFFFF",
            "walls_color": "#000000",
            "solution_colors": ["#FF0000",
                                "#00FF00",
                                "#0000FF",
                                "#E5DD14",
                                "#FF8B00",
                                "#D31AFF"],
            "pawn_color": "#FF0000",

        },
        "zoom_speed" : 1.2,
    }
    with open("config.json", "w+") as fp:
        fp.write(json.dumps(config,indent=4))

def LoadConfig():
    with open("config.json", "r") as fp:
        config = json.loads(fp.read())
        print json.dumps(config, indent=4, sort_keys=True)
        return config

def CreateOrLoadConfig():
    if not isfile("config.json"):
        CreateConfig()

    return LoadConfig()
if __name__ == "__main__":
    if not isfile("config.json"):
        CreateConfig()
    else:
        LoadConfig()