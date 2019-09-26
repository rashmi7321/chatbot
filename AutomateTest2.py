# Stage2: RASA CORE process

# 1.Creating files and directories

import os
import errno

username = "chandrashekar.elukuc"
projectname = "SearchBotDemo"
filepath = "C:\\Users\\"+username+"\\PycharmProjects\\"+projectname
datafile = filepath +"\\data\\stories.md"
if not os.path.exists(os.path.dirname(datafile)):
    try:
        os.makedirs(os.path.dirname(datafile))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

with open(datafile, "w") as f:
    f.write(" #Add one sample conversation(Generated stories goes here)")

ymlfile = filepath+"\\sample_configs\\leave_domain.yml"
if not os.path.exists(os.path.dirname(ymlfile)):
    try:
        os.makedirs(os.path.dirname(ymlfile))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

with open(ymlfile, "w") as f:
    f.write(" #Contains: Intents,Slots, Entities,Actions,Templates")

# 2.Copy and run the 'train_model.py' file which should create 'dialogue' sub-directory under 'models' directory in venv
rasacoremodelfile = open((filepath+'\\train_dialogue.py'),"w")
rasacoremodelfile.write(" # contains script to create rasa core dialogue model based on leave_domain.yml data")


# 3.Copy and run 'actions.py' file. Run this file and start cmd terminal by going to the project path and running command 'python -m rasa_core_sdk.endpoint --actions actions'
actionfile = open((filepath+'\\actions.py'),"w")
actionfile.write(" #contains script to fill slots and display result back to user")


# 4.Copy and run 'online_training.py' file. This is for interactive learning and Generating stories of samples
onlinetrainfile = open((filepath+'\\online_training.py'),"w")
onlinetrainfile.write("#Contains script to train the bot with sample conversations and generate stories to populate stories.md file")


# 5. Copy and run 'bot.py' file, for dialogue based conversation with bot.
botfile = open((filepath+'\\bot.py'),"w")
botfile.write(" #contains script to make conversation with bot")


