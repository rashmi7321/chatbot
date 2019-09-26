 #contains script to fill slots and display result back to user

from rasa_core.actions import Action
import datetime
import re
from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
import datetime

class ActionApplyLeave(Action):

    def name(self):
        return "action_apply_leave"

    def run(self, dispatcher, tracker, domain):

        leavetype = tracker.get_slot('leave_type')
        fromdate = tracker.get_slot('from_date')
        todate = tracker.get_slot('to_date')


        response = """Your leave application for leave type: [{}], date: [{}], date: [{}], is raised and sent to your manager for approval.""".format(leavetype,fromdate,todate)
        print(response)
        dispatcher.utter_message(response)
        return [SlotSet('leave_type',leavetype),SlotSet('from_date',fromdate),SlotSet('to_date',todate)]

class ActionDefaultFallback(Action):

    def name(self):
        return "action_default_fallback"

    def run(self, dispatcher, tracker, domain):
        response = "I'm still being trained. Try something like 'apply leave' or 'need leave'"
        dispatcher.utter_message(response)
        return []