
from . import imagemp_blueprint

from flask.views import MethodView
from flask import abort, make_response, request, jsonify
from app.imagemp.models import ImageMP
from app.user.models import User

# imagemp = Blueprint('imagemp', __name__, url_prefix='/imagemp')
# image file will be read as a url but loaded as a file
# need to add file upload for images (POST)
class ImageMPView(MethodView):

    def __authenticate__(self, request):
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        return access_token

    def post(self):
        access_token = self.__authenticate__(request)

        if access_token:
            user_id = User.decode_token(access_token)
            # if error user_id is a string
            if not isinstance(user_id, str):
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
                else:
                    response.status_code = 400
        else:
            response.status_code = 401
            
        return response

    def get(self, id=False):
        access_token = self.__authenticate__(request)
        if access_token:
            if not id:
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
            else:
                imagemp = ImageMP.query.filter_by(id=id).first()
                if not imagemp:
                    abort(404)

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
            response.status_code = 401
            return response

    def put(self, id):
        access_token = self.__authenticate__(request)

        if access_token:
            user_id = User.decode_token(access_token)
            # if error user_id is a string
            if not isinstance(user_id, str):
                # retrieve a imagemp by its id
                imagemp = ImageMP.query.filter_by(id=id).first()
                if not imagemp:
                    abort(404)
                
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
                return make_response({'errors': [{'message': 'BAD REQUEST'}]}), 400
                
        else:
            return make_response({'errors': [{'message': 'UNAUTHORIZED ACCESS'}]}), 401

    def delete(self, id):
        access_token = self.__authenticate__(request)
        if access_token:
            imagemp = ImageMP.query.filter_by(id=id).first()
            if not imagemp:
                abort(404)

            imagemp.delete()
            return make_response({'message': 'DELETE SUCCESS'}), 204
        else:
            return make_response({'errors': [{'message': 'UNAUTHORIZED ACCESS'}]}), 401

imagemp_view = ImageMPView.as_view('imagemp_view')

imagemp_blueprint.add_url_rule('/imagemp/', view_func=imagemp_view, methods=['GET', 'POST',])

imagemp_blueprint.add_url_rule('/imagemp/<int:id>', view_func=imagemp_view, methods=['DELETE', 'GET', 'PUT'])