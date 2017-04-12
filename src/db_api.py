from __future__ import print_function
from sqlalchemy import create_engine, and_
from sqlalchemy import Table, Column, String, Integer, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sys import exit

from dbconfig import DB_CONFIG
import models

from models.location import Location
from models.timestamp import Timestamp
from models.measurement_type import MeasurementType
from models.measurement import Measurement
from models.event import Event

class LightSenseDatabase(object):

    def __init__(self, config):
        try:
            db_string = "postgresql://{USER}:{PASSW}@{HOST}:{PORT}/{DBNAME}".format(**config)
            self.engine = create_engine(db_string)
            self.base = declarative_base()
            self.base.metadata.create_all(self.engine)
            self.session = sessionmaker(self.engine)()

        except:
            print("Cannot connect to the database, please check that the settings are configured correctly.")
            exit()
    '''
        Return all measurement types (DataType).
        See MeasurementType model for accessable data.
    '''
    def get_measurement_types(self):
        return self.session.query(MeasurementType)

    '''
        Return all nodes (Location) with position.
        See Location model for accessable data.
    '''
    def get_nodes(self):
        return self.session.query(Location).filter(Location.location.isnot(None)).order_by(Location.id)

    '''
        Return all events (Value) of nodes with positions.
        See Event model for accessable data.
    '''
    def get_events(self):
        return self.session.query(Event).join(Measurement).join(Location) \
        .filter(Event.measurement_id == Measurement.id) \
        .filter(Measurement.node_id == Location.id) \
        .filter(Location.location.isnot(None))

def main():
    db = LightSenseDatabase(DB_CONFIG)
    records = db.get_events()
    for record in records:
        print("%s @ %s" % (record.id, record.timestamp.event_timestamp))

if __name__ == "__main__":
    main()
