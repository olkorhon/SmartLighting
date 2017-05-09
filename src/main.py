from __future__ import print_function

import argparse
from datetime import datetime, date, timedelta
import pprint

import pandas as pd
import numpy as np

from dbconfig import DB_CONFIG
from db_api import LightSenseDatabase
import constants

import Bokeh.visualization


class Node(object):

    def __init__(self, node_id, node_type, location=None, data=None):
        self.node_id = node_id
        self.type = None                # 'PIR' or 'LAMP'
        if location:
            self.pos_x = location["x"]
            self.pos_y = location["y"]
        else:
            self.pos_x = None
            self.pos_y = None
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

    def put_cycle_count_events_to_node(self, node_id, start_time=None, end_time=None):
        cycle_counts = self.db.get_node_events_of_type_by_node_id_by_time_window(node_id, constants.CYCLE_COUNT,
                                                                                     start_time, end_time)
        if cycle_counts:
            self.id_node_map[node_id].cycle_readings = pd.DataFrame.from_records(cycle_counts,
                                                                                 index=['Timestamp'],
                                                                                 exclude=['Measurement'])

    def put_voltage_events_to_node(self, node_id, start_time=None, end_time=None):
        voltage_readings = self.db.get_node_events_of_type_by_node_id_by_time_window(node_id, constants.VOLTAGE,
                                                                                     start_time, end_time)
        if voltage_readings:
            self.id_node_map[node_id].voltage_readings = pd.DataFrame.from_records(voltage_readings,
                                                                                   index=['Timestamp'])

    def get_hourly_events_for_all_nodes_grouped_by_day(self):
        """
        :return: dict of node_id : {datetime.date : hourly_events_list}
        """
        hourly_events_per_node_per_day = {}
        print(self.id_node_map)
        for _id, node in self.id_node_map.iteritems():
            grouped = node.get_measurements_grouped_by_day()
            daily_events = {}
            for label, day_group in grouped:
                num_of_events_by_hour = day_group.groupby(pd.TimeGrouper(freq='H')).size()
                hourly_event_counts = [(key.to_pydatetime().hour, val) for key, val in num_of_events_by_hour.iteritems()]
                day = label.to_pydatetime().date()
                daily_events[day] = hourly_event_counts
                hourly_events_per_node_per_day[_id] = daily_events
        return hourly_events_per_node_per_day

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
        # grouped_by_hour = df.groupby(pd.TimeGrouper(freq='H')).size()
        return df
        #print(grouped_by_hour)
        #print("\n")
        #return traffic_ctr

    def format_traffic_events(self, traffic_events, source_node, sink_node):

        hourly_events_of_pair_per_day = {}

        traffic_events_by_day = traffic_events.groupby(pd.TimeGrouper(freq='D'))
        daily_traffic_events = {}
        for label, day_group in traffic_events_by_day:
            num_of_traffic_events_by_hour = day_group.groupby(pd.TimeGrouper(freq='H')).size()
            hourly_traffic_event_counts = [(key.to_pydatetime().hour, val) for key, val in
                                           num_of_traffic_events_by_hour.iteritems()]
            day = label.to_pydatetime().date()
            daily_traffic_events[day] = hourly_traffic_event_counts

            hourly_events_of_pair_per_day["from_node_id"] = source_node
            hourly_events_of_pair_per_day["to_node_id"] = sink_node

            hourly_events_of_pair_per_day["events"] = daily_traffic_events

        return hourly_events_of_pair_per_day

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

        pair_container = {}

        counter = 0

        for pair in node_pairs:
            source_node = pair[0]
            sink_node = pair[1]

            traffic_events = self.calc_traffic_between_nodes(self.id_node_map[source_node], self.id_node_map[sink_node], 5, 15, 6)
            pair_container[counter] = self.format_traffic_events(traffic_events, source_node, sink_node)
            counter = counter + 1

            traffic_events = self.calc_traffic_between_nodes(self.id_node_map[sink_node], self.id_node_map[source_node], 5, 15, 6)
            pair_container[counter] = self.format_traffic_events(traffic_events, sink_node, source_node)
            counter = counter + 1

        return pair_container

    def calculate_total_energy_savings_for_day(self, day):
        energy_savings_dict = {}
        for _id, node in self.id_node_map.iteritems():
            #print ("Processing node:", str(node_id))
            time_morning = datetime(day.year, day.month, day.day, 6, 0, 0)
            time_evening = datetime(day.year, day.month, day.day, 18, 0, 0)
            cycle_readings = node.cycle_readings
            if cycle_readings is not None and not cycle_readings.empty:
                time_window = cycle_readings[time_morning:time_evening]
                if not time_window.empty:
                    energy_savings_dict[_id] = (43200 - (time_window.iloc[-1] - time_window.iloc[0])) / 432 # in percents
        energy_savings = pd.DataFrame.from_dict(energy_savings_dict, orient='index')
        if not energy_savings.empty:
            if float(energy_savings.mean() <= 100):
                return float(energy_savings.mean())
            else:
                return 100
        return None

    def calculate_hourly_energy_savings_for_day(self, date_obj):
        hourly_savings_dict = {}
        time_morning = datetime(date_obj.year, date_obj.month, date_obj.day, 6, 0, 0)
        time_evening = datetime(date_obj.year, date_obj.month, date_obj.day, 18, 0, 0)
        for _id, node in self.id_node_map.iteritems():
            if node.cycle_readings is not None and not node.cycle_readings.empty:
                time_window = node.cycle_readings[time_morning:time_evening]
                print(time_window)
                hourly_index = time_window.reindex(pd.date_range(start=time_morning, end=time_evening, freq='H'))
                hourly_df = time_window.merge(hourly_index, how='outer', left_index=True, right_index=True)
                hourly_df.drop('Value_y', axis=1, inplace=True)
                interpolated_df = hourly_df.interpolate(method='time', limit=12, limit_direction='both')
                hour_values = interpolated_df.loc[pd.date_range(start=time_morning, end=time_evening, freq='H'), 'Value_x']
                if not time_window.empty:
                    hourly_savings = self._get_hourly_savings(hour_values.diff()) # dict(hour: savings_percentage)
                    hourly_savings_dict[_id] = hourly_savings
        energy_savings = pd.DataFrame.from_dict(hourly_savings_dict).mean(axis=1)
        if not energy_savings.empty:
                return [int(percentage) for percentage in energy_savings.tolist()]
        return None

    def _get_hourly_savings(self, hourly_cycle_counts):
        # saving = (3600 - diff) / 36
        hourly_savings = {}
        for index, row in hourly_cycle_counts[1:].iteritems():
            hourly_savings[index.to_pydatetime()] = int((3600 - row) / 36)
        return hourly_savings


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
    for row in db.get_nodes_with_location():
        if row.node_id not in node_ids:
            node_ids.add(row.node_id)
            container.id_node_map[row.node_id] = Node(row.node_id, "PIR", row.location)

    container.put_temp_events_to_all_nodes(start_time, end_time)

    pp = pprint.PrettyPrinter(indent=4)
    events_hourly = container.get_hourly_events_for_all_nodes_grouped_by_day()
    #pp.pprint(events_hourly)

    '''
    Fetch unique nodes without locations (for cycle counts)
    '''
    node_energy_ids = set()
    for row in db.get_nodes_without_locations():
        if row.node_id not in node_energy_ids:
            node_energy_ids.add(row.node_id)
            container.id_node_map[row.node_id] = Node(row.node_id, "LAMP")
            container.put_cycle_count_events_to_node(row.node_id, start_time, end_time)

    
    hourly_energy_savings_per_day = {}
    for day in pd.date_range(start_time, end_time):
        savings = container.calculate_hourly_energy_savings_for_day(day.date())
        hourly_energy_savings_per_day[day.date()] = savings

    # Uncomment next line to unleash true power of calculating and printing all traffic at vvt building on neighbour nodes
    traffic_events_hourly = container.get_traffic_on_neighbour_nodes_at_vtt()
    #pp.pprint(traffic_events_hourly)

    Bokeh.visualization.create(container.id_node_map, events_hourly, traffic_events_hourly, hourly_energy_savings_per_day)

if __name__ == "__main__":

    def valid_date(s):
        try:
            start_dt = datetime.strptime(s, "%Y-%m-%d")
            return start_dt
        except ValueError:
            msg = "Not a valid date: '{0}'. Date format should be [YYYY-MM-DD].".format(s)
            raise argparse.ArgumentTypeError(msg)

    def bounds_check(start_dt, end_dt):
        # check that given date has data in the database
        start_bound = datetime.strptime(constants.DB_LOWER_DATE_BOUND, "%Y-%m-%d")
        end_bound = datetime.strptime(constants.DB_UPPER_DATE_BOUND, "%Y-%m-%d")
        if (start_dt > start_bound and end_dt < end_bound):
            return
        else:
            msg = "Time window has to fit in range [{0}, {1}]".format(constants.DB_LOWER_DATE_BOUND, 
                                                                      constants.DB_UPPER_DATE_BOUND)
            raise argparse.ArgumentTypeError(msg)

    parser = argparse.ArgumentParser(description="Analyses and visualizes one week worth of data from LightSense database.\n\
                                                  Database has data for dates 2014-04-23 - 2016-02-16.")
    parser.add_argument("startdate", help="The starting date of analysis in format [YYYY-MM-DD].", type=valid_date)
    args = parser.parse_args()
    start = args.startdate
    end = start + timedelta(days=7)
    bounds_check(start, end)
    #start = datetime(2016, 1, 25)
    #end = datetime(2016, 1, 31)
    main(start, end)
