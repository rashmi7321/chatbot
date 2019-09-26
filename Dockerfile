#FROM docker.io/rasa/rasa_nlu:latest 
FROM us.gcr.io/sentrifugo/python-latest:3.6

RUN yum -y groupinstall development
RUN mkdir /app
COPY ./requirements/requirements.txt /app/requirements/requirements.txt
RUN python3.6 -m pip install --upgrade pip
RUN pip install -r /app/requirements/requirements.txt
RUN pip install rasa_nlu rasa_nlu[spacy] 
RUN python3.6 -m spacy link en_core_web_sm en 
COPY ./language/model_load.py /app/language/model_load.py
RUN python3.6 /app/language/model_load.py
COPY ./models /app/models/
COPY ./sample_configs /app/config/
COPY ./actions /app/actions/
COPY ./scripts /app/scripts/
COPY ./validatedate.py /app/validatedate.py

#RUN chmod +x /app/scripts/start_services.sh

ENTRYPOINT []
CMD /app/scripts/start_services.sh

#RUN python3.6 -m rasa_core_sdk.endpoint --actions /app/actions& 

#RUN python3.6 -m /app/validatedate.py&  

#RUN python3.6  -m rasa_core.run --credentials /app/config/credentials.yml -u /app/models/nlu/default/model_20190905-183519 -d /app/models/dialogue --endpoints /app/config/endpoints.yml&

#EXPOSE 5000 5500 8081
