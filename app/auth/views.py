from . import auth_blueprint

from flask.views import MethodView
from flask import make_response, request, jsonify
from app.models import User

class RegistrationView(MethodView):
    """Registers a new user."""
    
    def post(self):
        """Handle POST request for this view. URL ---> /auth/register"""

        user = User.query.filter_by(email=request.data['email']).first()

        if not user:
            try:
                post_data = request.data
                email = post_data['email']
                password = post_data['password']
                user = User(email=email, password=password)
                user.location=post_data['location']
                user.quip=post_data['quip']
                user.photo=post_data['photo']
                user.display_name=post_data['display_name']
                user.save()

                response = {
                    "message": "You have been registered successfully. Please log in."
                }

                # notify user
                return make_response(jsonify(response)), 201
            except Exception as e:

                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 401

        else:

            response = {
                'message': 'User already exists. Please log in'
            }

            return make_response(jsonify(response)), 202


class LoginView(MethodView):
    """Handles login and acess token generation"""

    def post(self):
        """ POST request for this view. url --->url/login"""
        try:
            user = User.query.filter_by(email=request.data['email']).first()
            if user and user.password_is_valid(request.data['password']):
                access_token = user.generate_token(user.id)
                if access_token:
                    response = {
                        'message': 'You logged in successfully',
                        'access_token': access_token.decode(),
                        'user_name': user.email
                    }
                    return make_response(jsonify(response)), 200
            else:
                response = {
                    'message': 'Invalid email or password, Please try again'
                }
                return make_response(jsonify(response)), 401

        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500    
    
registration_view = RegistrationView.as_view('registration_view')
login_view = LoginView.as_view('login_view')

auth_blueprint.add_url_rule('/auth/register', view_func=registration_view, methods=['POST'])
auth_blueprint.add_url_rule('/auth/login', view_func=login_view, methods=['POST'])

