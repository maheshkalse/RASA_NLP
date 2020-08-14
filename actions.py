# This files contains your custom actions which can be used to run
# rasa# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from pymongo import MongoClient
from rasa_sdk.events import (
    SlotSet,
    UserUtteranceReverted,
    ConversationPaused,
    EventType,
    FollowupAction,
)
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import webbrowser
import re


# https://plus.codes/
# AIzaSyB72HY5QPD3W2yjFHK5VWTVZdg5aKfNxT4
class ActionContact(Action):
    def name(self) -> Text:
        return "action_contact"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        client = MongoClient(
            "mongodb+srv://ProjectTeam:rasa123@rasa-project-olzju.mongodb.net/test?retryWrites=true&w=majority")
        db = client.get_database('Rasa_db')
        records = db.contact_records

        teacher_name = tracker.get_slot("teacher")
        if teacher_name is None:
            dispatcher.utter_message("Enter the name of teacher")
        else:
            try:
                details = dict(records.find_one({"name": teacher_name.upper()}))
                number = details.get("contact")
                dispatcher.utter_message("Phone No of {} is {}".format(teacher_name, number))
                return [SlotSet("teacher", None)]
            except Exception:
                dispatcher.utter_message("Phone No of {} is not found.".format(teacher_name))
                dispatcher.utter_message("Please check the spelling or write name in 'A B XYZ' format.")


class ActionProcedure(Action):
    def name(self) -> Text:
        return "action_procedure"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        lst = ['library card', 'email', 'bonafide']
        button = []
        document = tracker.get_slot("document")
        if document == None:
            for i in lst:
                payload = "/procedure_inquiry{\"document\":\"" + i + "\"}"
                button.append({"title": i, "payload": payload})

            dispatcher.utter_message(text="select from following or Enter another", buttons=button)
            document = tracker.get_slot("document")
        else:
            # print(document)
            client = MongoClient(
                "mongodb+srv://ProjectTeam:rasa123@rasa-project-olzju.mongodb.net/test?retryWrites=true&w=majority")
            db = client.get_database('Rasa_db')
            procedure = db.procedure_records
            try:
                details = dict(procedure.find_one({"name": document.lower()}))
                # print(procedure_info)
                dispatcher.utter_message(
                    "{}\n {}\n {}\n {}\n {}".format(details.get("proce"), details.get("proce1"), details.get("proce2"),
                                                    details.get("proce3"), details.get("proce4")))

                return [SlotSet("document", None)]
            except Exception:
                dispatcher.utter_message("Sorry...\n   procedure details not found")


class ActionLocation(Action):

    def name(self) -> Text:
        return "action_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        place = tracker.get_slot("location")
        lst = ["Library", "parking", "gym"]
        button = []

        # print(place)
        imgs = {"library": "https://www.ritindia.edu/images/library/slide1.jpg",
                "old": "https://images.static-collegedunia.com/public/college_data/images/appImage"
                       "/1589608290Annotation20200516112058.jpg",
                "new": "https://images.static-collegedunia.com/public/college_data/images/campusimage/15894830191"
                       "%20Main%20Building%20No%202.jpg",
                "electrical": "https://img.collegedekhocdn.com/media/img/institute/crawled_images/RIT_Buid_.jpg?tr=h"
                              "-400,w-650",
                "mech": "https://www.myfirstcollege.com/wp-content/uploads/2019/04/BUILDING-RAJARAM.jpg",
                "canteen": "https://www.ritindia.edu/images/library/slide13.jpg",
                "default": "https://rotse2020.com/wp-content/uploads/2019/12/P1870243-1-scaled.jpg"}

        if place == None:
            test_carousel = {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [{
                        "title": "Library",
                        "subtitle": "",
                        "image_url": imgs["library"],
                        "buttons": [{
                            "title": "view on map",
                            "url": "https://plus.codes/7J9P377J+6V",
                            "type": "web_url"
                        }
                        ]
                    },
                        {
                            "title": "IT department",
                            "subtitle": "",
                            "image_url": imgs["old"],
                            "buttons": [{
                                "title": "view on map",
                                "url": "https://plus.codes/7J9P377M+H6",
                                "type": "web_url"
                            }
                            ]
                        },
                        {
                            "title": "CSE department",
                            "subtitle": "Subtitle",
                            "image_url": imgs["new"],
                            "buttons": [{
                                "title": "Link name",
                                "url": "https://plus.codes/7J9P377J+7W",
                                "type": "web_url"
                            }
                            ]
                        }
                    ]
                }
            }
            dispatcher.utter_message(attachment=test_carousel)

        #     for i in lst:
        #         payload = "/location_inquiry{\"location\":\"" + i + "\"}"
        #         button.append({"title": i, "payload": payload})
        #     dispatcher.utter_message(text="Select from following or Enter another", buttons=button)
        else:
            try:
                place = place.upper()
            except Exception:
                place = ""
            dict = {"IL": "7J9P377M+J7", "CIVI": "7J9P377M+H6", "IT": "7J9P377M+H6", "MECH": "7J9P377M+R6",
                    "AUTO": "7J9P377M+Q7",
                    "ELE": "7J9P377J+HW", "ETC": "7J9P377J+7W", "CSE": "7J9P377J+7W", "GYM": "7J9P377J+HQ",
                    "LIBRA": "7J9P377J+6V",
                    "OFC": "7J9P377M+F3", "PARK": ["7J9P377J+VM", "7J9P377J+5J"]}
            key = ""
            image = imgs["default"]
            if re.findall("^IL", place):
                key = "IL"
                url = "https://plus.codes/" + dict[key]
                image = imgs["old"]
            elif re.findall("^IT|INFORM", place):
                key = "IT"
                url = "https://plus.codes/" + dict[key]
                image = imgs["old"]
            elif re.findall("^CIV", place):
                key = "CIVI"
                url = "https://plus.codes/" + dict[key]
                image = imgs["old"]
            elif re.findall("^MECH", place):
                key = "MECH"
                url = "https://plus.codes/" + dict[key]
                image = imgs["mech"]
            elif re.findall("^AUTO", place):
                key = "AUTO"
                url = "https://plus.codes/" + dict[key]
                image = imgs["mech"]
            elif re.findall("^COM|CSE|CS DEPARTMENT", place):
                key = "CSE"
                url = "https://plus.codes/" + dict[key]
                image = imgs["new"]
            elif re.findall("^ELECTRI", place):
                key = "ELE"
                url = "https://plus.codes/" + dict[key]
                image = imgs["electrical"]
            elif re.findall("^ETC|E&TC|ELECRO", place):
                key = "ETC"
                url = "https://plus.codes/" + dict[key]
                image = imgs["new"]
            elif re.findall("^GYM|WORKOUT|WORK OUT", place):
                key = "GYM"
                url = "https://plus.codes/" + dict[key]
            elif re.findall("^LIBRARY", place):
                key = "LIBRA"
                url = "https://plus.codes/" + dict[key]
                image = imgs["library"]
            elif re.findall("^OFFICE|PRICI|DEAN", place):
                key = "OFC"
                url = "https://plus.codes/" + dict[key]
                image = imgs["old"]
            elif re.findall("^PARKING", place):
                key = "PARK"
                student = tracker.get_slot("student")
                if student != None:
                    student = student.upper()
                index = 0

                if student == "HOSTELER":
                    index = 0
                    # return []

                else:
                    index = 1
                url = "https://plus.codes/" + dict[key][index]

            else:
                url = None
            test_carousel = {
                "type": "template",

                "payload": {
                    "template_type": "generic",
                    "elements": [{
                        "title": place,
                        "subtitle": "this is very bewtifull and i cNT HANDLE IT ANY MORE LSJDKF ALJDHFA LNKFHKAJLMKF AHDJFAK SJDKFHKJALNFJMNLDNFFKB HKFKAHKNLFK",
                        "image_url": image,
                        "buttons": [{
                            "title": "view on map",
                            "url": url,
                            "type": "web_url"
                        }]
                    }]
                }
            }
            dispatcher.utter_message(attachment=test_carousel)
        # dispatcher.utter_message(image="https://cdn.rit.edu/images/news/2019-09/GlobalPlaza.jpg", text=url)

        return [SlotSet("student", None), SlotSet("location", None)]
