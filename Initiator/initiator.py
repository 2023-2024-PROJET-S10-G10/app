import uvicorn
import sys
import os
import subprocess

sys.path.append(sys.path[0].replace("/Initiator", ""))

from utils.sql import *

if __name__ == "__main__":
    # initialize DB
    if os.path.exists("SQL/" + name_DB):
        print("DB found successfully.")
    else:
        subprocess.run(["python", "SQL/Config_BDD.py"])

    # launch CiGri's API
    sys.path.append(sys.path[0].replace("/Initiator", "/API/CiGri"))
    uvicorn.run("ServerApi:app", reload=True)
