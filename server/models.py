from extensions import db
from sqlalchemy import Enum
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    image_url = db.Column(db.String(100), nullable=True)
    
    bookings = db.relationship('Booking', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    
    def __repr__(self):
        return f"<User {self.username}>"

class PasswordResetToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    expiration = db.Column(db.DateTime, nullable=False)
    token = db.Column(db.String(100), nullable=False)
    
    user = db.relationship('User', backref='reset_tokens')
    
class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    location = db.Column(db.String(100))
    age = db.Column(db.Integer)
    
    rides = db.relationship('Ride', backref='driver', lazy=True)
    
    def __repr__(self):
        return f"<Driver {self.username}>"
    
class Ride(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    departure_location = db.Column(db.String(100))
    destination = db.Column(db.String(100))
    departure_time = db.Column(db.DateTime)
    available_seats = db.Column(db.Integer)
    price = db.Column(db.Float)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=False)
    
    bookings = db.relationship('Booking', backref='ride', lazy=True)
    reviews = db.relationship('Review', backref='ride', lazy=True)
    
    def __repr__(self):
        return f"<Ride {self.departure_location, self.departure_time}>"

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ride_id = db.Column(db.Integer, db.ForeignKey('ride.id'), nullable=False)
    status = db.Column(Enum("confirmed", "pending", "cancelled"), nullable=False)
    
    def __repr__(self):
        return f"<Booking {self.status}>"
    
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comments = db.Column(db.String)
    rating = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ride_id = db.Column(db.Integer, db.ForeignKey('ride.id'), nullable=False)
    
    def __repr__(self):
        return f"<Review {self.comments}>"

class TokenBlocklist(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    jti = db.Column(db.String(), nullable=False)
    create_at = db.Column(db.DateTime(), default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Token {self.jti}>"