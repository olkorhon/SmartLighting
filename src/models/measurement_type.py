from models import base
from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import INTEGER, TEXT

class MeasurementType(base):
    __tablename__ = "DataType"
    id = Column("Id", INTEGER, primary_key=True)
    description = Column("Description", TEXT)
    unit = Column("Unit", TEXT)
    symbol = Column("Symbol", TEXT)