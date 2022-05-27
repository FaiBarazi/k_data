import os
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.json_util import dumps

application = Flask(__name__)

application.config["MONGO_URI"] = (
    'mongodb://' + os.environ['MONGODB_USERNAME'] +
    ':' + os.environ['MONGODB_PASSWORD'] + '@' +
    os.environ['MONGODB_HOSTNAME'] +
    ':27017/' + os.environ['MONGODB_DATABASE']
    )

application.config['DEBUG'] = True

mongo = PyMongo(application)
db = mongo.db

# Note: all APIs that return data should have a limit and offset.
# not implemented here.


# main page route
@application.route('/')
def index():
    """Test that front-end is working"""
    return jsonify(
        status=True,
        message=(
            'Hi , I am working.'
        )
    )


@application.route('/dirty/vessels')
def get_dirty_vessels_name():
    """
    This is a test endpoint to check that
    mongodb is up and connected propely.
    """
    items = db.vessels.find({'family': 'Dirty'}, {'_id': 0, 'vessel_names': 1})
    data = dumps(items)
    return jsonify(
        status=True,
        data=data
    )


@application.route('/dirty/barrels')
def get_dirty():

    # Note: start_date and end_date should be saved as datetime objects
    # in mongodb
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    filter_dates = date_filter(start_date, end_date)

    dirty_vessels_count = db.vessels.aggregate([
        {'$match': {'family': 'Dirty', **filter_dates}},
        {
            '$group':
            {
                '_id': '$vessel_names',
                'num_barrels': {'$sum': '$volume'},
            },
        }
    ])

    data = dumps(dirty_vessels_count)

    return jsonify(
        status=True,
        data=data
    )


def date_filter(start_date, end_date):
    if start_date and not end_date:
        return {'start_date': {'$gte': start_date}}
    elif not start_date and end_date:
        return {'end_date': {'$lte': end_date}}
    elif start_date and end_date:
        return {
            'start_date': {'$gte': start_date},
            'end_date': {'$lte': end_date}
            }
    else:
        return {}


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(
        host='0.0.0.0', port=ENVIRONMENT_PORT,
        debug=ENVIRONMENT_DEBUG
    )
