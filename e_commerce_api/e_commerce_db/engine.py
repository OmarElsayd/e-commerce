import os

import sqlalchemy
from sqlalchemy.engine import create_engine


def get_curds() -> dict:
    return {
        "HOST": os.getenv("DB_HOST", default="localhost"),
        "USER": os.getenv("DB_USER", default="postgres"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "PORT": os.getenv("DB_PORT", 5432),
        "SCHEMA": os.getenv("SCHEMA", "ecom")
    }


def get_engine() -> sqlalchemy.Engine:
    creds = get_curds()
    connection_string = f"postgresql://{creds['USER']}:{creds['PASSWORD']}@{creds['HOST']}:{creds['PORT']}/postgres"
    engine = create_engine(connection_string)
    return engine
