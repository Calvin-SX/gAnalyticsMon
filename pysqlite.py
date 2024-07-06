import sqlite3
import os
import json
import random
from datetime import datetime
from datetime import timedelta

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
    READ_NUM_CITIES = "SELECT COUNT(DISTINCT country) FROM record;"
    # TOTAL is not used
    CREATE_TOTAL_TABLE = "CREATE TABLE IF NOT EXISTS total (id INTEGER PRIMARY KEY, total INTEGER, date DATETIME);"
    INSERT_TOTAL = "INSERT INTO total(id, total, date) VALUES(NULL, ?, ?);"
    UPDATE_TOTAL = "UPDATE total SET total=?, date=? WHERE id=1;"
    READ_TOTAL = "SELECT total, date FROM total;"
    # blacklist website
    CREATE_BLACKLIST_SITE_TABLE = "CREATE TABLE IF NOT EXISTS bl_webs (id INTEGER PRIMARY KEY, web STRING);"
    BLACKLIST_GET_ALL = "SELECT web FROM bl_webs;"
    INSERT_BLACKLIST = "INSERT INTO bl_webs(id, web) VALUES(NULL, ?);"

    # urls 
    CREATE_URL_TABLE = "CREATE TABLE IF NOT EXISTS urls (id INTEGER PRIMARY KEY, url STRING);"
    URL_GET_ALL = "SELECT url FROM urls;"
    INSERT_URL_TABLE = "INSERT INTO urls(id, url) VALUES(NULL, ?);"

    DB_FILE = "ga_data.db"
    INIT_FILE = "blacklisturl.json"

    def connect(self):
        self.conn = sqlite3.connect(self.DB_FILE)
        if ~os.path.exists(self.DB_FILE):
            self.init_db()

    def init_db(self):
        cursor = self.conn.cursor()
        # create a table
        cursor.execute(self.CREATE_TABLE)
        cursor.execute(self.CREATE_TOTAL_TABLE)
        cursor.execute(self.CREATE_URL_TABLE)
        cursor.execute(self.CREATE_BLACKLIST_SITE_TABLE)

        curtime = str(datetime.now().date())
        cursor.execute(self.INSERT_TOTAL, (0, curtime))

        self.conn.commit()


    def import_init_data(self):
        with open(self.INIT_FILE) as infile:
            data = json.load(infile)
            blacklist = data["blacklist"]
            urls = data["url"]

            for bl in blacklist:
                self.add_bl_web(bl)
            
            for url in urls:
                self.add_url(url) 

    # Daily count table
    def add_data(self, city, count, date=None):
        cursor = self.conn.cursor()
        if date == None:
            curtime = str(datetime.now().date())
        else:
            curtime = date

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
    
    def read_num_cities(self):
        num_cities = 0
        cursor = self.conn.cursor()
        cursor.execute(self.READ_NUM_CITIES)
        rows = cursor.fetchall()
        for row in rows:
            num_cities = row[0]
        
        return num_cities

    def read_data_for_date(self, date):
        cursor = self.conn.cursor()
        cursor.execute(self.READ_RECORD_FOR_DATE, (date,))
        rows = cursor.fetchall()
        return rows
    
    def read_blacklist_web(self):
        cursor = self.conn.cursor()
        cursor.execute(self.BLACKLIST_GET_ALL)
        rows = cursor.fetchall()
        ret = list(map(lambda x: x[0], rows))
        return ret

    def read_urls(self):
        cursor = self.conn.cursor()
        cursor.execute(self.URL_GET_ALL)
        rows = cursor.fetchall()
        ret = list(map(lambda x: x[0], rows))
        return ret

    def close_conn(self):
        self.conn.close()

    def add_bl_web(self, web):
        cursor = self.conn.cursor()
        cursor.execute(self.INSERT_BLACKLIST, (web,))
        self.conn.commit()

    def add_url(self, url):
        cursor = self.conn.cursor()
        cursor.execute(self.INSERT_URL_TABLE, (url, ))
        self.conn.commit()

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

    @staticmethod
    def simulate_data(num_days, dbname="ga_data.db"):
        pysql = PySqlite()
        pysql.DB_FILE = dbname
        pysql.connect()
        
        today = datetime.now()
        
        for i in range(num_days):
            date = today - timedelta(days = i)
            datestr = f'{date:%Y-%m-%d}'
            bst = random.randint(100, 120)
            chi = random.randint(70, 90)
            ny = random.randint(90, 100)
            pysql.add_data("Boston", bst, datestr)
            pysql.add_data("Chicago", chi, datestr)
            pysql.add_data("New York", ny, datestr)

        pysql.close_conn()

if __name__ == '__main__':
    PySqlite.simulate_data(10)
    # pysql = PySqlite()
    # pysql.DB_FILE = "temp.db"
    # pysql.connect()
    # pysql.import_init_data()

    # bst = 1
    # chi = 2
    # ny = 3

    # date = "2024-05-21"
    # pysql.add_data("Boston", bst, date)
    # pysql.add_data("Chicago", chi, date)
    # pysql.add_data("New York", ny, date)

    # date = "2024-05-22"
    # bst += 10
    # chi += 21
    # ny += 17
    # pysql.add_data("Boston", bst, date)
    # pysql.add_data("Chicago", chi, date)
    # pysql.add_data("New York", ny, date)

    # date = "2024-05-23"
    # bst += 11
    # chi += 26
    # ny += 12
    # pysql.add_data("Boston", bst, date)
    # pysql.add_data("Chicago", chi, date)
    # pysql.add_data("New York", ny, date)

    # date = "2024-05-24"
    # bst += 31
    # chi += 20
    # ny += 19
    # pysql.add_data("Boston", bst, date)
    # pysql.add_data("Chicago", chi, date)
    # pysql.add_data("New York", ny, date)

    # date = "2024-05-25"
    # bst += 21
    # chi += 16
    # ny += 22
    # pysql.add_data("Boston", bst, date)
    # pysql.add_data("Chicago", chi, date)
    # pysql.add_data("New York", ny, date)

    # date = "2024-05-26"
    # bst += 77
    # chi += 22
    # ny += 18
    # pysql.add_data("Boston", bst, date)
    # pysql.add_data("Chicago", chi, date)
    # pysql.add_data("New York", ny, date)


    # date = "2024-05-27"
    # bst += 8
    # chi += 6
    # ny += 2
    # pysql.add_data("Boston", bst, date)
    # pysql.add_data("Chicago", chi, date)
    # pysql.add_data("New York", ny, date)

    # rows = pysql.read_all_data()
    # print(rows)

    # sum = pysql.read_daily_sum()
    # print(sum)

    # date = str(datetime.now().date())
    # ret = pysql.read_data_for_date(date)
    # print(ret)
    # blacklist_webs = pysql.read_blacklist_web()
    # print(blacklist_webs)
    # urls = pysql.read_urls()
    # print(urls)