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

    def _get_node_events_of_type(self, node_id, measurement_type_id):
        """
        node_id = Location.Id (not Location.NodeId)
        """
        return [{   "Timestamp": u.timestamp.event_timestamp, 
                    "Measurement": u.measurement.measurement_type.description,
                    "Value": u.value} for u in self.session.query(Event) \
        .join(Measurement).join(Location) \
        .filter(Event.measurement_id == Measurement.id) \
        .filter(Measurement.node_id == Location.id) \
        .filter(Location.id == node_id) \
        .filter(Measurement.measurement_type_id == measurement_type_id)]

    def get_node_temperatures(self, node_id):
        return self._get_node_events_of_type(node_id, 4)

    def get_node_humidities(self, node_id):
        return self._get_node_events_of_type(node_id, 5)

    def get_node_cycle_counts(self, node_id):
        return self._get_node_events_of_type(node_id, 6)

    def get_node_voltages(self, node_id):
        return self._get_node_events_of_type(node_id, 7)

    def _get_node_events_of_type_by_node_id(self, node_id, measurement_type_id):
        """
        Return all events of certain type for a single node.
        
        :param node_id: int
        :param measurement_type_id: int
        :return: list of dicts
        Keys: 
            Timestamp(datetime)
            Measurement(string)
            Value(float)
        """
        return [{"Timestamp": u.timestamp.event_timestamp,
                 "Measurement": u.measurement.measurement_type.description,
                 "Value": u.value} for u in self.session.query(Event) \
                    .join(Measurement).join(Location) \
                    .filter(Event.measurement_id == Measurement.id) \
                    .filter(Measurement.node_id == Location.id) \
                    .filter(Location.node_id == node_id) \
                    .filter(Measurement.measurement_type_id == measurement_type_id)]

    def get_node_temperatures_by_node_id(self, node_id):
        """
        Return all temperature events for a single node.

        :param node_id: int 
        :return: list of all temperature events for a single node.
        """
        return self._get_node_events_of_type_by_node_id(node_id, 4)

    def get_node_humidities_by_node_id(self, node_id):
        """
        Return all humidity events for a single node.

        :param node_id: int 
        :return: list of all humidity events for a single node.
        """
        return self._get_node_events_of_type_by_node_id(node_id, 5)

    def get_node_cycle_counts_by_node_id(self, node_id):
        """
        Return all cycle count events for a single node.

        :param node_id: int 
        :return: list of all cycle count events for a single node.
        """
        return self._get_node_events_of_type_by_node_id(node_id, 6)

    def get_node_voltages_by_node_id(self, node_id):
        """
        Return all voltage events for a single node.

        :param node_id: int 
        :return: list of all voltage events for a single node.
        """
        return self._get_node_events_of_type_by_node_id(node_id, 7)

def main():
    db = LightSenseDatabase(DB_CONFIG)
    temp_list = db.get_node_temperatures_by_node_id(253)
    print(len(temp_list))
    #print(db.get_node_humidities(347))
    #print(db.get_node_cycle_counts(347))
    #print(db.get_node_voltages(347))

if __name__ == "__main__":
    main()
