from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort, make_response
from flask_cors import CORS

from instance.config import app_config

db = SQLAlchemy()

def create_app(config_name):
    from app.models import TextMP, ImageMP, User

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    CORS(app, resources=r'/*')

    @app.route('/users/<string:email>', methods=['GET', 'DELETE', 'PUT'])
    def user(email, **kwargs):
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            # if error user_id is a string
            if not isinstance(user_id, str):
                user = User.get(email)
                if request.method == "GET":
                    if user:
                        response = jsonify({
                            'data': {
                                'type': 'user',
                                'id': user.email,
                                'attributes': {
                                    'email': user.email,
                                    'location': user.location,
                                    'quip': user.quip,
                                    'photo': user.photo,
                                    'user_name': user.user_name
                                }
                            }
                        })
                        response.status_code = 200
                        return response
                        
                elif request.method == "DELETE":
                    user.delete()
                    return {
                        "message": "User {} deleted successfully".format(email)
                    }, 200  
                elif request.method == "PUT":
                    user.user_name = str(request.data.get('user_name', ''))
                    user.location = str(request.data.get('location', ''))
                    user.quip = str(request.data.get('quip', ''))
                    user.photo = str(request.data.get('photo', ''))
                    user.save()
                    response = jsonify({
                        'data': [{
                            'type': 'user',
                            'id': user.id,
                            'attributes': {
                                'email': user.email,
                                'location': user.location,
                                'quip': user.quip,
                                'photo': user.photo,
                                'user_name': user.user_name
                            }
                        }]
                    })
                    response.status_code = 200
                    return response
                else:
                    return make_response({'error' : 'Invalid request method'}), 400
        
            else:
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401
    
    @app.route('/textmp/', methods=['POST', 'GET'])
    def textmps():
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            # if error user_id is a string
            if not isinstance(user_id, str):
                if request.method == "POST":
                    title = str(request.data.get('title', ''))
                    if title:
                        textmp = TextMP(title=title)
                        textmp.post = str(request.data.get('post', ''))
                        textmp.author = str(request.data.get('author', user_id))
                        textmp.save()
                        response = jsonify({
                            'data': [{
                                'type': 'textmp',
                                'id': textmp.id,
                                'attributes': {
                                    'title': textmp.title,
                                    'author': textmp.author,
                                    'post': textmp.post,
                                    'date_created': textmp.date_created,
                                    'date_modified': textmp.date_modified
                                }
                            }]
                        })
                        response.status_code = 201
                        return response
                else:
                    # GET req
                    textmps = TextMP.get_all(user_id)
                    results = []

                    for mp in textmps:
                        obj = {
                            'type': 'textmp',
                            'id'    : mp.id,
                            'attributes': {
                                'title' : mp.title,
                                'author': mp.author,
                                'post'  : mp.post,
                                'date_created' : mp.date_created,
                                'date_modified': mp.date_modified
                            }
                        }
                        results.append(obj)
                    response = jsonify({ 'data': results })
                    response.status_code = 200
                    return response
            
            else:
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401
    
 

    @app.route('/textmp/<string:id>', methods=['GET', 'PUT', 'DELETE'])
    def mod_textmps(id, **kwargs):
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            # if error user_id is a string
            if not isinstance(user_id, str):
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
                        'data': [{
                            'type': 'textmp',
                            'id'    : textmp.id,
                            'attributes': {
                                'title' : textmp.title,
                                'author': textmp.author,
                                'post'  : textmp.post,
                                'date_created' : textmp.date_created,
                                'date_modified': textmp.date_modified
                            }
                        }]
                    })
                    response.status_code = 200
                    return response
                
                else:
                    # GET
                    response = jsonify({
                        'data': [{
                            'type': 'textmp',
                            'id'    : textmp.id,
                            'attributes': {
                                'title' : textmp.title,
                                'author': textmp.author,
                                'post'  : textmp.post,
                                'date_created' : textmp.date_created,
                                'date_modified': textmp.date_modified
                            }
                        }]
                    })
                    response.status_code = 200
                    return response
            else:
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401

    # image file will be read as a url but loaded as a file
    # need to add file upload for images (POST)
    @app.route('/imagemp/', methods=["GET", "POST"])
    def imagemps():
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            # if error user_id is a string
            if not isinstance(user_id, str):
                if request.method == "POST":
                    title = str(request.data.get('title', ''))
                    if title:
                        imagemp = ImageMP(title=title)
                        imagemp.post = str(request.data.get('post', ''))
                        imagemp.author = str(request.data.get('author', ''))
                        imagemp.save()
                        response = jsonify({
                            'data': [{
                                'type': 'imagemp',
                                'id': imagemp.id,
                                'attributes': {
                                    'title': imagemp.title,
                                    'author': imagemp.author,
                                    'post': imagemp.post,
                                    'date_created': imagemp.date_created,
                                    'date_modified': imagemp.date_modified
                                }
                            }]
                        })
                        response.status_code = 201
                        return response
                else:
                    # GET req
                    imagemps = ImageMP.get_all(str(request.data.get('author')))
                    results = []

                    for mp in imagemps:
                        obj = {
                            'type': 'imagemp',
                            'id'    : mp.id,
                            'attributes': {
                                'title' : mp.title,
                                'author': mp.author,
                                'post'  : mp.post,
                                'date_created' : mp.date_created,
                                'date_modified': mp.date_modified
                            }
                        }
                        results.append(obj)
                    response = jsonify({'data': results})
                    response.status_code = 200
                    return response
            else:
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401

    @app.route('/imagemp/<string:id>', methods=['GET', 'PUT', 'DELETE'])
    def mod_imagemps(id, **kwargs):
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            # if error user_id is a string
            if not isinstance(user_id, str):
                # retrieve a imagemp by its id
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
                            'data': [{
                                'type': 'imagemp',
                                'id'    : imagemp.id,
                                'attributes': {
                                    'title' : imagemp.title,
                                    'author': imagemp.author,
                                    'post'  : imagemp.post,
                                    'date_created' : imagemp.date_created,
                                    'date_modified': imagemp.date_modified
                                }
                            }]
                    })
                    response.status_code = 200
                    return response
                
                else:
                    # GET
                    response = jsonify({
                        'data': [{
                            'type': 'imagemp',
                            'id'    : imagemp.id,
                            'attributes': {
                                'title' : imagemp.title,
                                'author': imagemp.author,
                                'post'  : imagemp.post,
                                'date_created' : imagemp.date_created,
                                'date_modified': imagemp.date_modified
                            }
                        }]
                    })
                    response.status_code = 200
                    return response
            else:
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401
    
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app