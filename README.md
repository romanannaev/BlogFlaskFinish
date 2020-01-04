Quick Start

First Steps
# using python 3.6.9
# (PostgreSQL) 12.1 

$ pip install virtualenv
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt

Set up Migrations
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade

Run
# the app
$ python app.py or
$ python manage.py runserver