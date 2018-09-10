from . import user_blueprint

from flask.views import MethodView
from flask import abort, make_response, request, jsonify

from app.user.models import User


class UserView(MethodView):

    def __authenticate__(self, request):
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        return access_token

    def get(self, email):
        access_token = self.__authenticate__(request)

        if access_token:
            user = User.get(email)
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
            
            else:
                return make_response({'errors': {'message': 'RESOURCE NOT FOUND'}}), 404
        
        else:
            return make_response({'errors': {'message': 'UNAUTHORIZED ACCESS'}}), 401

    def put(self, email):
        access_token = self.__authenticate__(request)

        if access_token:
            user = User.get(email)
            if user:
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
                return make_response({'errors': {'message': 'USER NOT FOUND'}}), 404
        else:
            return make_response({'errors' : {'message': 'UNAUTHORIZED REQUEST'}}), 401
            
    def delete(self, email):
        access_token = self.__authenticate__(request)

        if access_token:
            user = User.get(email)
            user.delete()
            return make_response({
                'data': [{
                    "message": "User {} deleted successfully".format(email)
                }]
            }), 200 
        else:
            return make_response({'errors': {'message': 'UNAUTHORIZED ACCESS'}}), 401

user_view = UserView.as_view('user_view')

user_blueprint.add_url_rule('/users/', view_func=user_view, methods=['GET', 'POST',])

user_blueprint.add_url_rule('/users/<string:email>', view_func=user_view, methods=['DELETE', 'GET', 'PUT'])