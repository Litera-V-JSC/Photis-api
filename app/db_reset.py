import sqlite3
import config_module
from lib.file_utils import *
from werkzeug.security import generate_password_hash
from random import *
import os
import datetime
import shutil


conf = config_module.Config()


def generate_default_users(db, count=4):
	users = [{"username": f"u{i}", "password": generate_password_hash(f"p{i}")} for i in range(count)]
	for req in users:
		db.execute(
				"INSERT INTO users"
				"(username, password)"
				"VALUES (?, ?)",
				(list(req.values()))
			)
		db.commit()
	print("<== Default users generated ==>")


def generate_default_receipts(db, count=5):
	categories = ["ГСМ топливо", "Товары", "Услуги"]
	dates = ["2025-07-"+f"{day}".zfill(2) for day in range(1, 31)]
	receipts = [
		{"category": choice(categories), "sum": randint(100, 4242), "receipt_date": choice(dates), "file_name": "sample.png"} for _ in range(count)
	]
	for req in receipts:
		db.execute(
				"INSERT INTO receipts"
				"(category, sum, receipt_date, file_name)"
				"VALUES (?, ?, ?, ?)",
				(list(req.values()))
			)
		db.commit()
	print("<== Default receipts generated ==>")


def reset_db():
	print(os.path.realpath(os.path.join('storage', 'database.sqlite')))
	os.makedirs(conf.FILE_STORAGE, exist_ok=True)
	try:
		os.remove(conf.DATABASE)
		print('Removed previous database file')
	except FileNotFoundError:
		print("Creating new database file")
	db = sqlite3.connect(
		conf.DATABASE, detect_types=sqlite3.PARSE_DECLTYPES
	)
	cur = db.cursor()
	with open(conf.SCHEMA) as schema:
		cur.executescript(schema.read()) 
		generate_default_users(db)
		generate_default_receipts(db)
		print("<== Database initialized ==>")
	

if __name__ == "__main__":
	reset_db()