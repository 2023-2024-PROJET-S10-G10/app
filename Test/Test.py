import os
import sys
from TestManager import TestManager

# Appends the parent directory of the current directory to the Python module search path.
sys.path.append(sys.path[0].replace("Test", ""))

if __name__ == "__main__":
    files = [
        file
        for file in os.listdir(os.getcwd())
        if file.endswith(".py")
        and file != "TestManager.py"
        and file != "Test.py"
    ]
    if len(files) == 0:
        print(
            "No tests found (Did you run the command in app/Test/ directory ?)"
        )
        exit(1)
    for file in files:
        module_name = file.replace(".py", "")
        __import__(module_name)

    passed = TestManager(int(sys.argv[1]) if len(sys.argv) >= 2 else 0).start()
    exit(0 if passed else 1)
