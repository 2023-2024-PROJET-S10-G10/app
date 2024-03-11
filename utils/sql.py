# To use in app folder
path_DB = "sqlite+pysqlite:///SQL/mycigri.db"

# To use in Test folder
path_DB_test = "sqlite+pysqlite:///../Test/SQL/mycigri_test.db"


def validation(value, default):
    if value is None or value <= 0:
        return default
    else:
        return value
