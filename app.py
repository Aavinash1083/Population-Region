import os
from flask import Flask, render_template, make_response, request
import sys
import logging
from time import time
import json
from random import random
import sqlite3
from sqlite3 import Error
import zenv

database = zenv.DB_LOCATION


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def select_by_Name(conn, name):
    """
    Query all rows in the MOVIE table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    name_obj = {
        'name': name
    }
    cur.execute("SELECT * FROM POPULATIONS WHERE CountryName = :name", name_obj)

    rows = cur.fetchall()
    return rows

    # print('rows count : '+str(len(rows)))

   # if(len(rows) <= 0):
    #    print('No Data available')

    # for row in rows:
    #   print(row)


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'XYZ')

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data/<name>', methods=["GET", "POST"])
def data(name):

    # Data Format
    # [TIME, Temperature, Humidity]

    #Temperature = random() * 100
    #Humidity = random() * 55

    #data = [time() * 1000, Temperature, Humidity]

    conn = create_connection(database)
    with conn:
        rows = select_by_Name(conn, name)

    response = make_response(json.dumps(rows))
    response.content_type = 'application/json'
    print(response.data)
    return response


@app.route('/highchart', methods=["GET", "POST"])
def main():
    if request.method == 'POST':
        name = request.form['name']
    return render_template('graph.html', name=name)
