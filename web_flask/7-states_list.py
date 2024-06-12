#!/usr/bin/python3
"""Starts a Flask web application"""

from flask import Flask, render_template
from models import storage
from models.state import State
import os
from sqlalchemy import create_engine

app = Flask(__name__)

# Path to the SQL file
sql_file = '7-states_list.sql'

# Read the SQL file
with open(sql_file, 'r') as file:
    sql_script = file.read()

# Create an engine
engine = create_engine('mysql+mysqldb://hbnb_dev:hbnb_dev_pwd@localhost/hbnb_dev_db')

# Execute the SQL script
with engine.connect() as connection:
    connection.execute(sql_script)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """Displays a list of states"""
    states = storage.all(State).values()
    states = sorted(states, key=lambda state: state.name)
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
