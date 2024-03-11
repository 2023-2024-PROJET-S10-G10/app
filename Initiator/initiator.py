import uvicorn
import sys
import os
import subprocess

sys.path.append(sys.path[0].replace("/Initiator", ""))

from utils.sql import *

if __name__ == "__main__":
    # initialize DB
    if len(sys.argv) == 3:
        if os.path.exists(sys.argv[2]):
            if not os.path.exists(sys.argv[2] + name_DB):
                subprocess.run(["python", "SQL/Config_BDD.py " + sys.argv[2]])
            else:
                print("DB found successfully.")
        else:
            print(f"Error: Your path ({sys.argv[2]}) doesn't exist.")
            sys.exit(1)
    else:
        if os.path.exists("SQL/" + name_DB):
            print("DB found successfully.")
        else:
            subprocess.run(["python", "SQL/Config_BDD.py"])

    # launch CiGri's API
    sys.path.append(sys.path[0].replace("/Initiator", "/API/CiGri"))
    uvicorn.run("ServerApi:app", reload=True)
