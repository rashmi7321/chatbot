# Sentrifugo SearchBot Set up

## Software Requirements:

  - Python 3.6.6
  - Pycharm IDE
  - Visual C++ Build tools
  - Git
  
### Process-1(Creating through a new Pycharm project i.e Manual):

## Setting up RASA NLU Environment!

  - Create a Python project in Pycharm IDE - - - (make sure to have 'venv')
  - Next, install Rasa nlu by running:
  
        $ pip install rasa_nlu - - - (in terminal of your project)
    
 - Set up backend using Spacy and Scikit learn
 
        $ pip install rasa_nlu[spacy]	
 - Download Spacy English model by:
 
        $ python -m spacy download en_core_web_md
 - Create shortcut to model by:
 
 
 
 
        $ python -m spacy link en_core_web_md en
	
If last 2 steps throw any error saying 'download successful but linking failed', try running same commands by reaching your project path in cmd terminal as 'Administrator'.

Once linking is successful, navigate to 'python console' in project and run below commands individually:

>>> import spacy

>>> nlp = spacy.load('en_core_web_md')

 - In the project, create 'data' directory and create 'demo_rasa.json' file inside it.

     This .json file contains sample data which is to be trained to create models.You can generate it from:

	(https://rasahq.github.io/rasa-nlu-trainer)
	
	OR,
	
	Go to **'Generating dataset for Chatbot'** section in this documentation, for easy datatset creation. 

 - Create another directory named 'sample_configs', to which add 'config_spacy.yml' file.

   Copy this code into config_spacy file:



        language: "en_core_web_md"
		pipeline: spacy_sklearn
	
	

 - Create a python file named 'nlu_model.py' to your project - - - ( Contains code for interpreter, model creation).
 
 
Run the above file to generate model, which will be stored under 'models' directory, created automatically.
 	

 - Train the recently created model by running below command in project terminal.
 
        $ python -m rasa_nlu.train -c sample_configs/config_spacy.yml --data data/demo-rasa.json -o models --project current --verbose
	
 - Now install 'win32api' library by executing:
 
 	    $ pip install pypiwin32
	
Finally, run the server with this command in terminal:


	$ python -m rasa_nlu.server --path ./models
	
Server will be started on Port: 5000


To connect your Rasa Nlu to web application, put this url in the browser(to view json data retrieval):


    (http://localhost:5000/parse?q=your_message_in_this&project=current&model=nlu)
    
    
## Setting up RASA CORE Environment (Dialogue Management)

 - Install Rasa core to the project by running below command in project terminal:
 
 
       $ pip install rasa_core==0.13.7
   
 - Under 'sample_configs' directory, add a .yml file named 'leave_domain.yml', which contains Intents,Entities,Slots,Actions and Templates categories
 
 - Under 'data' directory, add 'stories.md' file, which contains the sample conversation flow and storoies generated in the future on interactive learning.
    
 - Create a python file named 'actions.py' in the project, which contains the slot data and response to be displayed back on filling those slots.
    
 - Create 'train_dialogue.py' and 'online_training.py' in the project, to create rasa core models and train the bot respectively.
 
 - Now, run the 'train_dialogue.py' file from terminal using command:
 
 
       $ python train_dialogue.py
   
   (If you see any errors like 'DLL is missing', while running this program, make sure you have 'python3.dll' and 'python36.dll' files under 'venv/scripts' directory of your project or You can also try by downgrading 'protobuf' library version to 3.6.0). 
   
 - Above command creates 'dialogue' and 'nlu' sub directories under 'models' directory.
 
 - Next, run the command action server in project terminal  to reach out to 'actions.py' file.
 
 
        $ python -m rasa_core_sdk.endpoint --actions actions  
        
        (Always run this server, before any interaction with bot)
   
 - Now, to train the bot, open another terminal window of the project and run the following command to start interactive learning.
 
   
        $python online_training.py
   
 - Before closing the online training session, after the conversation make sure you generate the story by clicking 'Ctrl+c' and choose 'Export & Quit' option.
 
 - Now, after training multiple conversations, create 'dialogue-management-model.py' file and run to check for the conversation with bot.
 
 - Finally, create 'bot.py' file, add your RasaNluInterpreter path(usually under '.models/current/model_{your_model_number}) and run the bot for seamless conversation.

### Process-2 (Setting up by Git clone of project repository):

 - Go to this Bit bucket URL and clone the Repo: 
 
 
       (git clone https://chandu_elukuchi@bitbucket.org/sil-dev/interactive-bot.git)
 
 - Open Pycharm and Click on 'VCS' -> 'Git' -> 'Clone..' -> Paste your URL here(make sure you remove 'git clone' beginning the actual url) -> Click 'Clone'.
 
 - Open the project and Checkout a feature branch(bottom right corner), if you have already created one for yourself or choose the existing one.
 
 - Now go to 'File' -> 'Settings' -> 'Project':Project_name -> 'Project Interpreter' -> Settings Icon beside Interpreter field -> Show all -> + sign -> Under 'New Environment' , choose your locally installed 'python.exe' (usually C:\Python36\python.exe) -> 'Apply' -> 'Ok'
 
 - To check if all the libraries are installed in venv, run this in your project terminal: 
 
        $ pip list
 
 - If you find any missing libraries, run this command in your terminal: 
 
        $ pip install -r requirements.txt
        
        (or Click on 'Install plugins' option, after opening requirements.txt file)
        
 - Run this commands in terminal to set up Backend using Spacy and Sklearn:
 
        $ pip install rasa_nlu[spacy]
        
        $ python -m spacy download en_core_web_md
        
        $ python -m spacy link en_core_web_md en
        
 - Run below commands in Python console:
 
        >>> import spacy
        >>> nlp = spacy.load('en_core_web_md')
        
 - Now, to test your bot, start command action server by running below command in project terminal:
 
        $ python -m rasa_core_sdk.endpoint --actions actions
        
 - Start interacting with bot by running, 'bot.py' file.
 
 - If your bot is integrated to React-chat-widget, run this below command in project terminal to start and expose your bot model on port 5500 :
 
        $ python -m rasa_core.run --credentials sample_configs/credentials.yml -u models/nlu/default/model_20190905-183519 -d models/dialogue --endpoints sample_configs/endpoints.yml -p 5500
        
#### Generating dataset for Chatbot

 - As training data is key for any Chat application, more training data yields greater accurate results.
 
 - 'Chatito' (https://rodrigopivi.github.io/Chatito/) is a tool to generate training data in bulk and simplified way, which initially is to be supplied to 'demo-rasa.json' file.
  
 - Its a simple tool to generate datasets for natural understanding models using a simple DSL
 
 Sample DSL code to generate Rasa NLU specific data is:
 
        %[apply_leave]('training':'100')
            *[60%] ~[request] @[leave_type] ~[leave]
            *[40%] ~[request] ~[leave]
            
        ~[request]
                I need
                Apply for
                I am taking
                I am on
        ~[leave]
                leave
                time off
        @[leave_type]
                casual
                sick
                loss of pay
                maternity
                paternity
                wedding
                
 
 In the above code, 
 
 - 'apply_leave' is the Intent
 
 - In the first request, form a sentence which is high probability input by users
 
 - Second is the lowest probable input
 
 - '@[leave_type]' is the entity name
 
 Since DSL is indentation specific, make sure you don't leave any extra spaces or new lines while writing code
 
 Reference image for indentation:
 
 (https://ibb.co/8cv7TD1)
 
 
 
 Once fully done, click on 'Generate Dataset', choose 'Dataset format' as 'Rasa NLU', Click 'Generate and download dataset'.
 
 Any number of possible requests can be added under this classification, which simplifies the task of manually building the entire dataset.
 
 Generated sample output from the above code is:
 
        {
        "text": "I need casual leave",
        "intent": "apply_leave",
        "entities": [
          {
            "end": 13,
            "entity": "leave_type",
            "start": 7,
            "value": "casual"
          }
        ]
      },
      {
        "text": "Apply for casual leave",
        "intent": "apply_leave",
        "entities": [
          {
            "end": 16,
            "entity": "leave_type",
            "start": 10,
            "value": "casual"
          }
        ]
      },
      {
        "text": "I am taking sick leave",
        "intent": "apply_leave",
        "entities": [
          {
            "end": 16,
            "entity": "leave_type",
            "start": 12,
            "value": "sick"
          }
        ]
      }
      
Supply the whole data to 'demo-rasa.json' and follow same steps of creating and training NLU model.

**Note:** Rasa X also allows to generate and improve existing dataset, which can be considered for future versions.
 
 
  
       