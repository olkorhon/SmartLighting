from models import base
from sqlalchemy import Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import INTEGER, DOUBLE_PRECISION, TIMESTAMP
from sqlalchemy.orm import relationship

class Measurement(base):
    __tablename__ = "DataPoint"
    id = Column("Id", INTEGER, primary_key=True)
    node_id = Column("LocationId", INTEGER, ForeignKey("Location.Id"))
    measurement_type_id = Column("DataTypeId", INTEGER, ForeignKey("DataType.Id"))

    node = relationship("Location", foreign_keys=node_id)
    measurement_type = relationship("MeasurementType", foreign_keys=measurement_type_id)