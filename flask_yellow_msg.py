
# from base64 import b64encode
# from hashlib import blake2b
# import random
# import re

from math import floor
from flask import Flask,request,redirect
import json
import pdb
from sqlite3 import OperationalError
import sqlite3, string

app = Flask(__name__)
import requests



# default route
@app.route('/')
def hello():
    return """Hello ,
	    World!"""


host = 'http://localhost:5000/'



# Setting up Table Configurations before starting app
def table_check():

	create_table = """
		CREATE TABLE WEB_URL(
		ID INT PRIMARY KEY     AUTOINCREMENT,
	 	URL  TEXT    NOT NULL
		);
		"""
	with sqlite3.connect('event_database.db') as conn:
		cursor = conn.cursor()
		try:
			cursor.execute(create_table)
		except OperationalError:
			pass



# Url Ecoder and Retriever Methods
def toBase62(num, b = 62):
    pdb.set_trace()
    if b <= 0 or b > 62:
        return 0
    import string
    base = string.digits + string.ascii_lowercase + string.ascii_uppercase
    r = num % b
    res = base[r];
    q = floor(num / b)
    while q:
        r = q % b
        q = floor(q / b)
        res = base[int(r)] + res
    return res

def toBase10(num, b = 62):
    base = string.digits + string.ascii_lowercase + string.ascii_uppercase
    limit = len(num)
    res = 0
    for i in range(limit):
        res = b * res + base.find(num[i])
    return res



# Link to shorten the url
@app.route('/shorten_url/')
def url_short():
	#table_check()

	# Getting the URL and inserting it into a Table and making encrypted shortened
	# URL based on its Index Values i.e ID

	original_url = request.args.get('url')
	with sqlite3.connect('event_database.db') as conn:
		cursor = conn.cursor()
		insert_row = """
			INSERT INTO WEB_URL (URL)
			VALUES ('%s')
			"""%(original_url)
		result_cursor = cursor.execute(insert_row)
		encoded_string = toBase62(result_cursor.lastrowid)
	return host + encoded_string

# Link to Retdirect to reach to the actual url from the shortened url
@app.route('/<short_url>')
def redirect_short_url(short_url):

	#Decoding or Retrieving Back the original URL by getting back the actual ID from encrypted one
	# and mapping it with the available Actual URL
	# ANd Finally redirecting to the Original URL
    decoded_string = toBase10(short_url)
    redirect_url = 'http://localhost:5000'
    with sqlite3.connect('event_database.db') as conn:
        cursor = conn.cursor()
        select_row = """
                SELECT URL FROM WEB_URL
                    WHERE ID=%s
                """%(decoded_string)
        result_cursor = cursor.execute(select_row)
        try:
            redirect_url = result_cursor.fetchone()[0]
        except Exception as e:
            print(e)
    return redirect(redirect_url)

if __name__ == '__main__':
    table_check()
    app.run(debug=True)