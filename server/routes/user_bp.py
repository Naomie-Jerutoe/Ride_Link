from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
from flask_marshmallow import Marshmallow
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import random, string
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt

from models import db, User, PasswordResetToken, TokenBlocklist
from schemas import userSchema, passwordRestTokenSchema

user_bp = Blueprint('user_bp', __name__)
ma = Marshmallow(user_bp)
api = Api(user_bp)

class Register(Resource):
  def post(self):
    data = request.get_json()
  
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
  
    
    # Check if email is valid
    if not email or '@' not in email or '.' not in email:
        return {"error": "Invalid email address."}, 400

    # Check if password is strong enough (you can adjust the criteria)
    if not (6 <= len(password) <= 50):
        return {"error": "Password must be between 8 and 50 characters."}, 400
    
    #Check whether a user exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return {"error":"User with that email address already exists"}, 403
    
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(
      username = username,
      email = email,
      password = hashed_password
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    result = userSchema.dump(new_user)
    response = make_response(jsonify(result), 201)
    return response

api.add_resource(Register, '/register')

class Login(Resource):
  def post(self):
    data = request.get_json()
  
    username = data.get('username')
    password = data.get('password')
    
    if not data:
      return jsonify({"message": "Fill in your username and password to Login"})
    
    user = User.query.filter_by(username=username).first()
    
    #associate a user to a token
    if user:
      #check if password matches
      if check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.username)
        refresh_token = create_refresh_token(identity=user.username)

        return make_response(jsonify({
          "message": "Logged In",
          "tokens": {
            "access": access_token,
            "refresh": refresh_token
            }
          }), 200)
      else:
        return make_response(jsonify({"message":"Invalid password"}), 400)
      
    else:
      return make_response(jsonify({"message":"Invalid username"}), 400)

api.add_resource(Login, '/login')

class ProtectedRoute(Resource):
  @jwt_required()
  def post(self):
    current_user = get_jwt_identity()
    return make_response(jsonify({"current_user_id": current_user, "message": "Access Granted"}), 200)
  
api.add_resource(ProtectedRoute, '/protected')

class ForgotPassword(Resource):
  def post(self):
    data = request.get_json()

    if not data:
      return jsonify({"message":"Received no data"})
    
    username = data.get('username')
    
    user = User.query.filter_by(username=username).first()
    if user:
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        expiration = datetime.now() + timedelta(seconds=3600)
        reset_token = PasswordResetToken(
          user_id = user.id,
          token = token,
          expiration = expiration
        )
        db.session.add(reset_token)
        db.session.commit()
        
        return make_response(jsonify({"message":"Password reset token generated successfully.Use it to reset password", "token": reset_token.token}))
    return jsonify({"message": "user not found"}), 400
  
api.add_resource(ForgotPassword, '/forgot_password')

class ResetToken(Resource):
  def post(self, token):
    data = request.get_json()
    new_password = data.get('new_password')
    
    reset_token = PasswordResetToken.query.filter_by(token=token).first()
    if reset_token and reset_token.expiration > datetime.now():
            user = User.query.get(reset_token.user_id)
            if user:
                hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')
                user.password = hashed_password
                
                db.session.delete(reset_token) 
                db.session.commit()
                
                return make_response(jsonify({"message": "Password reset is successful"}), 200)
            return jsonify({"message": "User not found"}), 404
    return jsonify({"message": "Invalid or expired reset token"}), 400
api.add_resource(ResetToken, '/reset_token/<string:token>')

class Logout(Resource):
    @jwt_required()
    def get(self):
        token = get_jwt()
        blocked_token = TokenBlocklist(
            jti=token['jti'], created_at=datetime.utcnow())
        db.session.add(blocked_token)
        db.session.commit()
        return {'detail': "Token logged out"}


api.add_resource(Logout, '/logout')

class Users(Resource):
  @jwt_required()
  def get(self):
    users = User.query.all()
    result = userSchema.dump(users, many=True)
    return make_response(jsonify(result), 200)

api.add_resource(Users, '/users')

class UserById(Resource):
  def get(self, id):
    user = User.query.filter_by(id=id).first()
    result = userSchema.dump(user)
    return make_response(jsonify(result),200)

api.add_resource(UserById, '/users/<string:id>')