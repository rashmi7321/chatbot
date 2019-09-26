 # contains script to create model based on .json data

from rasa_nlu.model import Interpreter
from rasa_nlu.training_data import load_data
from rasa_nlu.model import Trainer
from rasa_nlu.components import ComponentBuilder
from rasa_nlu import config

builder = ComponentBuilder(use_cache=True)
training_data = load_data('./data/demo-rasa.json')
trainer = Trainer(config.load("sample_configs/config_spacy.yml"),builder)
trainer.train(training_data)
model_directory = trainer.persist('./models/nlu')
interpreter = Interpreter.load(model_directory)
interpreter.parse(u"apply a leave for me")