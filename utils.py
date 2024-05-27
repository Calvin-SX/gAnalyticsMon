from datetime import datetime
import pysqlite

def is_data_stored():
    # check if data for today already stored
    ret = False
    sqlDB = pysqlite.PySqlite()
    today = datetime.today().date()
    sqlDB.connect()
    records = sqlDB.read_data_for_date(today)
    sqlDB.close_conn()
    return len(records) > 0
    
def get_delta(records):
    ret = []
    if len(records) >= 2:
        base = records[0][1]
        for i in range(1, len(records)):
            delta = records[i][1] - base
            if delta < 0:
                delta = 0
            ret.append(delta)
            base = records[i][1]

    return ret


if __name__ == '__main__':
    l1  = [("a", 1)]
    ret = get_delta(l1)
    print(ret)
    l2 = [("a", 1),("a", 2),("a", 3),("a", 4),("a", 5),("a", 6)]
    ret = get_delta(l2)
    print(ret)