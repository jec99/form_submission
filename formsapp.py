# the current workflow:
#	1. When soemone inputs their email, we send them an email with a link to the
#		signup form. This has fields First Name, Last Name, email, Card Number,
#		Card Verification Code, and Card Expiration: {month, year}
#	2. Thinkful receives an email notifying them of a new student
#	3. The student's Zoho profile is changed, specifically Status is set to
#		"Closed - CC on file"
#	4. They are sent an email with a link to the enrollment form, which has fields
#		First Name, Last Name, When they would like to start the class,
#		Mailing Address {main, city, state, zip}, Country, Email Address, Time Zone,
#		Mentoring Sessions [], Comments About Availability, Current Skills, Employment,
#		Career Goals, Link to Projects, Other, Refer a Friend Email
#	5. This information is propagated to a Google Drive spreadsheet.

from flask import Flask, render_template, Response, request, jsonify, make_response, flash
import time, datetime
from mfabrik.zoho.crm import CRM
from tf_utils import env, get_crm, get_stripe
from tf_utils.beautiful_soupcon_tf_zoho import ThinkfulPerson
# from customerio import CustomerIO
# from google_spreadsheet.api import SpreadsheetAPI

app = Flask(__name__)

stripe = get_stripe()

# only run this once
# stripe.Plan.create(amount=0, interval='month', name='Zero Plan', currency='usd', id='zero')

# NECESSARY FUNCTIONS:
# 1. Send initial information to CRM upon submission of signup form
# 2. Submit credit card information to Stripe
# 3. Send email to all@thinkful with some text
# 4. Process enrollment form, propagate that information to the GDocs spreadsheet

@app.route('/api/signup', methods=['GET', 'POST'])
def signup():
	now = datetime.datetime.now()

	"""
	tp = ThinkfulPerson()
	tp.is_lead = False
	tp.is_potential = True
	tp.email = request.args['email']
	tp.funnel_stage = "Closed - CC on file"
	tp.contect_owner = "nora@thinkful.com"
	tp.phone = None
	tp.lead_source = None
	tp.first_name = request.args['firstname']
	tp.last_name = request.args['lastname']
	tp.signup_date = '/'.join(now.day, now.month, now.year)
	tp.note_title = 'Signup form with CC'
	tp.notes = "User-agent: %(user_agent)s Referrer: %(referrer)s" % (
		dict(user_agent=user_agent, referrer=referrer))

	crm = get_crm()
	crm.open()
	tp.send2zoho(crm)
	crm.close()
	"""

	token = request.args['tken']
	
	# tests; does nothing important
	# with open('tokenz.txt', 'w') as f:
	# 	f.write(str(token))

	customer = stripe.Customer.create(card=token, plan='zero', email=request.args['eml'],
		name=request.args['fname'] + request.args['lname'])

	# TO DO
	# 1. Insert the applicant into the database
	# 2. Do something with the customer id?

	return "yup, we won"

@app.route('/api/enroll', methods=['GET', 'POST'])
def enroll():
	ag = request.args
	USERNAME = 'julien@thinkful.com'
	PASSWORD = '84r71m43u5'
	SOURCE = 'thinkful.com'
	api = SpreadsheetAPI(env(GOOGLE_USERNAME), env(GOOGLE_PASSWORD), env(GOOGLE_SOURCE))
	spreadsheets = api.list_spreadsheets()
	sheet = api.get_worksheet(spreadsheets[0][1], 'od6')
	rows = sheet.get_rows()
	row = dict(zip(map(lambda x: ag[x][0], ag), ag))
	sheet.insert_row(row)

	cio = get_cio()
	# TO DO
	# 1. send the inital welcome email
	# 2. send an email to thinkful

@app.route('/')
def page():
	return make_response(open('index.html').read())

if __name__ == '__main__':
	app.run()
