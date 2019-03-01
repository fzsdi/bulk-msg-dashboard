# Bulk Messaging Dashboard
sending group messages to group mobile numbers (MCI) in parallel

Build and Install bulk-dashboard

Download the bulk_dashboard-1.0.0-py3-none-any.whl that I've been uploaded into this repo.
To deploy bulk dashboard elsewhere, you build a wheel format file, with the .whl extension. Make sure the wheel library is installed first:
```bash
pip install wheel
pip install bulk-dashboard-1.0.0-py3-none-any.whl
```
Pip will install your project along with its dependencies.

Since this is a different machine, you need to run init-db to create the database and the instance folder. So at first you need to active your virtual environment.
```bash
. venv/bin/activate
export FLASK_APP=bulkDashboard
flask init-db
```
if you haven't installed virtual environment or flask yet you can learn it to the following link: http://flask.pocoo.org/docs/1.0/installation/#virtual-environments

Then put the database that I've uploaded into this repo in bulkdashboard-instance.
You can run the application with these commands:
```bash
. venv/bin/activate
export FLASK_APP=bulkDashboard
export FLASK_ENV=development
flask run
```
Now you can login to the dashboard with these details:
username: taranom
password: hellogram
Bulk form is for sending 100 messages to 100 mobile numbers in each requests. First MSG and Third MSG are constant.
single form is for sending a special message to 100 mobile numbers in each requests.
