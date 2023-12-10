from sqlalchemy.orm import sessionmaker
from .engine import get_engine

engine = get_engine()

Session = sessionmaker(engine)
