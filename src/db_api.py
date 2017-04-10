from __future__ import print_function

import psycopg2

import dbconfig

class LightSenseDatabase(object):

    def __init__(self, user, pw, host, port, dbname):
        self.user = user
        self.pw = pw
        self.host = host
        self.port = port
        self.dbname = dbname

        self.conn_string = "user={} password={} host={} port={} dbname={}"
        self.conn_string = self.conn_string.format(self.user, self.pw, self.host, self.port, self.dbname)
        self.conn = self.connect_to_db(self.conn_string)


    def connect_to_db(self, connection_string):
        try:
            conn = psycopg2.connect(connection_string)
        except:
            print("Cannot connect to the database, check that the settings are OK:\n", connection_string)
        return conn

    def get_datatypes(self, conn):
        result = []
        # http://initd.org/psycopg/docs/usage.html#with-statement
        with conn:  # Not quite sure if this is needed here...
            with conn.cursor() as cur:
                sql = 'SELECT * FROM "DataType" ORDER BY "Id";'
                cur.execute(sql)
                result = cur.fetchall()
        return result


def main():
    db = LightSenseDatabase(dbconfig.USER, dbconfig.PASSW, dbconfig.HOST, dbconfig.PORT, dbconfig.DBNAME)
    records = db.get_datatypes(db.conn)
    print(records)

if __name__ == "__main__":
    main()
