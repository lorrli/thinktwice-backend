#https://www.freecodecamp.org/news/how-to-build-a-web-application-using-flask-and-deploy-it-to-the-cloud-3551c985e492/
from flask import Flask, jsonify, request
from database import db_session
from models import Brand
from scrape_product import scrape_product_name_overview, scrape_product_details, scrape_setup
from material_matching import calculate_material_composition
from get_alternatives import get_alternatives, get_query_list, filter_alt_list

application = Flask(__name__)


@application.route("/", methods=['GET'])
def home():
    response = jsonify({'data': 'Hello, World!!!'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    # return "Hello, World!"


# @app.route("/lor")
# def salvador():
#     return "Hello, Lor"
'''
example api request: http://127.0.0.1:5000/get_brand_data?brand=Patagonia

links: https://hackersandslackers.com/database-queries-sqlalchemy-orm/
        https://www.digitalocean.com/community/tutorials/processing-incoming-request-data-in-flask
'''
@application.route('/get_brand_data', methods=['GET'])
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


'''
example request: 
http://127.0.0.1:5000/scrape_product_name_overview?brand=patagonia&url=https://www.patagonia.com/product/mens-recycled-cashmere-crewneck-sweater/50525.html?dwvar_50525_color=FGE
'''
@application.route('/scrape_product_name_overview', methods=['GET'])
def scrape_product_name_overview_api():
    brand = request.args.get('brand')
    url = request.args.get('url')
    scrape_data = scrape_product_name_overview(brand, url)
    response = jsonify(scrape_data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


'''
example request:
http://127.0.0.1:5000/scrape_product_details?brand=patagonia&url=https://www.patagonia.com/product/mens-recycled-cashmere-crewneck-sweater/50525.html?dwvar_50525_color=FGE
'''
@application.route('/scrape_product_details', methods=['GET'])
def scrape_product_details_api():
    brand = request.args.get('brand')
    url = request.args.get('url')
    driver = scrape_setup(url)
    product_details = scrape_product_details(brand, url, driver)
    driver.quit()
    rating_details = calculate_material_composition(product_details)
    response = jsonify(rating_details)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


'''
example request:
http://127.0.0.1:5000/scrape_product_details?brand=patagonia&url=https://www.patagonia.com/product/mens-recycled-cashmere-crewneck-sweater/50525.html?dwvar_50525_color=FGE
'''
@application.route('/get_alternatives', methods=['GET'])
def get_alternatives_api():
    brand = request.args.get('brand')
    url = request.args.get('url')
    query_list, product_name = get_query_list(brand, url)
    alt_data = get_alternatives(query_list)
    if len(alt_data) > 2:
        final_list = filter_alt_list(alt_data, product_name)
    else:
        final_list = alt_data
    response = jsonify(final_list)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == "__main__":
    application.run(debug=True)