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

	os.makedirs(os.path.join(app.config['FILE_STORAGE'], "logs"), exist_ok=True)

	with open(app.config["LOGGING_CONFIG"]) as logging_conf:
		logging.config.dictConfig(yaml.safe_load(logging_conf))
	logfile = logging.getLogger('file')
	logconsole = logging.getLogger('console')
	logfile.debug("Application created")
	logconsole.debug("Application created")

	if not os.path.exists(app.config["DATABASE"]):
		db.init_db(conf=app.config)
		
	db.init_app(app)

	jwt = JWTManager(app)
	
	return app