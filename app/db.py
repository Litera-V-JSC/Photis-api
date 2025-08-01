from flask import g, current_app, jsonify
from werkzeug.security import check_password_hash
import sqlite3
from lib.file_utils import *
import datetime
import json
import shutil


def get_db():
	if "db" not in g:
		g.db = sqlite3.connect(
			current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
		)
		g.db.row_factory = sqlite3.Row
	return g.db


def close_db(e=None):
	db = g.pop("db", None)
	if db is not None:
		db.close()
	

def get_item_by_id(id):
	try:
		db = get_db()
		return db.execute("SELECT * FROM items WHERE id = ?;", (id,)).fetchone()
	except Exception:
		return None


""" Returns list of item with specific id """
def get_items(id_list: list):
	try:
		db = get_db()
		items = []
		for id in id_list:
			item = get_item_by_id(id)
			if not item is None:
				items.append(item)
		return items
	except Exception:
		return None


def get_all_items():
	try:
		db = get_db()
		return db.execute("SELECT * FROM items").fetchall()
	except Exception as e:
		return None


def add_item(data):
	try:
		db = get_db()
		# image data should be base64 string only
		b64_string = data['image']
		filename = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.png'
		response = upload_file(b64_string, filename)
		if response is None:
			raise db.IntegrityError("invalid base64 string")
		db.execute(
				"INSERT INTO items"
				"(category, sum, creation_date, file_name)"
				"VALUES (?, ?, ?, ?)",
				(data['category'], data["sum"], data["creation_date"], filename)
			)
		db.commit()
		return True
	except db.IntegrityError:
		return None


""" check is there are other items using this photo """
def check_attachment(id: int, filename: str):
	try:	
		db = get_db()
		return list(db.execute(
			"SELECT * FROM items WHERE file_name = ?;",
			(filename,)
			).fetchall())
	except Exception as e:
		return None


def delete_item(id):
	try:
		db = get_db()
		filename = dict(get_items([id])[0])["file_name"]
		items_with_similar_attachment = check_attachment(id, filename)
		if items_with_similar_attachment is None:
			return None
		db.execute("DELETE FROM items WHERE id = ?;", (id,))
		db.commit()
		# if we dont have other items using this file, we remove it
		if len(items_with_similar_attachment) == 1:
			print("path:", os.path.join(
				current_app.root_path, 
				current_app.config['FILE_STORAGE'], 
				filename
			))
			os.remove(path = os.path.join(
				current_app.root_path, 
				current_app.config['FILE_STORAGE'], 
				filename
			))
		return True
	except Exception as e:
		return None


def delete_category(id):
	try:
		db = get_db()
		db.execute("DELETE FROM categories WHERE id = ?;", (id,))
		db.commit()
		return True
	except Exception:
		return None


def add_category(data):
	try:
		db = get_db()
		db.execute(
			"INSERT INTO categories"
			"(category)"
			"VALUES (?)",
			(data['category'],)
		)
		db.commit()
		return True
	except db.IntegrityError:
		return None


def get_categories():
	try:
		db = get_db()
		return db.execute("SELECT * FROM categories").fetchall()
	except Exception as e:
		return None



""" Check login data """
def check_user(username, password):
	try:
		db = get_db()
		user = dict(db.execute(
			"SELECT * FROM users WHERE username = ?;",
			(username,)
			).fetchone())
		return check_password_hash(user['password'], password)
	except Exception:
		return False
		


def init_db(conf):
	os.makedirs(conf["FILE_STORAGE"], exist_ok=True)
	db = sqlite3.connect(
		conf["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
	)
	cur = db.cursor()
	with open(conf["SCHEMA"]) as schema:
		cur.executescript(schema.read()) 


def init_app(app):
	app.teardown_appcontext(close_db)
	