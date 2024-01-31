import os
import sys
from TestManager import TestManager

if __name__ == '__main__':
    files = [file for file in os.listdir(os.getcwd()) if
             file.endswith(".py") and file != "TestManager.py" and file != "Test.py"]
    if len(files) == 0:
        sys.exit("No tests found")
    for file in files:
        module_name = file.replace(".py", "")
        __import__(module_name)

    TestManager(int(sys.argv[1]) if len(sys.argv) >= 2 else 0).start()
