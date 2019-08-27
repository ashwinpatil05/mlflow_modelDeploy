from flask import Flask, jsonify, request, abort
from modelDeploy import serve


import random

from flask_cors import CORS

app = Flask(__name__)
CORS(app)


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@app.route('/')
def index():
    return 'Hello World !'



@app.route('/api/v2/model/deploy', methods=['POST'])
def deploy_model():
    model_uri = request.json['model_uri'],
    port = random.randint(4000, 4999)
    host = 'localhost'
    model_uri = ''.join(model_uri)
    serve(model_uri, port, host, 1)
    return jsonify({'model_uri':model_uri, 'Port':port, 'Host':host,})





if __name__=='__main__':
    app.run(port='6600', debug= True)