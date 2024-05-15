from flask import Blueprint
from flask_restful import Api
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field, fields
from marshmallow.fields import Nested
from models import User, PasswordResetToken, Driver, Ride, Booking, Review

serializer_bp = Blueprint('serializer_bp', __name__)
ma = Marshmallow(serializer_bp)
api = Api(serializer_bp)

class PasswordResetTokenSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PasswordResetToken
        include_fk = True

passwordRestTokenSchema = PasswordResetTokenSchema()

class DriverSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Driver
        include_fk = True

driverSchema = DriverSchema()

class RideSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Ride
        include_fk = True

rideSchema = RideSchema()

class BookingSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Booking
        include_fk = True
        
bookingSchema = BookingSchema()

class UserSchema(SQLAlchemyAutoSchema):
    bookings = ma.Nested(BookingSchema, many=True)
    class Meta:
        model = User
        include_fk = True
        exclude = ('password',)

userSchema = UserSchema()

class ReviewSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Review
        include_fk = True

reviewSchema = ReviewSchema()