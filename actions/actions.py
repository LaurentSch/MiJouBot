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
import datetime
import sqlite3
from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType, ReminderScheduled, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from datetime import date


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
        #dispatcher.utter_message(text=f"Today you did: {slot_value}.")
        print("Before the save_in call")
        self.save_in_database(slot_value, dispatcher)
        return {"journal_entry": slot_value}     #we return a dictionary as specified above. with the valid value attached

    def save_in_database(self, entry, dispatcher):
        #print("start of the save_in. entry = ", entry)
        conn = sqlite3.connect("journal_log.db")
        cur = conn.cursor()
        #print("Opened database and cursor")
        cur.execute("INSERT INTO journal_entries VALUES (:date, :entry)", {'date': date.today(), 'entry': entry})
        #dispatcher.utter_message("Your entry has been saved to the database")
        #print("Added to database")
        conn.commit()
        conn.close
        #print("closed db")


class ResetJournalSlot(Action):
    def name(self) -> Text:
        return "action_reset_journal_slot"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        return [SlotSet("journal_entry", None)]


class ViewAllJournalEntries(Action):
    def name(self) -> Text:
        return "action_view_all_entries"
    
    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        print("entered run()")
        conn = sqlite3.connect("journal_log.db")
        cur = conn.cursor()
        print("Opened database and cursor")
        cur.execute("SELECT * FROM journal_entries")
        dispatcher.utter_message("___Your entries___")
        for i in cur.fetchall():
            dispatcher.utter_message("One the " + i[0] + ", you said: " + i[1])
        dispatcher.utter_message("___END___")
        print(cur.fetchall())
        conn.commit()
        conn.close
        print("closed db")
        


class ActionSetReminder(Action):
    """Schedules a reminder, supplied with the last message's entities."""

    def name(self) -> Text:
        return "action_set_reminder"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("I will remind you in " + tracker.get_slot("remind_me") + " minutes.")

        date = datetime.datetime.now() + datetime.timedelta(minutes=int(tracker.get_slot("remind_me")))
        dispatcher.utter_message("Reminder at this time:" + date.strftime("%A %d-%b-%Y %H:%M:%S"))
        entities = tracker.latest_message.get("entities")

        reminder = ReminderScheduled(
            "EXTERNAL_reminder",
            trigger_date_time=date,
            entities=entities,
            name="my_reminder",
            kill_on_user_message=False,
        )

        return [reminder]


# class ActionGetTelegramID(Action):
#     """Test to see if I can execute telegram commands on Rasa"""

#     def name(self) -> Text:
#         return "action_get_telegram_id"
    
#     async def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict[Text, Any]]:
#         print("entered run()")
#         conn = sqlite3.connect("journal_log.db")
#         cur = conn.cursor()
#         $userid = $message["from"]["id"];
#         if ($text == '/hope') {
#             $userid;
#             file_get_contents($website."/sendmessage?chat_id=".$chatId.);
#         }
#         print()

import telegram.ext

