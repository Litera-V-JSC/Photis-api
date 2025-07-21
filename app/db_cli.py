import sqlite3
import config_module
from lib.file_utils import *
from werkzeug.security import generate_password_hash
from random import *
import os
import datetime
import shutil


conf = config_module.Config()


""" Make backup of databse """
def make_backup():
	os.makedirs(os.path.join(conf.BACKUP, 'storage'), exist_ok=True)
	timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
	db_backup = os.path.join(conf.BACKUP, timestamp+'.sqlite')
	shutil.copy(os.path.realpath(conf.DATABASE), db_backup)
	storage = conf.FILE_STORAGE
	for item_name in os.listdir(storage):
		item_path = os.path.join(storage, item_name)
		if os.path.isfile(item_path):
			shutil.copy(item_path, os.path.join(conf.BACKUP, "storage", item_name))
			print(f"Copied file: {item_path}")
	print(f"Backup created: {db_backup}")


def generate_default_users(db):
	users = [{"username": f"u{i}", "password": generate_password_hash(f"p{i}")} for i in range(4)]
	for user in users:
		db.execute(
					"INSERT INTO users"
					"(username, password)"
					"VALUES (?, ?);",
					(list(user.values()))
				)
		db.commit()
	print("<== Default users generated ==>")


def generate_default_receipts(db):
	categories = ["Прочее", "Квитанция ЖКХ", "Магазины"]
	dates = ["2025-07-"+f"{day}".zfill(2) for day in range(1, 31)]
	receipts = [
		{"category": choice(categories), "sum": randint(100, 4242), "receipt_date": choice(dates), "file_name": "sample.jpg"} for _ in range(20)
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
	print(os.path.realpath('database.sqlite'))
	try:
		os.remove(os.path.join(os.path.dirname(__file__), 'database.sqlite'))
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
	action = None
	while action is None:
		ans = input('Choose an option: 1 - reset database, 2 - make backup')
		if ans in ('1', '2'):
			action = ans
		if ans == '1':
			reset_db()
		elif ans == '2':
			make_backup()