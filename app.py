from flask import Flask, jsonify, request, redirect
import psycopg2
from prettytable import PrettyTable

app = Flask(__name__)
con = None

class User:

	locations = []

	def __init__(self,email,locations = None):
		if locations is None:
			self.latVar = 0
			self.longVar = 0
			self.radius = 0
			self.score = 0
			self.email = email
			print ("New user created")

		else:
			self.locations = locations
			self.email = email
			self.calculate()
			print("User Restored")
		

	def calculate(self):
		self.latVar = 4
		self.longVar = 5
		self.radius = 6
		self.score = (self.latVar + self.longVar)
		return (self.latVar, self.longVar, self.radius, self.score)


class Location:

	longitude = 0
	latitude = 0
	time = 0

	def __init__(self, longitude, latitude, time):
		self.longitude = longitude
		self.latitude = latitude
		self.time = time


def updateScore(user, locations):
	
	for location in locations:
		user.locations.append(location)
	user.calculate()


def createLocationsFromData(rawData): # need to find way to split correctly.

	createdLocations = []
	for x,y,z in zip(rawData[0],rawData[1],rawData[2]):
		newLocation = Location(x,y,z)
		createdLocations.append(newLocation)

	return createdLocations


def splitDataFromLocations(locations):

	longitudes = []
	latitudes = []
	times = []
	for item in locations:
		longitudes.append(item.longitude)
		latitudes.append(item.latitude)
		times.append(item.time)
	return (longitudes, latitudes, times)

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
		cur.execute("INSERT INTO users VALUES(%s,%s)", (nextUserID, newUser.email))
		newLocations = splitDataFromLocations(newUser.locations)
		cur.execute("INSERT INTO locations VALUES(%s,%s,%s,%s)", (nextUserID, newLocations[0],newLocations[1],newLocations[2])
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

def retrieveUserByID(userid):

	con = createDBConnection()

	print("Created Connection")
	cur = con.cursor()
	cur.execute("SELECT * FROM users WHERE \"userid\" = %s", (userid,))
	results = cur.fetchone()
	print("Fetched from users")
	email = results[1]
	cur.execute("SELECT * FROM locations WHERE \"userid\" = %s", (userid,))
	results = cur.fetchone()
	print("Fetched from locations")
	locations = createLocationsFromData(results[1],results[2],results[3])
	retrievedUser = User(email,locations)

	return retrievedUser

def createUserWithEmail(email):

	newUser = User(email)
	addUserToDB(newUser)

	return newUser

def createUserWithLocations(email, locations):
	newUser = User(email,locations)
	addUserToDB(newUser)
	return newUser

@app.route('/create/', methods=['POST'])
def createUser():
	if request.method == 'POST':
		email = request.form['email']

		lats = (1,2,3)
		longs = (4,5,6)
		times = (7,8,9)
		createUserWithLocations('testemail', [longs,lats,times])

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
