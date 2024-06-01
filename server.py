from flask import Flask

app = Flask(__name__)

@app.route('/about')
def onAbout():
    return 'This is a flask server'

if __name__ == '__main__':
    app.run()