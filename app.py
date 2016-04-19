from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

con = None

def createDBConnection():

	try:
		con = psycopg2.connect(database='gentryar', user='gentryar', password='ginger whale station')

	except psycopg2.DatabaseError:
	    print ("Connection Error")
	    sys.exit(1)

	finally:
		return con

@app.route('/add/<name>')
def addUser(name):

	email = name+"@magswitch.com.au"

	con = createDBConnection()

	try:
		cur = con.cursor()
		cur.execute("INSERT INTO users VALUES(%s,%s)", (name, email))
		con.commit()
		print ("Added '" + name + " to the database")

	except psycopg2.DatabaseError:

		if con:
			con.rollback

		print ("Error adding a user")
		sys.exit(1)

	finally:
		if con:
			con.close
		return name + " is now in Andrews database..."
 

@app.route('/')
def index():
	return 'This is Andrew\'s server. If you see this message, it means that it\'s working.'


@app.route('/data')
def names():
	
	con = createDBConnection()

	try:
		cur = con.cursor()
		cur.execute("SELECT * FROM users")
		data = []
		for record in cur:
			data.append(record[0])		
		return '<h4><br>'.join(data)
		 

	except psycopg2.DatabaseError:

		if con:
			con.rollback

		print("Error displaying the users")
		sys.exit(1)



if __name__ == '__main__':
	app.run()
