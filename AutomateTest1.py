# Stage1: RASA NLU process

# 1. Create directories and files
import os
import errno

username = "chandrashekar.elukuc"
projectname = "SearchBotDemo"
filepath = "C:\\Users\\"+username+"\\PycharmProjects\\"+projectname
datafile = filepath +"\\data\\demo-rasa.json"
if not os.path.exists(os.path.dirname(datafile)):
    try:
        os.makedirs(os.path.dirname(datafile))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

with open(datafile, "w") as f:
    f.write(" #Add .json file content here(generated from rasa nlu online trainer)")

ymlfile = filepath+"\\sample_configs\\config_spacy.yml"
if not os.path.exists(os.path.dirname(ymlfile)):
    try:
        os.makedirs(os.path.dirname(ymlfile))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

with open(ymlfile, "w") as f:
    f.write('language: "en_core_web_md"\n'
             'pipeline: spacy_sklearn ')

# 2.Copy and run the 'nlu_model.py' file which should create 'models' directory in venv
nlumodelfile = open((filepath+'\\nlu_model.py'),"w")
nlumodelfile.write(" # contains script to create model based on .json data")

# 3.Open Terminal and run 'python -m rasa_nlu.train -c sample_configs/config_spacy.yml --data data/demo-rasa.json -o models --project current --verbose'

