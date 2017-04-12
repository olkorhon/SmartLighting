from models import base
from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import INTEGER, TEXT, JSON

class Location(base):
    __tablename__ = "Location"
    id = Column("Id", INTEGER, primary_key=True)
    type_id = Column("TypeId", INTEGER)
    description = Column("Description", TEXT)
    location_parent_id = Column("LocationParentId", INTEGER)
    name = Column("Name", TEXT)
    node_id = Column("NodeId", INTEGER)
    location = Column("Location", JSON)
    grid_location = Column("Gridlocation", JSON)