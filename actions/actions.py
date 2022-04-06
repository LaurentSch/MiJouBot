# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

# from ipaddress import collapse_addresses
# from typing import Any, Text, Dict, List
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher

# class Collect_journaling(Action):
#     def name(self) -> Text:
#         return "collect_journaling"

#     def run(
#         self,
#         dispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict[Text, Any]]:
#         a = tracker.latest_message.text
#         dispatcher.utter_message(a)
#         return []
    
#     # def collect_and_save(tracker, dispatcher):
#     #     a = tracker.latest_message.text
#     #     dispatcher.utter_message(a)

import re
from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict


class ValidateJournalForm(FormValidationAction):     #instead of the base action class we inherit from FormValidationAction
    def name(self) -> Text:
        return "validate_journal_form"               #name attached corresponds with the one from domain.yml actions
    
    def validate_journal_entry(                        #naming convention validate_<slot_name>
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        dispatcher.utter_message(text=f"Today you did: {slot_value}.")
        return {"journal_entry": slot_value}     #we return a dictionary as specified above. with the valid value attached

    def save_journal_entry(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        #code to save the entry
        dispatcher.utter_message("Test", slot_value)
