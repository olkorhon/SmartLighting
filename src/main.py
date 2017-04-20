from __future__ import print_function

import pandas as pd
import numpy as np

from dbconfig import DB_CONFIG
from db_api import LightSenseDatabase

from bokeh_heatmap import makeHeatmap
from bokeh_network import makeNetwork

class Node(object):

    def __init__(self, location, data=None):
        self.pos_x = location["x"]
        self.pos_y = location["y"]
        self.temp_readings = None
        self.humidity_readings = None
        self.cycle_readings = None
        self.voltage_reading = None
        self.all_readings = pd.DataFrame(data, index=['Timestamp'], columns=["Temperature", "Humidity", "Cycle count", "Voltage"])

    def get_temperatures_by_time_window(self, start_time, end_time):
        return self.temp_readings.ix[start_time:end_time]
    
    def get_measurement_count_by_time_window(self, start_time, end_time):
        return self.temp_readings.ix[start_time:end_time].shape[0]
        
    def get_measurements_count_by_day(self):
        return self.temp_readings.groupby(pd.TimeGrouper(freq='D')).size()
        
    def get_measurements_count_by_hour(self):
        return self.temp_readings.groupby(pd.TimeGrouper(freq='H')).size()

    def get_measurements_count_by_15_min(self):
        return self.temp_readings.groupby(pd.TimeGrouper(freq='15Min')).size()
        
    def get_measurements_count_by_minute(self):
        return self.temp_readings.groupby(pd.TimeGrouper(freq='Min')).size()


def main():
    try:
        db = LightSenseDatabase(DB_CONFIG)
    except:
        main()
        return
        
    nodes = {}
    node_ids = set()

    # Fetch unique nodes
    for row in db.get_nodes():
        if row.node_id not in node_ids:
            node_ids.add(row.node_id)
            nodes[row.node_id] = Node(row.location)

    makeNetwork(nodes)

    # Fetch data to nodes
    for node_id in node_ids:
        print ("Processing node:", str(node_id))
        temperature_readings = db.get_node_temperatures_by_node_id(node_id)
        nodes[node_id].temp_readings = pd.DataFrame.from_records(temperature_readings, index=['Timestamp'], exclude=['Measurement'])
        #print (nodes[node_id].temp_readings.tail())

    # This is my jam brah
    #testLocation = {'x': 1337, 'y': 1337}
    #newTestNode = Node(testLocation)
    
    #temperature_readings = db.get_node_temperatures_by_node_id(250)
    #newTestNode.temp_readings = pd.DataFrame.from_records(temperature_readings, index=['Timestamp'], exclude=['Measurement'])
 
    #print(newTestNode.temp_readings)
    #print(newTestNode.get_temperatures_by_time_window('2016-01-01 00:00:00','2016-01-10 12:00:00'))
    #print(newTestNode.get_measurement_count_by_time_window('2016-01-01 00:00:00','2016-01-10 12:00:00'))
    #print(newTestNode.get_measurements_count_by_day())
    #print(newTestNode.get_measurements_count_by_hour())
    #print(newTestNode.get_measurements_count_by_15_min()) 
    #print(newTestNode.get_measurements_count_by_minute())

    makeHeatmap(nodes)
    
    
if __name__ == "__main__":
    main()
