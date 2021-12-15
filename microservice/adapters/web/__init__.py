import logging
from icecream import ic
from flask import Flask
from microservice.core.exceptions import NoConfigFile


def create_app(config=None, actions=None):
    if config is None:
        msg = 'Config file variable is not defined'
        logging.critical(msg)
        raise NoConfigFile(msg)
    logging.info('creating web app')
    app = Flask(__name__, instance_relative_config=True)
    for k, v in config.items():
        app.config[k] = v
    app.ms_actions = actions

    with app.app_context():
        from microservice.adapters.web.controllers.root import blueprint as root
        from microservice.adapters.web.controllers.test import blueprint as test
        app.register_blueprint(root)
        app.register_blueprint(test, url_prefix="/test")

    return app

    # app = Flask(__name__, instance_relative_config=True)
    # config = os.getenv('MS_CONFIG')
    # if config is None:
    #     raise NoConfigFile("Variable de entorno MS_CONFIG no definida")
    # core = Core()
    # core.config.from_yaml(config)
    # fc.init_app(app, core)
    # web_config = core.config.get('flask')
    # for k, v in web_config.items():
    #     app.config[k] = v
    # with app.app_context():
    #     from .controllers import blueprint
    #     app.register_blueprint(blueprint)
    # return app
