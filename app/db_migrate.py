import os
import sqlite3
import shutil
from werkzeug.security import generate_password_hash

def migrate():
	OLD_DP_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'storage', 'database.sqlite')
	BACKUP_DP_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'storage', 'database.sqlite')
	SCHEMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'storage', 'schema.sql')


	shutil.copy(OLD_DP_PATH, BACKUP_DP_PATH)
	os.remove(OLD_DP_PATH)

	with open(SCHEMA_PATH) as schema:
		conn = sqlite3.connect(OLD_DP_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
		conn.cursor.executescript(schema.read()) 
		conn.close()

	conn = sqlite3.connect(BACKUP_DP_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
	receipts = conn.execute("SELECT * FROM receipts").fetchall()
	categories = conn.execute("SELECT * FROM categories").fetchall()
	conn.close()

	conn = sqlite3.connect(OLD_DP_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
	for receipt in receipts:
		conn.execute(
			"INSERT INTO items"
			"(category, sum, creation_date, file_name)"
			"VALUES (?, ?, ?, ?)",
			(receipt[0], receipt[1], receipt[2], receipt[3])
		)
	for category in categories:
		conn.execute(
			"INSERT INTO categories"
			"(category)"
			"VALUES (?)",
			(category,)
		)
	users = [{"username": f"user1", "password": generate_password_hash(f"pasw1"), "admin": False}, {"username": f"adm_usr", "password": generate_password_hash(f"adm_pasw"), "admin": True}]
	for user in users:
		conn.execute(
			"INSERT INTO users"
			"(username, password, admin)"
			"VALUES (?, ?, ?)",
			(user['username'].strip(), generate_password_hash(user['password']), user["admin"])
		)
	conn.close()

if __name__ == "__main__":
	migrate()