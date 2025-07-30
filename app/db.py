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
	db = get_db()
	try:
		return db.execute("SELECT * FROM items WHERE id = ?;", (id,)).fetchone()
	except db.IntegrityError:
		return None


""" Returns list of item with specific id """
def get_items(id_list: list):
	db = get_db()
	items = []
	try:
		for id in id_list:
			item = get_item_by_id(id)
			if not item is None:
				items.append(item)
		return items
	except db.IntegrityError:
		return None


def get_all_items():
	db = get_db()
	try:
		return db.execute("SELECT * FROM items").fetchall()
	except Exception as e:
		return None


def add_item(data):
	db = get_db()
	try:
		# image data should be base64 string only
		b64_string = data['image']
		filename = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.png'
		resp = upload_file(b64_string, filename)
		if resp is None:
			return jsonify({'error': 'Invalid base64 data'}), 400
		else:
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
	db = get_db()
	try:	
		return list(db.execute(
			"SELECT * FROM items WHERE file_name = ?;",
			(filename,)
			).fetchall())
	except Exception as e:
		return None


def delete_item(id):
	db = get_db()
	try:
		filename = dict(get_items([id])[0])["file_name"]
		items_ = check_attachment(id, filename)
		if items_ is None:
			return None
		else:
			db.execute("DELETE FROM items WHERE id = ?;", (id,))
			db.commit()
			# if we dont have other items using this file, we remove it
			if len(items_) == 1:
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
		print(e)
		return None

""" Update category list """
def update_categories(new_categories: list):
	try:
		db = get_db()
		cursor.execute("DELETE FROM categories")
		cursor.execute("DELETE FROM sqlite_sequence WHERE name='categories'")
		db.executemany("INSERT INTO categories (category,) VALUES (?,)", new_categories)
		return True
	except Exception as e:
		return None


def get_categories():
	try:
		db = get_db()
		return [i["category"] for i in list(db.execute("SELECT * FROM categories").fetchall())]
	except Exception as e:
		return None



""" Check login data """
def check_user(username, password):
	db = get_db()
	user = dict(db.execute(
		"SELECT * FROM users WHERE username = ?;",
		(username,)
		).fetchone())
	return check_password_hash(user['password'], password)
	


def init_db():
	db = get_db()
	with current_app.open_resource(current_app.config["SCHEMA"]) as schema:
		db.executescript(schema.read().decode("utf8"))


def init_app(app):
	app.teardown_appcontext(close_db)
	