import sqlite3

DB_FILE = 'tickets.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_no TEXT PRIMARY KEY,
            name TEXT,
            event TEXT,
            email TEXT,
            date TEXT,
            time TEXT,
            venue TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_ticket(ticket):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO tickets (ticket_no, name, event, email, date, time, venue)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (ticket['ticket_no'], ticket['name'], ticket['event'], ticket['email'], ticket['date'], ticket['time'], ticket['venue']))
    conn.commit()
    conn.close()

def get_ticket(ticket_no):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT * FROM tickets WHERE ticket_no=?', (ticket_no,))
    row = c.fetchone()
    conn.close()
    if row:
        return {
            'ticket_no': row[0],
            'name': row[1],
            'event': row[2],
            'email': row[3],
            'date': row[4],
            'time': row[5],
            'venue': row[6],
        }
    return None
