from flask import Flask, jsonify
from flask_migrate import Migrate
from extensions import db, jwt, cors
from datetime import timedelta
import os
from models import User, Booking, Ride, Driver, PasswordResetToken, Review, TokenBlocklist
from routes.user_bp import user_bp
from routes.ride_bp import ride_bp
from routes.booking_bp import booking_bp

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', False)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ridelink.db'
    app.config['SQLALCHEMY_ECHO'] = os.getenv('FLASK_SQLALCHEMY_ECHO', False)
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
    
    #initialize extensions
    migrate = Migrate(app, db)
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    
    #register blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(ride_bp)
    app.register_blueprint(booking_bp)
    
    
    # jwt error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
            return jsonify({"message": "Token has expired", "error": "token_expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
            return (
                jsonify(
                    {"message": "Signature verification failed", "error": "invalid_token"}
                ),
                401,
            )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
            return (
                jsonify(
                    {
                        "message": "Request doesnt contain valid token",
                        "error": "authorization_header",
                    }
                ),
                401,
            )
        
    @jwt.token_in_blocklist_loader
    def token_in_blocklist_callback(jwt_header,jwt_data):
            jti = jwt_data['jti']

            token = db.session.query(TokenBlocklist).filter(TokenBlocklist.jti == jti).scalar()

            return token is not None
    
    return app

app = create_app()
