from flask import Flask, jsonify, request, redirect
import psycopg2
from prettytable import PrettyTable

app = Flask(__name__)

class User:

	def __init__(self, email):
		self.latVar = 0
		self.longVar = 0
		self.radius = 0
		self.score = 0
		self.email = email
		print ("new user created")

con = None
def createDBConnection():

	try:
		con = psycopg2.connect(database='gentryar', user='gentryar', password='ginger whale station')

	except psycopg2.DatabaseError as e:
		print "Connection Error." + e
		sys.exit(1)

	finally:
		return con

def addUserToDB(newUser):
	con = createDBConnection()

	try:
		cur = con.cursor()
		cur.execute("SELECT userID FROM users ORDER BY userID DESC LIMIT 1")
		lastUserID = cur.fetchone()
		nextUserID = lastUserID[0] + 1
		cur.execute("INSERT INTO users VALUES(%s,%s,%s,%s,%s,%s)", (nextUserID, newUser.latVar, newUser.longVar, newUser.radius, newUser.score, newUser.email))
		con.commit()
		print ("Added " + nextUserID + " to the database.")

	except psycopg2.DatabaseError as e:

		print "Error adding a user." + e

		if con:
			con.rollback
		sys.exit(1)

	finally:
		if con:
			con.close

		return


@app.route('/create/', methods=['POST'])
def createUser():
	if request.method == 'POST':

		name = request.form['username']
		psswrd = request.form['psswrd']
		email = request.form['email']
		distributor = request.form['distributor']
		salesperson = request.form['salesperson']
		print "processed form"

		newUser = User(name,psswrd,email,distributor,salesperson)
		addUserToDB(newUser)

		return redirect('/data')

	else:
		return redirect('/')

@app.route('/score/', methods=['POST'])
def getScore():

	userid = request.form['userid']
	con = createDBConnection()

	try:
		cur = con.cursor()
		cur.execute("SELECT * FROM users WHERE \"userid\" = %s", (userid,))
		t = PrettyTable(['|______.Name.______|', '|______.Password.______|', '|________.Email._________|', '|___.Distributor.___|', '|___.Salesperson.__|'])
		for record in cur:
			t.add_row([record[0],record[1],record[2],record[3],record[4]])
		return t.get_html_string()

	except psycopg2.DatabaseError as e:

		if con:
			con.rollback

		print "Error displaying the users." + e
		sys.exit(1)
		

@app.route('/')
def index():
	return "/create  -  creates a new user \n /score  -  get the score of the user"


@app.route('/data')
def names():
	
	con = createDBConnection()

	try:
		cur = con.cursor()
		cur.execute("SELECT * FROM users")
		t = PrettyTable(['|______.Name.______|', '|______.Password.______|', '|________.Email._________|', '|___.Distributor.___|', '|___.Salesperson.__|'])
		for record in cur:
			t.add_row([record[0],record[1],record[2],record[3],record[4]])
		return t.get_html_string()
		 

	except psycopg2.DatabaseError as e:

		if con:
			con.rollback

		print "Error displaying the users." + e
		sys.exit(1)



if __name__ == '__main__':
	app.debug = True
	app.run()
