from sqlalchemy.orm import declarative_base
from sqlalchemy import MetaData


metadata = MetaData(schema="ecom")
Base = declarative_base(metadata=metadata)
