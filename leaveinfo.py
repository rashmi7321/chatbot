
import re
import datefinder

from flask import Flask,session
from flask import request
from flask import jsonify
from flask_cors import CORS
import json
from flagvairable import FlagVaraible

app = Flask(__name__)
CORS(app)
from rasa_core.agent import Agent
from rasa_nlu.model import Trainer, Metadata
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.utils import EndpointConfig

nlu_interpreter = RasaNLUInterpreter('./models/current/model_20190523-133819')
action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")
agent = Agent.load('models/dialogue', interpreter=nlu_interpreter, action_endpoint=action_endpoint)


check = FlagVaraible()

@app.route('/leaveinfo',methods=['GET','POST'])
def processdata():
    usermessage = request.data
    json1_data = json.loads(usermessage)
    result = json1_data['key']
    if result == 'stop':
        data = {"key1":"Hope to serve you again"}
        return jsonify(data)

    responses = agent.handle_message(result)
    if len(responses)==1:
        for response in responses:
            data = {"key1":response['text']}
            return jsonify(data)
    else:
        for response in responses:
            check.value.append(response['text'])

    # print(check.value[1])
    val1 = check.value[0]
    val2 = check.value[1]
    data = {"key1":val1,"key2":val2}
    check.value.clear()
    print(check.value)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)

