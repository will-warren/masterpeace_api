from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort

from instance.config import app_config

db = SQLAlchemy()

def create_app(config_name):
    from app.models import TextMP, ImageMP

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/textmp/', methods=['POST', 'GET'])
    def textmps():
        if request.method == "POST":
            title = str(request.data.get('title', ''))
            if title:
                textmp = TextMP(title=title)
                textmp.post = str(request.data.get('post', ''))
                textmp.author = str(request.data.get('author', ''))
                textmp.save()
                response = jsonify({
                    'id'    : textmp.id,
                    'title' : textmp.title,
                    'author': textmp.author,
                    'post'  : textmp.post,
                    'date_created' : textmp.date_created,
                    'date_modified': textmp.date_modified
                })
                response.status_code = 201
                return response
        else:
            # GET req
            textmps = TextMP.get_all()
            results = []

            for mp in textmps:
                obj = {
                    'id'    : mp.id,
                    'title' : mp.title,
                    'author': mp.author,
                    'post'  : mp.post,
                    'date_created' : mp.date_created,
                    'date_modified': mp.date_modified
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response
    
 

    @app.route('/textmp/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def mod_textmps(id, **kwargs):
        # retrieve a textmp by its id
        textmp = TextMP.query.filter_by(id=id).first()
        if not textmp:
            # Raise a 404 HTTPException if not foud
            abort(404)

        if request.method == "DELETE":
            textmp.delete()
            return {
                "message": "TextMP {} deleted successfully".format(textmp.title)
            }, 200
        
        elif request.method == 'PUT':
            textmp.title = str(request.data.get('title', ''))
            textmp.post = str(request.data.get('post', ''))
            textmp.author = str(request.data.get('author', ''))
            textmp.save()
            response = jsonify({
                    'id'    : textmp.id,
                    'title' : textmp.title,
                    'author': textmp.author,
                    'post'  : textmp.post,
                    'date_created' : textmp.date_created,
                    'date_modified': textmp.date_modified
            })
            response.status_code = 200
            return response
        
        else:
            # GET
            response = jsonify({
                    'id'    : textmp.id,
                    'title' : textmp.title,
                    'author': textmp.author,
                    'post'  : textmp.post,
                    'date_created' : textmp.date_created,
                    'date_modified': textmp.date_modified
            })
            response.status_code = 200
            return response

    # image file will be read as a url but loaded as a file
    # need to add file upload for images (POST)
    @app.route('/imagemp/', methods=["GET", "POST"])
    def imagemps():
        if request.method == "POST":
            title = str(request.data.get('title', ''))
            if title:
                imagemp = ImageMP(title=title)
                imagemp.post = str(request.data.get('post', ''))
                imagemp.author = str(request.data.get('author', ''))
                imagemp.save()
                response = jsonify({
                    'id'    : imagemp.id,
                    'title' : imagemp.title,
                    'author': imagemp.author,
                    'post'  : imagemp.post,
                    'date_created' :    imagemp.date_created,
                    'date_modified':    imagemp.date_modified
                })
                response.status_code = 201
                return response
        else:
            # GET req
            imagemps = ImageMP.get_all()
            results = []

            for mp in imagemps:
                obj = {
                    'id'    : mp.id,
                    'title' : mp.title,
                    'author': mp.author,
                    'post'  : mp.post,
                    'date_created' : mp.date_created,
                    'date_modified': mp.date_modified
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response

    @app.route('/imagemp/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def mod_imagemps(id, **kwargs):
        # retrieve a textmp by its id
        imagemp = ImageMP.query.filter_by(id=id).first()
        if not imagemp:
            # Raise a 404 HTTPException if not foud
            abort(404)

        if request.method == "DELETE":
            imagemp.delete()
            return {
                "message": "ImageMP {} deleted successfully".format(imagemp.title)
            }, 200
        
        elif request.method == 'PUT':
            imagemp.title = str(request.data.get('title', ''))
            imagemp.post = str(request.data.get('post', ''))
            imagemp.author = str(request.data.get('author', ''))
            imagemp.save()
            response = jsonify({
                    'id'    : imagemp.id,
                    'title' : imagemp.title,
                    'author': imagemp.author,
                    'post'  : imagemp.post,
                    'date_created' : imagemp.date_created,
                    'date_modified': imagemp.date_modified
            })
            response.status_code = 200
            return response
        
        else:
            # GET
            response = jsonify({
                    'id'    : imagemp.id,
                    'title' : imagemp.title,
                    'author': imagemp.author,
                    'post'  : imagemp.post,
                    'date_created' : imagemp.date_created,
                    'date_modified': imagemp.date_modified
            })
            response.status_code = 200
            return response
    
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app