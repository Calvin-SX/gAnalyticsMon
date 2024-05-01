# Google Analytics Monitor
This is a fun project using python.

# python
## python venv
venv is a virtual environemnt for running python. New python packages are installed into the venv, and it wouldn't pollute the system environment.
### start a venv
The following command starts a new venv called analytics-quickstart, which is in a folder called analytics-quickstart.
```bash
python3 -m venv analytics-quickstart
```
### Enter venv
```bash
source analytics-quickstart/bin/activate
```
### install 
```bash
pip install -update google-api-python-client
```

### use venv in pycharm
Open the "analytics-quickstart" folder from pycharm, it will recognize the venv automatically. But it might not be able to recognize the installed packages. Go to "Pycharm->Settings->Project Interpreter", install the following packages:
* httplib2
* oauth2client
* google-api-python-client


## Reference
[Google Analytics API](https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/installed-py)
