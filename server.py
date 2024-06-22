from flask import Flask
from flask import send_from_directory
import pysqlite

app = Flask(__name__)
pysql = None

@app.route('/about')
def onAbout():
    return 'Google Analytics Monitor'

@app.route('/ipaddress/<ip>')
def onCheckIPAddr(ip):
    return "Good ip: " + ip

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

# static content
@app.route('/views/<path:path>')
def onView(path):
    print("Called with " + path)
    return send_from_directory('views', path)
if __name__ == '__main__':
    # init database
    pysql = pysqlite.PySqlite()
    pysql.connect()
    # need to run only once
    #pysql.import_init_data()
    #pysql.close_conn()

    app.run()
    