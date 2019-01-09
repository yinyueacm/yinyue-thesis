import MySQLdb
import random
import string
from datetime import datetime


def pswd_generator(size=6, chars=string.ascii_lowercase + string.digits):
    random.seed(datetime.now())
    return ''.join(random.choice(chars) for _ in range(size))

db = MySQLdb.connect("localhost","djdb","django","djdb" )

cursor = db.cursor()

#cursor.execute("SELECT * from reuse_category")

#data = cursor.fetchall()
#for line in data:
#    print line

for i in range(1, 100):
    try:
        ran_pswd = pswd_generator()
        print ran_pswd
        cursor.execute("""INSERT INTO reuse_pswd_table VALUES (%s, %s)""", (i, ran_pswd))
        db.commit()
    except:
        print "what?"
        db.rollback()
    
db.close()
