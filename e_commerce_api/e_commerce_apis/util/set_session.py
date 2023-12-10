from typing import Generator
from e_commerce_api.e_commerce_db.session import Session


def get_session() -> Generator:
    session = Session()
    try:
        yield session
    finally:
        session.close()
