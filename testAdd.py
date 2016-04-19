import psycopg2
import sys


con = None

try:
     
    con = psycopg2.connect("dbname='gentryar' user='gentryar' password='ginger whale station'") 
    con.autocommit = True
    cur = con.cursor()
  
    cur.execute("INSERT INTO users (username, email, distributor) VALUES ('andrew', 'andy@gentry', TRUE)") 
    print "Added User"

except psycopg2.DatabaseError, e:
    
    if con:
        con.rollback()
    
    print 'Error %s' % e    
    sys.exit(1)
    
    
finally:
    
    if con:
        con.close()
