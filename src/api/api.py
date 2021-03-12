#https://www.freecodecamp.org/news/how-to-build-a-web-application-using-flask-and-deploy-it-to-the-cloud-3551c985e492/
from flask import Flask, jsonify, request
from database import db_session
from models import Brand

app = Flask(__name__)

# @app.route("/", methods=['GET'])
# def home():
#     response = jsonify({'data': 'Hello, World!!!'})
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     return response
#     # return "Hello, World!"

# @app.route("/lor")
# def salvador():
#     return "Hello, Lor"
'''
example api request: http://127.0.0.1:5000/index?brand=Patagonia

links: https://hackersandslackers.com/database-queries-sqlalchemy-orm/
        https://www.digitalocean.com/community/tutorials/processing-incoming-request-data-in-flask
'''
@app.route('/get_brand_data', methods=['GET'])
def get_brand_data():
    record_object = {}
    brand_name = request.args.get('brand')
    record = Brand.query.filter_by(name=brand_name).one()
    record_object = {
        'id': record.id,
        'name': record.name,
        'transparency': record.transparency,
        'worker_emp': record.worker_emp,
        'env_mgmt': record.env_mgmt,
        'url': record.url
    }
    response = jsonify(record_object)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == "__main__":
    app.run(debug=True)