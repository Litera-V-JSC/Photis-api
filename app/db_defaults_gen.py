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
	for cat in conf.DB_CATEGORIES:
		db.execute(
			"INSERT INTO categories"
			"(category)"
			"VALUES (?)",
			(cat,)
		)
		db.commit()
	print("<== Default categories generated ==>")


def generate_default_users(db, count=4):
	users = [{"username": f"u{i}", "password": generate_password_hash(f"p{i}"), "admin": choice([True, False])} for i in range(count)]
	for req in users:
		db.execute(
			"INSERT INTO users"
			"(username, password, admin)"
			"VALUES (?, ?, ?)",
			(list(req.values()))
		)
		db.commit()
	print("<== Default users generated ==>")


def generate_default_items(db, count=25):
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


def generate_defaults():
	db = sqlite3.connect(
		conf.DATABASE, detect_types=sqlite3.PARSE_DECLTYPES
	)
	generate_default_users(db)
	generate_default_items(db)
	generate_default_categories(db)
	print("<== Database initialized ==>")


if __name__ == "__main__":
	generate_defaults()