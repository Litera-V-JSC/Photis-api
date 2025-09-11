import sqlite3
import config_module
from lib.file_utils import *
from werkzeug.security import generate_password_hash
from random import *
import os
import datetime
import shutil


conf = config_module.Config()


def generate_default_categories(db):
	try:
		for cat in conf.DB_CATEGORIES:
			db.execute(
				"INSERT INTO categories"
				"(category)"
				"VALUES (?)",
				(cat,)
			)
			db.commit()
		print("<== Default categories generated ==>")
	except sqlite3.IntegrityError:
		print("! Skipping generation: Categories table is not empty")


def generate_default_users(db):
	try:
		users = [{"username": f"usr1", "password": generate_password_hash("pasw1"), "admin": False}, {"username": "adm_usr", "password": generate_password_hash("adm_pasw"), "admin": True}]
		for req in users:
			db.execute(
				"INSERT INTO users"
				"(username, password, admin)"
				"VALUES (?, ?, ?)",
				(list(req.values()))
			)
			db.commit()
		print("<== Default users generated ==>")
	except sqlite3.IntegrityError:
		print("! Skipping generation: Users table is not empty")


def generate_default_items(db, count=25):
	try:
		# skip generation if table already has default items - needed because item table has no unique fields
		if len(db.execute("SELECT * FROM items").fetchall()) > 0:
			raise sqlite3.IntegrityError

		categories = ["ГСМ топливо", "Товары", "Услуги"]
		dates = ["2025-07-"+f"{day}".zfill(2) for day in range(1, 31)]
		items = [
			{"category": choice(categories), "sum": randint(100, 4242), "creation_date": choice(dates), "file_name": "sample.png"} for _ in range(count)
		]
		for item in items:
			db.execute(
				"INSERT INTO items"
				"(category, sum, creation_date, file_name)"
				"VALUES (?, ?, ?, ?)",
				(list(item.values()))
			)
			db.commit()
		print("<== Default items generated ==>")
	except sqlite3.IntegrityError:
		print("! Skipping generation: Item table is not empty")


def generate_defaults():
	non_exist = False
	if not os.path.exists(conf.DATABASE):
		non_exist = True

	db = sqlite3.connect(
		conf.DATABASE, detect_types=sqlite3.PARSE_DECLTYPES
	)
	if non_exist:
		cur = db.cursor()
		with open(conf.SCHEMA) as schema:
			cur.executescript(schema.read()) 

	generate_default_users(db)
	generate_default_items(db)
	generate_default_categories(db)
	print("<== Database initialized ==>")


if __name__ == "__main__":
	generate_defaults()