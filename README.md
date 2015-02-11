# Yago
Home of the Yago API. The API is written in Django and utilizes the [Django Rest Framework] (http://www.django-rest-framework.org/). Follow the instruction 
below to setup a local copy of the Yago API. Alternatively you can access the live server docs here. <TODO: Insert link>

##Requirements
Before you can install you will need the following:

Python package installer - [pip](https://pypi.python.org/pypi/pip/)

Environment management - [virtualenv] (https://virtualenv.pypa.io/en/latest/) and [virtualenvwrapper] (http://virtualenvwrapper.readthedocs.org/en/latest/install.html)

Database - [PostgreSQL] (http://www.postgresql.org/download/) 

(optional) Database Management Tool - [PgAdmin] (http://www.pgadmin.org/download/)

##Setup/Installation 
NOTE: While non of this is platform specific, the following walkthrough is geared towards OSX. I am sure it can be adjusted to work
with Windows, but I don't have experience with this.

Create a new virtualenv for the project (bash terminal)

```
$ export WORKON_HOME=~/Envs
$ mkdir -p $WORKON_HOME
$ source /usr/local/bin/virtualenvwrapper.sh
$ mkvirtualenv yago_env
```

Checkout the latest code from this repository.

Navigate to the top level folder, you should see a file ```requirements.txt```

Make sure you are in the virtualenv you created earlier with ```workon <env_name>```

Install all project dependencies with ```pip install -r requirements.txt```

Set required project environment variables by editing the following two files in ```~/WORKON_HOME/<env_name>/bin/```:

postactivate - Sets up environment variables when you activate the virtualenv

``` bash
#!/bin/bash
# This hook is run after this virtualenv is activated.
export DJANGO_DEBUG=True
export DB_NAME=<whatever you intend to call your local db>
export DB_USER=<db username, if on OSX, this defaults to your admin username>
export DB_PASSWORD=<whatever you want>
export DJANGO_SECRET_KEY=<this isnt important locally, just make a few random characters>
export USE_AWS=False
export HEROKU=False
```

predeactivate - Removes environment variables previously setup

``` bash
#!/bin/bash
# This hook is run before this virtualenv is deactivated.
unset DJANGO_DEBUG
unset DB_NAME
unset DB_USER
unset DB_PASSWORD
unset DJANGO_SECRET_KEY
unset USE_AWS
unset HEROKU
```

Test to see if it is working
```
$ workon <env_name>
$ echo $DB_USER
williamkelly
```

Create a new postgres database and make sure your postgres server is running. This database will be your own local copy so you can call 
it whatever you want. This is much easier with a DB management tool like PgAdmin.

Generate project database tables with ```python manage.py syncdb``` (manage.py found in top level project folder)

Run any data migrations with ```python manage.py migrate```

Create admin user for yourself with ```python manage.py createsuperuser``` and follow the prompts

Now you should be able to launch the server with ```python manage.py runserver```

If everything is working, you should be able to navigate to http://localhost:8000/users/ and see the API docs.

NOTE: You will have to login (top right) with username you created earlier in order to see any data.
