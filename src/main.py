from __future__ import print_function

import pandas as pd
import numpy as np

from dbconfig import DB_CONFIG
from db_api import LightSenseDatabase


class Node(object):

    def __init__(self, location, data=None):
        self.pos_x = location["x"]
        self.pos_y = location["y"]
        self.temp_readings = None
        self.humidity_readings = None
        self.cycle_readings = None
        self.voltage_reading = None
        self.all_readings = pd.DataFrame(data, index=['Timestamp'], columns=["Temperature", "Humidity", "Cycle count", "Voltage"])


def main():
    db = LightSenseDatabase(DB_CONFIG)
    nodes = {}
    node_ids = set()
    for row in db.get_nodes():
        if row.node_id not in node_ids:
            node_ids.add(row.node_id)
            nodes[row.node_id] = Node(row.location)

    for node_id in node_ids:
        temperature_readings = db.get_node_temperatures_by_node_id(node_id)
        nodes[node_id].temp_readings = pd.DataFrame.from_records(temperature_readings, index=['Timestamp'], exclude=['Measurement'])
        print("\n" + str(node_id))
        print(nodes[node_id].temp_readings.tail())


if __name__ == "__main__":
    main()
