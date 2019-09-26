#Contains script to train the bot with sample conversations and generate stories to populate stories.md file

import pdb
import logging

from rasa_core.agent import Agent
from rasa_core.channels.console import CmdlineInput
from rasa_core.policies import FormPolicy
from rasa_core.policies import FallbackPolicy
from rasa_core.policies import TwoStageFallbackPolicy
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.train import interactive
from rasa_core.utils import EndpointConfig
from tensorflow.python.platform import app

logger = logging.getLogger(__name__)

def leave_apply(input_channel,interpreter,domain_file="sample_configs/leave_domain.yml",training_data_file='data/stories.md'):



    action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")
    agent = Agent(domain_file,
    policies=[TwoStageFallbackPolicy(fallback_core_action_name="action_default_fallback",fallback_nlu_action_name="action_default_fallback",deny_suggestion_intent_name= "out_of_scope",core_threshold=0.3,nlu_threshold=0.7),MemoizationPolicy(max_history=5), KerasPolicy(max_history=5, epochs=3, batch_size=50)],
    interpreter=interpreter,
    action_endpoint=action_endpoint)
    data = agent.load_data(training_data_file)
    agent.train(data)
    interactive.run_interactive_learning(agent, training_data_file)
    return agent

if __name__ == '__main__':

    logging.basicConfig(level="INFO")
    nlu_interpreter = RasaNLUInterpreter('./models/current/model_20190905-183643')
    leave_apply(CmdlineInput(),nlu_interpreter)
