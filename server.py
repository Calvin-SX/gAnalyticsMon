from flask import Flask
from flask import send_from_directory
import pysqlite
import checkipaddr
from datetime import datetime

app = Flask(__name__)
pysql = None

@app.route('/about')
def onAbout():
    return 'Google Analytics Monitor'

@app.route('/ipaddress/<ip>')
def onCheckIPAddr(ip):
    ret = {
        "ip": ip,
        "badIp": False
    }
    pysql.connect()
    blwebs = pysql.read_blacklist_web()
    pysql.close_conn()
    cia = checkipaddr.CheckIpAddr()
    for web in blwebs:
        bInList = cia.checkIPinBlackList(ip, web)
        if bInList:
            ret['badIp'] = True
            return ret, 200

    return ret, 200

@app.route('/blacklistwebs')
def onBlacklistWebs():
    pysql.connect()
    blwebs = pysql.read_blacklist_web()
    pysql.close_conn()
    return blwebs, 200

@app.route('/urls')
def onUrls():
    pysql.connect()
    urls = pysql.read_urls()
    pysql.close_conn()
    return urls, 200

@app.route('/daily')
def onDaily():
    date = str(datetime.now().date())
    pysql.connect()
    ret = pysql.read_data_for_date(date)
    pysql.close_conn()

    return ret, 200

@app.route('/dailysum')
def onDailySum():
    ret = {
        "dailysum": []
    }
    pysql.connect()
    ret['dailysum'] = pysql.read_daily_sum()
    pysql.close_conn()

    return ret, 200

# static content
@app.route('/views/<path:path>')
def onView(path):
    print("Called with " + path)
    return send_from_directory('views', path)
if __name__ == '__main__':
    # init database
    pysql = pysqlite.PySqlite()
    # need to run only once
    #pysql.connect()
    #pysql.import_init_data()
    #pysql.close_conn()

    app.run()
    