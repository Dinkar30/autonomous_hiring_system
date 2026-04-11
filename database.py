import sqlite3

def init_db():
    connection = sqlite3.connect('recruit.db')
    c = connection.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS candidates
                 (email TEXT PRIMARY KEY, 
                  name TEXT, 
                  score INTEGER, 
                  tier TEXT, 
                  last_msg_id TEXT, 
                  round INTEGER, 
                  status TEXT)''')
    
    connection.commit()
    connection.close()
    
def update_candidate(email,name,score,tier,status="NEW"):
    connection = sqlite3.connect('recruit.db')
    c = connection.cursor()

    c.execute('''INSERT OR REPLACE INTO candidates (email,name,score,tier,status) 
              VALUES (?,?,?,?,?)''' (email,name,score,tier,status))
    connection.commit()
    connection.close()
    
