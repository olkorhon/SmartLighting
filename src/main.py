from __future__ import print_function

from datetime import datetime, date
import pprint

import pandas as pd
import numpy as np

from dbconfig import DB_CONFIG
from db_api import LightSenseDatabase
import constants

import Bokeh.visualization


class Node(object):

    def __init__(self, node_id, location=None, data=None):
        self.node_id = node_id
        self.pos_x = location["x"]
        self.pos_y = location["y"]
        self.temp_readings = None
        self.humidity_readings = None
        self.cycle_readings = None
        self.voltage_readings = None
        self.all_readings = pd.DataFrame(data, index=['Timestamp'], columns=["Temperature", "Humidity", "Cycle count", "Voltage"])

    def get_temperatures_by_time_window(self, start_time, end_time):
        return self.temp_readings.ix[start_time:end_time]

    def get_measurement_count_by_time_window(self, start_time, end_time):
        return self.temp_readings.ix[start_time:end_time].shape[0]

    def get_measurements_grouped_by_day(self):
        return self.temp_readings.groupby(pd.TimeGrouper(freq='D'))

    def get_measurements_count_by_day(self):
        return self.temp_readings.groupby(pd.TimeGrouper(freq='D')).size()

    def get_measurements_grouped_by_hour(self):
        return self.temp_readings.groupby(pd.TimeGrouper(freq='H'))

    def get_measurements_count_by_hour(self):
        return self.temp_readings.groupby(pd.TimeGrouper(freq='H')).size()

    def get_measurements_count_by_15_min(self):
        return self.temp_readings.groupby(pd.TimeGrouper(freq='15Min')).size()

    def get_measurements_count_by_minute(self):
        return self.temp_readings.groupby(pd.TimeGrouper(freq='Min')).size()

class NodeContainer(object):

    def __init__(self, db_conn):
        self.db = db_conn
        self.id_node_map = {}

    def put_temp_events_to_all_nodes(self, start_time=None, end_time=None):
        for node_id in self.id_node_map.keys():
            tempe_readings = self.db.get_node_events_of_type_by_node_id_by_time_window(node_id, constants.TEMPERATURE,
                                                                                       start_time, end_time)
            self.id_node_map[node_id].temp_readings = pd.DataFrame.from_records(tempe_readings, index=['Timestamp'])

    def put_voltage_events_to_all_nodes(self, start_time=None, end_time=None):
        for node_id in self.id_node_map.keys():
            voltage_readings = self.db.get_node_events_of_type_by_node_id_by_time_window(node_id, constants.VOLTAGE,
                                                                                         start_time, end_time)
            self.id_node_map[node_id].voltage_readings = pd.DataFrame.from_records(voltage_readings,
                                                                                   index=['Timestamp'])

    def calc_traffic_between_nodes(self, source_node, sink_node, offset_lowbound, offset_upbound, sensor_cooldown):
        # offset_lowbound = excpected shortest time in seconds that it takes to walk between nodes
        # offset_lowbound = excpected longest time in seconds that it takes to walk between nodes

        source_node_df = source_node.temp_readings
        sink_node_df = sink_node.temp_readings

        traffic_ctr = 0
        event_timestamps = []

        # This decides that how many seconds window are events suppressed when traffic between nodes occurs
        sensor_cooldown_time = sensor_cooldown

        cooldown_counter = 0
        for timestamp in list(source_node_df.index):

            if cooldown_counter > 0:
                # Sensor is on cooldown state, skip to next simestramp
                cooldown_counter = cooldown_counter - 1
                continue


            start_time = timestamp + pd.DateOffset(seconds=offset_lowbound)
            end_time = timestamp + pd.DateOffset(seconds=offset_upbound)

            count = sink_node_df.ix[start_time:end_time].shape[0]
            if (count > 1):
                # Movement found, add cooldown to sensor

                # Taking cooldown time window
                cooldown_window_start = timestamp + pd.DateOffset(seconds=1)
                cooldown_window_end = timestamp + pd.DateOffset(seconds=sensor_cooldown_time)
                events_on_cooldown_window = source_node_df.ix[cooldown_window_start:cooldown_window_end].shape[0]

                # Add skip amount of found events
                cooldown_counter = events_on_cooldown_window
                # print("Cooldownwindow events %d" % cooldown_counter)
                # Add movement to list
                event_timestamps.append(timestamp)

        df = pd.DataFrame(event_timestamps, index=event_timestamps)
        grouped_by_hour = df.groupby(pd.TimeGrouper(freq='H')).size()
        print(grouped_by_hour)
        print("\n")
        return traffic_ctr

    def get_hourly_events_for_all_nodes_grouped_by_day(self):
        """
        :return: dict of node_id : {datetime.date : hourly_events_list}
        """
        hourly_events_per_node_per_day = {}
        for id, node in self.id_node_map.iteritems():
            grouped = node.get_measurements_grouped_by_day()
            daily_events = {}
            for label, day_group in grouped:
                num_of_events_by_hour = day_group.groupby(pd.TimeGrouper(freq='H')).size()
                hourly_event_counts = [(key.to_datetime().hour, val) for key, val in num_of_events_by_hour.iteritems()]
                day = label.to_datetime().date()
                daily_events[day] = hourly_event_counts
                hourly_events_per_node_per_day[id] = daily_events
        return hourly_events_per_node_per_day

    def get_traffic_on_neighbour_nodes_at_vtt(self):
        node_pairs = [[259, 254],
                      [254, 256],
                      [254, 251],
                      [256, 251],
                      [251, 252],
                      [252, 258],
                      [252, 253],
                      [253, 258],
                      [253, 250],
                      [250, 257]
                      ]

        for pair in node_pairs:
            source_node = pair[0]
            sink_node = pair[1]

            print("Traffic from node %d to node %d" % (source_node, sink_node))
            self.calc_traffic_between_nodes(self.id_node_map[source_node], self.id_node_map[sink_node], 5, 15, 6)

            print("Traffic from node %d to node %d" % (sink_node, source_node))
            self.calc_traffic_between_nodes(self.id_node_map[sink_node], self.id_node_map[source_node], 5, 15, 6)




class NodeEnergy(object):

    def __init__(self, location, data=None):
        self.cycle_readings = None
        self.all_readings = pd.DataFrame(data, index=['Timestamp'], columns=["Cycle count"])

def main(start_time, end_time):
    # Fix this monstrosity
    try:
        db = LightSenseDatabase(DB_CONFIG)
    except:
        main(start_time, end_time)
        return

    container = NodeContainer(db)

    # Fill NodeContainer with all the unique Nodes
    node_ids = set()
    for row in db.get_nodes():
        if row.node_id not in node_ids:
            node_ids.add(row.node_id)
            container.id_node_map[row.node_id] = Node(row.node_id, row.location)


    container.put_temp_events_to_all_nodes(start_time, end_time)

    pp = pprint.PrettyPrinter(indent=4)
    events_hourly = container.get_hourly_events_for_all_nodes_grouped_by_day()
    pp.pprint(events_hourly)

    Bokeh.visualization.create(container.id_node_map, events_hourly)

    '''
    Fetch unique nodes without locations (for cycle counts)
    '''
    nodes_energy = {}
    node_energy_ids = set()
    for row in db.get_nodes_without_locations():
        if row.node_id not in node_energy_ids:
            node_energy_ids.add(row.node_id)
            nodes_energy[row.node_id] = NodeEnergy(row.location)
    # Calculate energy savings for one day
    print(calculate_energy_savings_for_day(db, "2016-01-25"))

    # Fetch data to nodes

    #for node_id in [250, 257, 259, 254, 253, 251, 252, 256, 258]:
    #    print ("Processing node:", str(node_id))
    #    temperature_readings = db.get_node_temperatures_by_node_id(node_id)
    #    nodes[node_id].temp_readings = pd.DataFrame.from_records(temperature_readings, index=['Timestamp'], exclude=['Measurement'])

        #print (nodes[node_id].temp_readings.tail())


    # Uncomment next line to unleash true power of calculatin and printing all traffict at vvt builgin on neighbour nodes
    container.get_traffic_on_neighbour_nodes_at_vtt()

    makeHeatmap(nodes)



    #source_node_df = nodes[251].get_temperatures_by_time_window(datetime(2016, 1, 15), datetime(2016, 1, 16))
    #sink_node_df = nodes[252].get_temperatures_by_time_window(datetime(2016, 1, 15), datetime(2016, 1, 16))
    #print("From node 251 to node 252")
    #calc_traffic_between_nodes(source_node_df, sink_node_df, 15)
    #print("From node 252 to node 251")
    #calc_traffic_between_nodes(sink_node_df, source_node_df, 15)

    # This is my jam brah
    #testLocation = {'x': 1337, 'y': 1337}
    #newTestNode = Node(testLocation)

    #temperature_readings = db.get_node_temperatures_by_node_id(250)
    #newTestNode.temp_readings = pd.DataFrame.from_records(temperature_readings, index=['Timestamp'], exclude=['Measurement'])

    # print(newTestNode.temp_readings)
    # print(newTestNode.get_temperatures_by_time_window('2016-01-01 00:00:00','2016-01-10 12:00:00'))
    # print(newTestNode.get_measurement_count_by_time_window('2016-01-01 00:00:00','2016-01-10 12:00:00'))
    # print(newTestNode.get_measurements_count_by_day())
    # print(newTestNode.get_measurements_count_by_hour())
    # print(newTestNode.get_measurements_count_by_15_min())
    # print(newTestNode.get_measurements_count_by_minute())


def calculate_energy_savings_for_day(database, day):
    energy_savings_dict = {}
    for node_id in range(1, 36): #nodes 1-35 have cyclecounts
        #print ("Processing node:", str(node_id))
        time_morning = "%s 06:00:00" % day
        time_evening = "%s 18:00:00" % day
        cycle_readings = database.get_node_events_of_type_by_node_id_by_time_window(node_id, 6, time_morning, time_evening)
        if cycle_readings == []:
            energy_savings_dict[node_id] = 100
        else:
            cycle_readings_df = pd.DataFrame.from_records(cycle_readings, index=['Timestamp'], exclude=['Measurement'])
            energy_savings_dict[node_id] = (43200 - (cycle_readings_df.iloc[-1] - cycle_readings_df.iloc[0])) / 432  # in percents
    energy_savings = pd.DataFrame.from_dict(energy_savings_dict, orient='index')
    #print(energy_savings)
    if float(energy_savings.mean() <= 100):
        return float(energy_savings.mean())
    else:
        return 100

if __name__ == "__main__":
    start = datetime(2016, 1, 25)
    end = datetime(2016, 1, 31)
    main(start, end)