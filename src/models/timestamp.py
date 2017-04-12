from models import base
from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import INTEGER, TIMESTAMP
from sqlalchemy.orm import relationship

class Timestamp(base):
    __tablename__ = "ValueTime"
    id = Column("Id", INTEGER, primary_key=True)
    event_timestamp = Column("EventTimestamp", TIMESTAMP)