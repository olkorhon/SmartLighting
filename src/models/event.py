from models import base
from sqlalchemy import Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import INTEGER, DOUBLE_PRECISION
from sqlalchemy.orm import relationship

class Event(base):
    __tablename__ = "Value"
    id = Column("Id", INTEGER, primary_key=True)
    value = Column("Value", DOUBLE_PRECISION)
    timestamp_id = Column("ValueTimeId", INTEGER, ForeignKey("ValueTime.Id"))
    measurement_id = Column("DataPointId", INTEGER, ForeignKey("DataPoint.Id"))

    timestamp = relationship("Timestamp", foreign_keys=timestamp_id)
    measurement = relationship("Measurement", foreign_keys=measurement_id)