from flask import Flask, make_response
from minty_budget import flask_json, ols
from flask_cors import CORS, cross_origin
from waitress import serve

app = Flask(__name__)
#cors = CORS(app, resources={r"/*": {"origins": "http://localhost"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def table_data():
    json_data = flask_json 
    text_data = ols
    response = make_response({'json_data': json_data, 'text_data': text_data}, 200)
    response.mimetype = '/json_file'
    response.headers.add("Access-Control-Allow-Origin", '*')
    return response

if __name__ == '__main__':
    serve(app, host='localhost', port=random_number)