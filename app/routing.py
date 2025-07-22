from flask import abort, Blueprint, request, current_app, send_from_directory, jsonify, make_response

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies

from lib.report import create_pdf
import db
import os
import datetime


bp = Blueprint('routing', __name__)

""" Using an `after_request` callback, we refresh any token that is within 30 """
@bp.after_request
def refresh_expiring_jwts(response):
	try:
		exp_timestamp = get_jwt()["exp"]
		now = datetime.datetime.now(datetime.timezone.utc)
		target_timestamp = datetime.datetime.timestamp(now + datetime.timedelta(minutes=30))
		if target_timestamp > exp_timestamp:
				access_token = create_access_token(identity=get_jwt_identity())
				set_access_cookies(response, access_token)
		return response
	except (RuntimeError, KeyError):
		# Case where there is not a valid JWT. Just return the original response
		return response


""" Auth to get JWT token with password"""
@bp.route('/login', methods=("GET", "POST"))
def login():
	username = request.json.get("username", None)
	password = request.json.get("password", None)
	if not db.check_user(username, password):
		return jsonify({'error': 'invalid password'}), 404

	jwt_token = create_access_token(identity=username)
	return make_response(jsonify({'access_token': jwt_token}), 200)


""" Index page, does not accept any requests"""
@bp.route('/', methods=("GET", "POST"))
def index():
	return abort(400)


""" Add receipt info to database and save its img """
@bp.route('/add', methods=("POST",))
@jwt_required()
def add_receipt():
	return db.add_new_receipt(request)


""" Delete existing receipt """
@bp.route('/delete/<int:id>', methods=("DELETE",))
@jwt_required()
def delete_receipt(id):
	return db.delete_receipt(id)


""" 
Get receipt by its id or list of all available receipts 
id=all - list of all receipts; 
id=<id:int> - only one receipt with unique id
"""
@bp.route('/receipt/<id>', methods=("GET",))
@jwt_required()
def get_receipt(id):
	if str(id) == "all":
		receipts = db.get_all_receipts()
		if receipts is None:
			return jsonify({'error': f"error while loading list of all receipts from database"}), 404
		return jsonify([dict(row) for row in receipts]), 200
	else:
		receipt = db.get_receipt_by_id(id)
		if receipt is None: 
			return jsonify({'error': f"invalid id: {id}"}), 404
		return jsonify(dict(receipt)), 200


"""
Get list of filtered receipts.
start, end - date filter
category - category filter
"""
@bp.route('/filter_receipt/<start>/<end>/<category>', methods=("GET",))
@jwt_required()
def filter_receipt(start, end, category):
	receipts = db.get_filtered_receipts(start, end, category)
	if receipts is None:
		return jsonify({'error': f"invalid data, start: {start}, end: {end}, category: {category}"}), 404
	return jsonify([dict(row) for row in receipts]), 200
		

""" Get receipt img """
@bp.route('/files/<int:id>', methods=("GET",))
@jwt_required()
def download(id):
	receipt = db.get_receipt_by_id(id)
	if receipt is None:
		return jsonify({'error': 'invalid receipt id'}), 404
	storage_path = os.path.join(current_app.root_path, current_app.config['FILE_STORAGE'])
	return send_from_directory(storage_path, receipt["file_name"])


""" Get receipt categories """
@bp.route('/categories', methods=("GET",))
@jwt_required()
def categories():
	return jsonify(["ГСМ топливо", "Товары", "Услуги"]), 200


""" Generate general receipts report """
@bp.route('/report', methods=("GET",))
@jwt_required()
def report():
	filename = "report " + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.pdf'
	receipts = db.get_receipt_group(request.json.get("id_list", None))
	if receipts is None:
		return jsonify({'error': 'invalid receipt id'}), 404
	resp = create_pdf(
		os.path.join(current_app.root_path, current_app.config['FILE_STORAGE'], filename),
		receipts
	)
	storage_path = os.path.join(current_app.root_path, current_app.config['FILE_STORAGE'])
	return send_from_directory(storage_path, filename)