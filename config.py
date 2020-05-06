"""
This file contains all of the configuration values for the application.
"""
import os
import platform

# The secret key is used by Flask to encrypt session cookies.
SECRET_KEY = 'secret'

# Alternatively, you could use a local MySQL instance for testing.
LOCAL_MYSQL_CONFIG = {
    "address": "localhost",
    "port": 3306,
    "user":"hao",
    "password": "root",
    "database": "personal_tool"
}


def __get_database_uri(db_dict):
    address = db_dict.get("address")
    port = db_dict.get("port")
    user = db_dict.get("user")
    password = db_dict.get("password")
    database = db_dict.get("database")
    return f"mysql+pymysql://{user}:{password}@{address}:{port}/{database}"

if platform.system() == "Windows":
    SQLALCHEMY_DATABASE_URI = __get_database_uri(db_dict=LOCAL_MYSQL_CONFIG)
else:
    print("Unknown system")