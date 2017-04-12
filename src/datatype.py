from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()

class DataType(base):
    __tablename__ = "DataType"
    id = Column("Id", Integer, primary_key=True)
    description = Column("Description", String)
    unit = Column("Unit", String)
    symbol = Column("Symbol", String)