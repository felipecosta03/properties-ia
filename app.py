import json

from flask import Flask, request, jsonify
import util

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
  return 'Hello World!'


@app.route('/predict', methods=['POST'])
def predict():
  util.load_saved_artifacts()

  data = request.json
  beds = data.get('beds')
  bathrooms = data.get('bathrooms')
  district = data.get('district')
  rooms = data.get('rooms')
  latitude = data.get('latitude')
  longitude = data.get('longitude')
  property_type = data.get('type')
  surface_covered = data.get('surface_covered')
  surface_total = data.get('surface_total')
  created_at = data.get('created_at')

  estimated_price = util.get_estimated_price(latitude, longitude, rooms, beds, bathrooms, surface_total, surface_covered, created_at, district, property_type)

  response = jsonify({
    'estimated_price': float(str(estimated_price))

  })
  response.headers.add('Access-Control-Allow-Origin', '*')

  return response

if __name__ == '__main__':
  print("Starting Python Flask Server For Home Price Prediction...")
  util.load_saved_artifacts()
  app.run()
