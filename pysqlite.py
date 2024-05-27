import sqlite3
import os
from datetime import datetime

# This is the database access file

class PySqlite:
    # Database connection
    conn = None
    
    # record table
    CREATE_TABLE = "CREATE TABLE IF NOT EXISTS record (id INTEGER PRIMARY KEY, dailycount INTEGER, country STRING, date DATETIME);"
    INSERT_DAILY_COUNT = "INSERT INTO record(id, dailycount, country, date) VALUES(NULL, ?, ?, ?); "
    READ_DATA = "SELECT * FROM record;"
    READ_DAILY_TOTAL = "SELECT date, SUM(dailycount) as sum FROM record GROUP BY date;"
    READ_RECORD_FOR_DATE = "SELECT * FROM record WHERE date=?;"
    # TOTAL is not used
    CREATE_TOTAL_TABLE = "CREATE TABLE IF NOT EXISTS total (id INTEGER PRIMARY KEY, total INTEGER, date DATETIME);"
    INSERT_TOTAL = "INSERT INTO total(id, total, date) VALUES(NULL, ?, ?);"
    UPDATE_TOTAL = "UPDATE total SET total=?, date=? WHERE id=1;"
    READ_TOTAL = "SELECT total, date FROM total;"

    DB_FILE = "ga_data.db"

    def connect(self):
        self.conn = sqlite3.connect(self.DB_FILE)
        if ~os.path.exists(self.DB_FILE):
            self.init_db()

    def init_db(self):
        cursor = self.conn.cursor()
        # create a table
        cursor.execute(self.CREATE_TABLE)
        cursor.execute(self.CREATE_TOTAL_TABLE)
        curtime = str(datetime.now().date())
        cursor.execute(self.INSERT_TOTAL, (0, curtime))

        self.conn.commit()

    # Daily count table
    def add_data(self, city, count):
        cursor = self.conn.cursor()
        curtime = str(datetime.now().date())

        cursor.execute(self.INSERT_DAILY_COUNT, (count, city, curtime))
        self.conn.commit()

    def read_all_data(self):
        cursor = self.conn.cursor()
        cursor.execute(self.READ_DATA)
        rows = cursor.fetchall()
        return rows
    
    def read_daily_sum(self):
        cursor = self.conn.cursor()
        cursor.execute(self.READ_DAILY_TOTAL)
        rows = cursor.fetchall()
        return rows
    
    def read_data_for_date(self, date):
        cursor = self.conn.cursor()
        cursor.execute(self.READ_RECORD_FOR_DATE, (date,))
        rows = cursor.fetchall()
        return rows
    
    def close_conn(self):
        self.conn.close()

    # TOTAL table
    def set_total(self, total):
        cursor = self.conn.cursor()
        curtime = str(datetime.now().date())
        cursor.execute(self.UPDATE_TOTAL, (total, curtime))
        self.conn.commit()

    def read_total(self):
        cursor = self.conn.cursor()
        cursor.execute(self.READ_TOTAL)
        rows = cursor.fetchall()
        total = 0
        for row in rows:
            total = row[0]
            break
        # there shall be only one
        return total


if __name__ == '__main__':
    pysql = PySqlite()
    pysql.connect()
    
    pysql.add_data("Boston", 1)
    pysql.add_data("Chicago", 2)
    pysql.add_data("New York", 3)
    pysql.add_data("Miami", 4)
    rows = pysql.read_all_data()
    print(rows)

    pysql.set_total(10)
    total = pysql.read_total()
    print(total)

    sum = pysql.read_daily_sum()
    print(sum)

    date = str(datetime.now().date())
    ret = pysql.read_data_for_date(date)
    print(ret)