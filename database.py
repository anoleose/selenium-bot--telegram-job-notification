import sqlite3
from sqlite3 import Error

def create_data_base(name):
	conn = None
	try:
		conn = sqlite3.connect(name)
	except Error as e:
		print(e)
	return conn 
database_name = 'ma_base.db'
connection = create_data_base(database_name)

def create_table(connection):
    cursor = connection.cursor()
    create_task_table = """
	CREATE TABLE IF NOT EXISTS task(
    task_id INTEGER PRIMARY KEY,
    title TEXT,
    link TEXT, 
    price TEXT,
    bid TEXT,
    view TEXT,
    posted TEXT
	);
	"""

    try:
        cursor.execute(create_task_table)
        connection.commit()
        print("table created successful")
    except Error as err:
        print(f"Error: '{err}'")

def create_task(connection, query):
    cursor = connection.cursor()

    sql = """
		INSERT INTO task(task_id, title, link, price, bid, view, posted) 
		VALUES(?, ?, ?, ?, ?, ?, ?)"""
    try:
        cursor.execute(sql, query)
        connection.commit()
        print("created task successful")
    except Error as err:
        print(f"Error: '{err}'")
    return cursor.lastrowid



def get_all_task(connection):
	cursor = connection.cursor()
	sql = """ SELECT * FROM  task """
	try:
		cursor.execute(sql)
		tasks = cursor.fetchall()
	except Error as err:
		print(f"Error: '{err}'")
	return tasks


def get_task(connection, task_id):
	cursor = connection.cursor()
	sql = 'SELECT * FROM task WHERE task_id=?'
	cursor.execute(sql, (task_id,))
	task = cursor.fetchone()
	return task


def update_task(connection, task):
	cursor = connection.cursor()
	sql = """ UPDATE task
	SET title = ? ,
		link  = ?,
		price = ? ,
		bid = ?,
		view = ?,
		posted = ?
	WHERE task_id = ?"""
	try:
		cursor.execute(sql, task)
		connection.commit()
		print("updated successful")
	except Error as err:
		print(f"Error: '{err}'")
	return cursor.lastrowid

	
def delete_task(conn, id):
    sql = 'DELETE FROM task WHERE task_id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()
    print("deleted successful")


def delete_all_tasks(conn):
    sql = 'DELETE FROM tasks'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    print("deleted all successful")

create_table(connection)
t = get_all_task(connection)
print(t)

