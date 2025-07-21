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
	

def get_receipt_by_id(id):
	db = get_db()
	try:
		receipt = db.execute("SELECT * FROM receipts WHERE id = ?;", (id,)).fetchone()
	except db.IntegrityError:
		return None
	return receipt


""" Returns list of receipt by id list """
def get_receipt_group(id_list):
	db = get_db()
	receipts = []
	try:
		for id in id_list:
			receipt = get_receipt_by_id(id)
			if not receipt is None:
				receipts.append(receipt)
	except db.IntegrityError:
		return None
	return receipts


def get_all_receipts():
	db = get_db()
	return db.execute("SELECT * FROM receipts").fetchall()


def get_categories():
	db = get_db()
	return db.execute("SELECT DISTINCT category FROM receipts").fetchall()


""" Filtering receipts by date """
def get_filtered_receipts(start, end, category):
	db = get_db()
	try:
		if start == end == "all":
			receipts = db.execute(
				"SELECT * FROM receipts WHERE category = ?;", (category,)
			).fetchall()
		elif category == 'all':
			receipts = db.execute(
				"SELECT * FROM receipts WHERE ? <= receipt_date AND receipt_date <= ?"
				"ORDER BY receipt_date DESC;", (start, end)
			).fetchall()
		else:
			receipts = db.execute(
					"SELECT * FROM receipts WHERE ? <= receipt_date AND receipt_date <= ? AND category = ?"
					"ORDER BY receipt_date DESC;", (start, end, category)
				).fetchall()
	except db.IntegrityError:
		return None
	return receipts


def add_new_receipt(request):
	data = request.get_json()
	print(data)
	# image data should be base64 string only
	if not data or 'image' not in data:
		return jsonify({'error': 'data is missing'}), 404
	db = get_db()

	try:
		b64_string = data['image']
		filename = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.png'
		resp = upload_file(b64_string, filename)
		if resp[1] not in (200, 204):
			return resp

		db.execute(
				"INSERT INTO receipts"
				"(category, sum, receipt_date, file_name)"
				"VALUES (?, ?, ?, ?)",
				(data['category'], data["sum"], data["receipt_date"], filename)
			)
		db.commit()
	except db.IntegrityError:
		return jsonify({'error': 'receipt already exists'}), 404
	return '', 204


""" check is there are other receipts using this photo """
def is_file_attached(id):
	db = get_db()
	try:	
		receipt = dict(get_receipt_by_id(id))
		print(receipt)
		same_photo_receipts = db.execute(
			"SELECT * FROM receipts WHERE file_name = ?;",
			(receipt['file_name'],)
			).fetchall()
	except Exception as e:
		return jsonify({'error': f"Invalid id: {id}"}), 404
	return (len(list(same_photo_receipts)) != 0, receipt['file_name'])


def delete_receipt(id):
	db = get_db()
	try:
		attached, filename = is_file_attached(id)
		if filename == 404:
			raise db.IntegrityError("Invalid id: {id}")
		db.execute("DELETE FROM receipts WHERE id = ?;", (id,))
		db.commit()
		if attached:
			os.remove(path = os.path.join(
				current_app.root_path, 
				current_app.config['FILE_STORAGE'], 
				filename
			))
	except db.IntegrityError as e:
		return jsonify({'error': str(e)}), 404
	return '', 204


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
	