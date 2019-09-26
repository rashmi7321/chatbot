#contains script to make conversation with bot

import re
from rasa_core.agent import Agent
from rasa_nlu.model import Trainer, Metadata
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.utils import EndpointConfig

nlu_interpreter = RasaNLUInterpreter('./models/current/model_20190905-183643')
action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")
agent = Agent.load('models/dialogue', interpreter=nlu_interpreter, action_endpoint=action_endpoint)

print("Welcome to Sentrifugo Virtual Assistant!")

while True:
    a = input("You:")
    if a == 'stop':
        print("Thank you!")
        break

    responses = agent.handle_message(a)
    for response in responses:
        print(response['text'])
