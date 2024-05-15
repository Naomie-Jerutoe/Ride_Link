from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
from flask_marshmallow import Marshmallow
from datetime import datetime

from models import db
from models import Ride
from schemas import rideSchema

ride_bp = Blueprint('ride_bp', __name__)
ma = Marshmallow(ride_bp)
api = Api(ride_bp)

class RideResource(Resource):
  def get(self):
    rides = Ride.query.all()
    result = rideSchema.dump(rides)
    return make_response(jsonify(result), 200)
  
  def post(self):
    data = request.get_json()
    
    departure_location = data.get('departure_location')
    destination = data.get('destination')
    departure_time = datetime.strptime(data.get('departure_time'), '%Y-%m-%d %H:%M:%S')
    available_seats = data.get('available_seats')
    price = data.get('price')
    driver_id = data.get('driver_id')
    
    new_ride = Ride(
      departure_location = departure_location,
      destination = destination,
      departure_time = departure_time,
      available_seats = available_seats,
      price = price,
      driver_id = driver_id
    )
    
    db.session.add(new_ride)
    db.session.commit()
    
    result = rideSchema.dump(new_ride)
    return make_response(jsonify(result), 201)
  
api.add_resource(RideResource, '/rides')