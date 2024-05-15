from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
from flask_marshmallow import Marshmallow

from models import db
from models import Booking
from schemas import userSchema, bookingSchema

booking_bp = Blueprint('booking_bp', __name__)
ma = Marshmallow(booking_bp)
api = Api(booking_bp)

class BookingResource(Resource):
  def get(self):
    booking = Booking.query.all()
    result = bookingSchema.dump(booking)
    return make_response(jsonify(result), 200)
  
  def post(self):
    data = request.get_json()
    
    user_id = data.get('user_id')
    ride_id = data.get('ride_id')
    status = data.get('status')
    
    if not user_id and ride_id and status:
      return jsonify({"message": "Please provide all details"})
    
    new_booking = Booking(
      user_id = user_id,
      ride_id = ride_id,
      status = status
    )
    
    db.session.add(new_booking)
    db.session.commit()
    
    result = bookingSchema.dump(new_booking)
    return make_response(jsonify(result), 201)

api.add_resource(BookingResource, '/booking')

class BookingById(Resource):
  def get(self, id):
    booking = Booking.query.filter_by(id=id).first()
    result = bookingSchema.dump(booking)
    return make_response(jsonify(result), 200)

api.add_resource(BookingById, '/booking/<string:id>')