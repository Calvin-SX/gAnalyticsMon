from flask import Flask
from flask import send_from_directory

app = Flask(__name__)

@app.route('/about')
def onAbout():
    return 'Google Analytics Monitor'

@app.route('/ipaddress/<ip>')
def onCheckIPAddr(ip):
    return "Good ip: " + ip


# static content
@app.route('/views/<path:path>')
def onView(path):
    print("Called with " + path)
    return send_from_directory('views', path)
if __name__ == '__main__':
    app.run()