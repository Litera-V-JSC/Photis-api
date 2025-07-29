import json
import os
from dotenv import load_dotenv


with open(os.path.join(os.path.dirname(__file__), "app_config.json")) as file:
	CONFIG_FILE = json.load(file)
	load_dotenv()


class Config(object):
	global CONFIG_FILE
	DATABASE = os.path.abspath(os.path.join(os.path.dirname(__file__), CONFIG_FILE["DATABASE"]))
	SCHEMA = os.path.join(os.path.dirname(__file__), CONFIG_FILE["SCHEMA"])
	FILE_STORAGE = os.path.join(os.path.dirname(__file__), CONFIG_FILE["FILE_STORAGE"])
	ALLOWED_EXTENSIONS = CONFIG_FILE["ALLOWED_EXTENSIONS"]
	SECRET_KEY = os.getenv("SECRET_KEY")
	BACKUP = os.path.join(os.path.dirname(__file__), CONFIG_FILE["BACKUP"])
