import os
import logging, logging.config, yaml 

def set_logging(config_path, logs_path):
	os.makedirs(logs_path, exist_ok=True)

	empty_config = False
	try:
		empty_config = os.path.getsize(config_path) == 0
	except Exception as e:
		empty_config = True

	if empty_config:
		config = open(config_path, 'w+')
		config.write(
f"""version: 1
formatters:
  hiformat:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
  simple:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
handlers:
  console:
    class: logging.StreamHandler
    level: DEBUG
    formatter: hiformat
    stream: ext://sys.stdout
  file:
    class: logging.FileHandler
    level: DEBUG
    formatter: simple
    filename: {os.path.join(logs_path, 'app.log')}
loggers:
  console:
    level: DEBUG
    handlers: [console]
    propagate: no
  file:
    level: DEBUG
    handlers: [file]
    propagate: no
root:
  level: DEBUG
  handlers: [console,file] """)
		config.close()

	config = open(config_path, 'r+')	
	logging.config.dictConfig(yaml.safe_load(config))
	config.close()

	logfile = logging.getLogger('file')
	logconsole = logging.getLogger('console')
	logfile.debug("Application created")
	logconsole.debug("Application created")