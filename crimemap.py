import json
import string
import datetime

from flask import Flask
from flask import request
from flask import render_template

# ExLib
import dateparser

import dbconfig


if dbconfig.IN_DEVELOPMENT:
	from mockdbhelper import MockDBHelper as DBHelper
else:
	from dbhelper import DBHelper



app = Flask(__name__)
DB = DBHelper()
categories = ['mugging', 'break-in']


def format_date(userdate):
	date = dateparser.parse(userdate)
	try:
		return datetime.datetime.strftime(date, "%Y-%m-%d")
	except TypeError:
		return None

def sanitize_string(userinput):
	whitelist = string.letters + string.digits + " !?$.,;:-()&"
	return filter(lambda x: x in whitelist, userinput)


@app.route('/')
def home( error_message=None ):
	crimes = DB.get_all_crimes()
	crimes = json.dumps(crimes)
	return render_template(
		'home.html', 
		crimes=crimes, 
		categories=categories, error_message=error_message)


@app.route("/submitcrime", methods=["POST"])
def submitcrime():
	category = request.form.get("category")
	# validate that a valid category was selected/passed
	if category not in categories:
		return home()

	date = format_date(request.form.get("date"))
	if not date:
		return home("Invalid date. Please use yyyy-mm-dd format")

	try:
		latitude = float(request.form.get("latitude"))
		longitude = float(request.form.get("longitude"))
	except ValueError as err:
		print(err)
		return home()
	
	description = request.form.get("description")
	description = sanitize_string(description)

	DB.add_crime(category, date, latitude, longitude, description)
	return home()


if __name__ == '__main__':
	app.run(port=5000, debug=True)