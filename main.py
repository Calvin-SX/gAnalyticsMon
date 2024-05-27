# This is the main module
import os
import googleData
import pysqlite
import utils

# Read data from GA4
def read_cur_data():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./credentials.json"
    curData = googleData.sample_run_report()
    print(curData)
    return curData

def store_data(sqlDB, cur_data):
    for city_data in cur_data:
        sqlDB.add_data(city_data['city'], city_data['count'])

def main():
    
    # write data only once a day. Check if it is done already
    is_data_stored = utils.is_data_stored()

    sqlDB = pysqlite.PySqlite()
    sqlDB.connect()
    if not is_data_stored:
        # Step 1: Read data from GA4
        curData = read_cur_data()

        # Step 2: connect to Database and write data
        store_data(sqlDB, curData)

    # Step 3: read historical data
    acc_counts = sqlDB.read_daily_sum()
    daily_count = utils.get_delta(acc_counts)
    print(daily_count)
    
if __name__ == '__main__':
    main()