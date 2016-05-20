from flask import Flask, jsonify, request, redirect
import psycopg2
from prettytable import PrettyTable

app = Flask(__name__)
con = None

class User:

	longitudes = []
	latitudes = []

	def __init__(self, latVar, longVar, radius, score, email):
		self.latVar = 0
		self.longVar = 0
		self.radius = 0
		self.score = 0
		self.email = email
		self.longitudes = []
		self.latitudes = []
		print ("new user created")

	def updateScore(latitude, longitude):
		self.longitudes.append(longitude)
		self.latitudes.append(latitude)
		self.calculate()

	def calculate():
		self.latVar = self.latVar + 5
		self.longVar = self.longVar  + 9
		self.radius = self.radius + 3
		self.score = self.latVar + self. longVar
		return (latVar, longVar, radius, score)


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

def retrieveUser(userid):

	con = createDBConnection()

	print("Created Connection")
	cur = con.cursor()
	cur.execute("SELECT * FROM users WHERE \"userid\" = %s", (userid,))
	results = cur.fetchone()
	print("Fetched")
	retrievedUser = User(results[1], results[2], results[3], results[4], results[5])
	print(results[1], results[2], results[3], results[4], results[5])
	print(retrievedUser.score)
	return retrievedUser


@app.route('/create/', methods=['POST'])
def createUser():
	if request.method == 'POST':

		email = request.form['email']
		newUser = User(email)
		addUserToDB(newUser)

		return "Created"

	else:
		return redirect('/')

@app.route('/score/', methods=['POST'])
def getScore():

	userid = request.form['userid']
	userScore = retrieveUser(userid)
	return userScore.score


@app.route('/')
def index():
	return "/create  -  creates a new user \n /score  -  get the score of the user"



if __name__ == '__main__':
	app.debug = True
	app.run()
