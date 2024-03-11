sqlite_prefix = "sqlite+pysqlite:///"
name_DB = "mycigri.db"

# To use for production (default)
path_DB = sqlite_prefix + "SQL/" + name_DB

# For testing
path_DB_test = sqlite_prefix + "../Test/SQL/mycigri_test.db"

def getPath(path):
    return sqlite_prefix + path + name_DB

def validation (value, default):
    if value is None or value <= 0:
        return default
    else:
        return value

