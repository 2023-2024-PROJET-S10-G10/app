sqlite_prefix = "sqlite+pysqlite:///"
name_DB = "mycigri.db"

path_DB = sqlite_prefix + "SQL/" + name_DB

def getPath(path):
    return sqlite_prefix + path + name_DB

def validation (value, default):
    if value is None or value <= 0:
        return default
    else:
        return value

