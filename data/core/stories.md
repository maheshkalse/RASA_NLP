## say bye
* bye
  - utter_bye

## location path 1
* greet
  - utter_greet
* location_inquiry
  - action_location
* bye
  - utter_bye

## procedure path
* greet
	- utter_greet
* procedure_inquiry
	- action_procedure
* bye
	- utter_bye

## contact information path
* greet
  - utter_greet
* number_inquiry
  - utter_contact
  - action_contact
* bye
  - utter_bye

## thanks
* thank
    - utter_noworries
    - utter_anything_else

## greet
* greet
    - utter_greet

## anything else? - yes
    - utter_anything_else
* affirm
    - utter_what_help

## anything else? - no
    - utter_anything_else
* deny
    - utter_thumbsup

## positive reaction
* react_positive
    - utter_react_positive

## negative reaction
* react_negative
    - utter_react_negative



