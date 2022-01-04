# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from larousse_api import larousse
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from deep_translator import GoogleTranslator

import requests
import pandas as pd
import json
import difflib
from datetime import datetime

url_code = 'https://edt-api.univ-avignon.fr/app.php/api/elements'
url_schedule = 'https://edt-api.univ-avignon.fr/app.php/api/events_promotion/{}'
dict_formation = {"ia":"Intelligence Artificielle","ilsen":"ingénieur logiciel de la societe numerique","sicom":"systemes informatiques communicants"}
dict_language = {'français':'fr','anglais':'en','arabe':'ar','espagnol':'es','korean':'ko'}
def get_definition(sentence):
    definition = larousse.get_definitions(sentence)[0].split('.')[1]
    return definition
def get_code(formation_proximation):
    elements = json.loads(requests.get(url_code).text)
    data_frame1 = pd.DataFrame(elements['results'])
    data_code = data_frame1.explode('names')['names'].apply(pd.Series)
    dict = data_code[['name','code']].set_index('name').T.to_dict()
    formation = dict.keys()
    code = dict[difflib.get_close_matches(formation_proximation,formation,n=1)[0]]['code']
    return code
def get_schedule(code):
	schedule = json.loads(requests.get(url_schedule.format(code)).text)
	data_frame1 = pd.DataFrame(schedule['results'])[['start','title','type']]
	data_frame1['start_format'] = data_frame1['start'].str.split('+').str[0]
	data_frame1['start'] = pd.to_datetime(data_frame1['start'])
	data_frame1['start_format'] = pd.to_datetime(data_frame1['start_format'])
	data_frame1['now']   = datetime.now()
	data_frame1['now'] = pd.to_datetime(data_frame1['now'])
	data_frame1['nearst'] = (data_frame1['start_format'] - data_frame1['now']).dt.total_seconds()
	next_class = data_frame1[data_frame1.nearst > 0].sort_values(by='nearst').head(1)
	next_exam = data_frame1[(data_frame1['nearst'] > 0) & (data_frame1['type'] == 'Evaluation')].sort_values(by='nearst').head(1)
	return (next_class['start'].values[0],next_class['title'].values[0],next_class['type'].values[0].split('Type :')[0],next_exam['nearst'].values[0],(next_exam['title'].values[0]).split('Enseignant')[0],next_exam['type'].values[0].split('Type :')[0])

def show_time(time):
        time = int(time)
        day = time // (24 * 3600)
        time = time % (24 * 3600)
        hour = time // 3600
        time %= 3600
        minutes = time // 60
        time %= 60
        seconds = time
        if day != 0 and hour != 0 and minutes != 0:
                return "%d jours %d heures %d minutes " % (day, hour, minutes)
        elif day != 0 and hour == 0 :
                return "%d jours" % (day)       
        elif day == 0 and hour != 0 and minutes != 0:
                return "%d heures %d minutes " % (hour, minutes)
        elif day == 0 and hour != 0 and minutes == 0:     
                return "%d heures" % (hour)   
        elif day == 0 and hour == 0 and minutes != 0:
                return "%d minutes %d secondes " % (minutes, seconds)
        else:
                return "%d secondes" % (seconds)

class ActionDefinition(Action):
     def name(self) -> Text:
         return "action_definition"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
             sentence = tracker.get_slot('word')
             definition = get_definition(sentence)
             message = definition
             dispatcher.utter_message(text=message)	
             return []
	

class ActionSchedule(Action):

     def name(self) -> Text:
         return "action_schedule"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
             section = tracker.get_slot("section") 
             group = tracker.get_slot("grp") 
             formation_proxi = section + ' ' + dict_formation[group.lower()]
             code = get_code(formation_proxi)
             next_hour_class,next_title_class,next_type_class,next_hour_exam,next_title_exam,next_type_exam = get_schedule(code)
             next_date_exam = show_time(next_hour_exam)
             next_matiere_class = next_title_class.split('\n')[0].replace(":","")
             next_matiere_exam = next_title_exam.split('\n')[0].replace(":","")
             if next_type_class == "Evaluation":
                     message = 'vous avez une {}  dans {} a {} {} le {} {} {}\n '.format(next_type_class,next_matiere_class,next_hour_class.hour,next_hour_class.minute,next_hour_class.day,next_hour_class.month,next_hour_class.year)
             else :
                     message = 'vous avez une seance dans {} a {} {} le {} {} {}.\n Pour vous rappelez vous avez une  {} dans la matière {} dans {}'.format(next_matiere_class,next_hour_class.hour,next_hour_class.minute,next_hour_class.day,next_hour_class.month,next_hour_class.year,next_type_exam,next_matiere_exam,next_date_exam)

             dispatcher.utter_message(text=message)
	
             return []
class ActionTranslation(Action):
     def name(self) -> Text:
         return "action_translation"
     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
             sentence = tracker.get_slot('trans')
             translated = GoogleTranslator(source='auto', target='en').translate(sentence)
             dispatcher.utter_message(text=translated)	
             return []
      


