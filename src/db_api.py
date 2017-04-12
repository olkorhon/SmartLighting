from __future__ import print_function
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, Integer, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sys import exit

from dbconfig import DB_CONFIG

# Tables
from datatype import DataType

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

    def get_datatypes(self):
        return self.session.query(DataType)

def main():
    db = LightSenseDatabase(DB_CONFIG)
    records = db.get_datatypes()
    for record in records:
        print(record.description)

if __name__ == "__main__":
    main()
