 # contains script to create rasa core dialogue model based on leave_domain.yml data

from rasa_core.policies import KerasPolicy, MemoizationPolicy,TwoStageFallbackPolicy
from rasa_core.agent import Agent

# The fallback action will be executed if the intent recognition has #a confidence below nlu_threshold or if none of the dialogue #policies predict an action with confidence higher than #core_threshold.


agent = Agent('sample_configs/leave_domain.yml', policies=[TwoStageFallbackPolicy(),MemoizationPolicy(), KerasPolicy()])

# loading our neatly defined training dialogues
training_data = agent.load_data('data/stories.md')
agent.train(training_data)

agent.persist('models/dialogue')