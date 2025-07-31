from flask import current_app, jsonify
import os
import base64


""" Encode base64 string to binary """ 
def encode_base64(b64_string):
	if ',' in b64_string:
		b64_string = b64_string.split(',')[1]
	try:
		img_data = base64.b64decode(b64_string)
	except Exception as e:
		return None 
	return img_data


""" Добавление файла """
def upload_file(b64_string, filename):
	img_data = encode_base64(b64_string)
	if img_data is None:
		return None
	else:
		storage_path = os.path.join(current_app.root_path, current_app.config['FILE_STORAGE'])
		with open(os.path.join(storage_path, filename), 'wb') as f:
			f.write(img_data)
		return True


"""
Removes files from storage.
extensions - determines files with which extensions should be removed
"""
def clear_storage(extensions=[]):
	directory_path = os.path.realpath(current_app.config['FILE_STORAGE'])
	for item_name in os.listdir(directory_path):
		item_path = os.path.join(directory_path, item_name)
		if os.path.isfile(item_path) and item_name.split('.')[-1] in extensions:
			os.remove(item_path)
			print(f"Removed file: {item_path}")