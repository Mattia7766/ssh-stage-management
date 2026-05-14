import os
import aiomysql
from .db_interface import DatabaseInterface

MYSQL_CONFIG = {
    "host":     os.environ.get("DB_HOST",     "localhost"),
    "port":     int(os.environ.get("DB_PORT", "3306")),
    "user":     os.environ.get("DB_USER",     "student"),
    "password": os.environ.get("DB_PASSWORD", "Pass"),
    "db":       os.environ.get("DB_NAME",     "DB_SSH_todo_app2"),
    "autocommit": True,
    "minsize": 1,
    "maxsize": 10,
}

COOKIE_SECRET = os.environ.get("COOKIE_SECRET", "super_secret_key_change_me")
PORT = int(os.environ.get("PORT", "8888"))  # Railway usa variabile PORT

_pool = None

async def init_pool():
    global _pool
    if _pool is None:
        _pool = await aiomysql.create_pool(**MYSQL_CONFIG)
    return _pool

def get_pool():
    return _pool

db_interface = DatabaseInterface(get_pool)
