from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from instance.config import app_config

db = SQLAlchemy()

def create_app(config_name):
    
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    CORS(app, resources=r'/*')
    
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .imagemp import imagemp_blueprint
    app.register_blueprint(imagemp_blueprint)

    from .user import user_blueprint
    app.register_blueprint(user_blueprint)

    from .textmp import textmp_blueprint
    app.register_blueprint(textmp_blueprint)

    return app