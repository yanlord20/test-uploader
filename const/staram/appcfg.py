import os
"""
Database
"""
DBHOST = os.environ.get("DBHOST", "localhost")
DBUSER = os.environ.get("DBUSER", "root")
DBPWD = os.environ.get("DBPWD", "")
DBNAME = os.environ.get("DBNAME", "staram_db_dev")
DBPORT = os.environ.get("DBPORT", 3306)
DBCHARSET = "utf8"

"""
TTL
"""
TTLDAY = 86400
TTLSHORT = 1200
TTLINQ = 300
TTLHR = 3600