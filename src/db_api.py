from __future__ import print_function
from sqlalchemy import create_engine, cast, Date
from sqlalchemy import Table, Column, String, Integer, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import sessionmaker
from sys import exit
from datetime import datetime

from dbconfig import DB_CONFIG
import constants
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
        Return all nodes without position
    '''
    def get_nodes_without_locations(self):
        return self.session.query(Location).filter(Location.location.is_(None))

    '''
        Return all events (Value) of nodes with positions.
        Optional timeframe inputs.
        See Event model for accessable data.
    '''
    def get_events(self, start_time=None, end_time=None):
        query = self.session.query(Event).join(Measurement).join(Location).join(Timestamp) \
        .filter(Event.measurement_id == Measurement.id) \
        .filter(Measurement.node_id == Location.id) \
        .filter(Location.location.isnot(None))

        if start_time is not None:
            query = query.filter(cast(Timestamp.event_timestamp, Date) >= start_time)

        if end_time is not None:
            query = query.filter(cast(Timestamp.event_timestamp, Date) <= end_time)

        return query.all()

    def get_events_as_dict(self, start_time=None, end_time=None):
        return [{   "Timestamp": u.timestamp.event_timestamp,
                    "Measurement": u.measurement.measurement_type.description,
                    "Value": u.value,
                    "NodeId": u.measurement.node.node_id} for u in self.get_events(start_time, end_time)]

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
        return self._get_node_events_of_type(node_id, constants.TEMPERATURE)

    def get_node_humidities(self, node_id):
        return self._get_node_events_of_type(node_id, constants.HUMIDITY)

    def get_node_cycle_counts(self, node_id):
        return self._get_node_events_of_type(node_id, constants.CYCLE_COUNT)

    def get_node_voltages(self, node_id):
        return self._get_node_events_of_type(node_id, constants.VOLTAGE)

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
     
     
    def get_node_events_of_type_by_node_id_by_time_window(self, node_id, measurement_type_id, start_time=None, end_time=None):
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
                    .join(Measurement).join(Location).join(Timestamp) \
                    .filter(Event.measurement_id == Measurement.id) \
                    .filter(Measurement.node_id == Location.id) \
                    .filter(Location.node_id == node_id) \
                    .filter(Measurement.measurement_type_id == measurement_type_id) \
                    .filter(Timestamp.event_timestamp > start_time) \
                    .filter(Timestamp.event_timestamp < end_time)]


    def get_node_temperatures_by_node_id(self, node_id):
        """
        Return all temperature events for a single node.

        :param node_id: int 
        :return: list of all temperature events for a single node.
        """
        return self._get_node_events_of_type_by_node_id(node_id, constants.TEMPERATURE)



    def get_node_humidities_by_node_id(self, node_id):
        """
        Return all humidity events for a single node.

        :param node_id: int 
        :return: list of all humidity events for a single node.
        """
        return self._get_node_events_of_type_by_node_id(node_id, constants.HUMIDITY)

    def get_node_cycle_counts_by_node_id(self, node_id):
        """
        Return all cycle count events for a single node.

        :param node_id: int 
        :return: list of all cycle count events for a single node.
        """
        return self._get_node_events_of_type_by_node_id(node_id, constants.CYCLE_COUNT)

    def get_node_voltages_by_node_id(self, node_id):
        """
        Return all voltage events for a single node.

        :param node_id: int 
        :return: list of all voltage events for a single node.
        """
        return self._get_node_events_of_type_by_node_id(node_id, constants.VOLTAGE)

    def get_node_events_of_type_by_node_id_by_time_window(self, node_id, measurement_type_id, start_time=None, end_time=None):
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
                    .join(Measurement).join(Location).join(Timestamp) \
                    .filter(Event.measurement_id == Measurement.id) \
                    .filter(Measurement.node_id == Location.id) \
                    .filter(Location.node_id == node_id) \
                    .filter(Measurement.measurement_type_id == measurement_type_id) \
                    .filter(Timestamp.event_timestamp > start_time) \
                    .filter(Timestamp.event_timestamp < end_time)]



def main():
    db = LightSenseDatabase(DB_CONFIG)
    r = db.get_events(datetime(2015, 11, 1), datetime(2015, 11, 2))
    print(len(r))

if __name__ == "__main__":
    main()
