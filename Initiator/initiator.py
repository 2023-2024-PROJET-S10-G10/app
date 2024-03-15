import uvicorn
import sys
import os

sys.path.append(sys.path[0].replace("/Initiator", ""))

from utils.sql import *


def initializeDB(path=None):
    if path is not None:
        path_local = sys.argv[1]
        if not path_local.endswith("/"):
            path_local += "/"

        if os.path.isdir(path_local):
            if os.path.isfile(path_local + name_DB):
                print("DB found successfully.")
            else:
                os.system("python SQL/Config_BDD.py " + path_local)
        else:
            # print(f"The path `{path_local}`is not valid.")
            print(
                f"The path `{path_local}` doesn't exist. So, we create this folder in /app."
            )
            os.mkdir(path_local)
            os.system("python SQL/Config_BDD.py " + path_local)
            sys.exit(1)
    else:
        if os.path.isfile("SQL/" + name_DB):
            print("DB found successfully.")
        else:
            os.system("python SQL/Config_BDD.py")


def launchAPI():
    sys.path.append(sys.path[0].replace("/Initiator", "/API/CiGri"))
    uvicorn.run("ServerApi:app", reload=True)


if __name__ == "__main__":
    # initialize DB
    initializeDB(sys.argv[1] if len(sys.argv) > 1 else None)

    # launch CiGri's API
    launchAPI()
