
from . import textmp_blueprint

from flask.views import MethodView
from flask import abort, make_response, request, jsonify
from app.textmp.models import TextMP
from app.user.models import User

#JSON API Error Objects
BAD_REQ_ERROR = {
    'status': 400,
    'title': 'We don\'t understand what you want'
}

UNAUTH_ERROR = {
    'status': 401,
    'title': 'Access Denied'
}


# image file will be read as a url but loaded as a file
# need to add file upload for images (POST)
class TextMPView(MethodView):

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
                    textmp = TextMP(title=title)
                    textmp.post = str(request.data.get('post', ''))
                    textmp.author = str(request.data.get('author', ''))
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
                else:
                    response.status_code = 400
                    response.errors = [BAD_REQ_ERROR]
        else:
            response.status_code = 401
            response.errors = [UNAUTH_ERROR]
            
        return response

    def get(self, id=False):
        access_token = self.__authenticate__(request)
        if access_token:
            if not id:
                textmps = TextMP.get_all(str(request.data.get('author')))
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
                response = jsonify({'data': results})
                response.status_code = 200
            else:
                textmp = TextMP.query.filter_by(id=id).first()
                if not textmp:
                    abort(404)

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
            response.status_code = 401
            response.errors = [UNAUTH_ERROR]
            return response

    def put(self, id):
        access_token = self.__authenticate__(request)

        if access_token:
            user_id = User.decode_token(access_token)
            # if error user_id is a string
            if not isinstance(user_id, str):
                # retrieve a textmp by its id
                textmp = TextMP.query.filter_by(id=id).first()
                if not textmp:
                    abort(404)
                
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
                return make_response({'errors': [BAD_REQ_ERROR]}), 400
                
        else:
            return make_response({'errors': [UNAUTH_ERROR]}), 401

    def delete(self, id):
        access_token = self.__authenticate__(request)
        if access_token:
            textmp = TextMP.query.filter_by(id=id).first()
            if not textmp:
                abort(404)

            textmp.delete()
            return make_response({'data': {'message': 'DELETE SUCCESS'} }), 204
        else:
            return make_response({'errors': [UNAUTH_ERROR]}), 401

textmp_view = TextMPView.as_view('textmp_view')

textmp_blueprint.add_url_rule('/textmp/', view_func=textmp_view, methods=['GET', 'POST',])

textmp_blueprint.add_url_rule('/textmp/<int:id>', view_func=textmp_view, methods=['DELETE', 'GET', 'PUT'])