from flask import Flask
from flask_jwt_extended import JWTManager
import routing
import db
import config_module
import logging, logging.config, yaml 
import os


def create_app():
	app = Flask(__name__)
	app.config.from_object(config_module.Config())

	app.register_blueprint(routing.bp)

	app.add_url_rule("/", endpoint="index")

	logging.config.dictConfig((yaml.safe_load(open(os.path.join(os.path.dirname(__file__), 'logging.conf')))))
	logfile = logging.getLogger('file')
	logconsole = logging.getLogger('console')
	logfile.debug("Application created")
	logconsole.debug("Application created")

	db.init_app(app)
	jwt = JWTManager(app)
	os.makedirs(app.config['FILE_STORAGE'], exist_ok=True)
	
	return app