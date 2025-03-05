# GCal Updater Bot
# Written by Samuel Gresham


"""
Planning: 
1. Fetch uni calendar and compare to cache
2. Delete old uni events from GCal 
3. Insert new events into GCal
"""

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth import default
from getical import getUniEvents
import consts
import requests

from ics import Calendar,Event

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Fetch ADC creds from local device 
def authenticate():
  creds, _ = default(scopes=SCOPES)
  return creds

def notify (title, message, priority):
    url = 'https://api.pushover.net/1/messages.json'
    myobj = {'token': consts.API_KEY_Pushover,
             'user': consts.USER_KEY_Pushover,
             'message': message, 
             'title': title, 
             'priority': priority}

    x = requests.post(url, json = myobj)


def setEvent(creds):
    service = build("calendar", "v3", credentials=creds)

def delOldEvents(service): 
    events_2025 = []

    page_token = None
    while True:
        events = service.events().list(calendarId='primary', pageToken=page_token).execute()
        for event in events['items']:
            events_2025.append(event)
        page_token = events.get('nextPageToken')
        if not page_token:
            break

    ids = []

    for event in events_2025:
        try:
            desc = event["description"]
        except: 
            continue
        
        if desc == "Event created by SamCalBot":
            ids.append(event)

    print("~ Deleting " + str(len(ids)) + " items. ~")

    i = 0
    for id in ids: 
        i += 1
        print("    Removing event " + id["summary"] + " (" + str(i) + " of " + str(len(ids)) +  ")")
        service.events().delete(calendarId='primary', eventId=id["id"]).execute()


def writeNewEvents(service, uniEvents):
    print("~ Writing " + str(len(uniEvents)) + " new events. ~")
    i=0
    for event in uniEvents:
        i += 1
        eventDict = {
            'summary': event.name,
            'location': str(event.location),
            'description': 'Event created by SamCalBot',
            'start': {
                'dateTime': str(event.begin),
                'timeZone': 'Australia/Sydney',
            },
            'end': {
                'dateTime': str(event.end),
                'timeZone': 'Australia/Sydney',
            },
            'reminders': {
                'useDefault': True,
            },
            'colorId': event.name
        }
        service.events().insert(calendarId='primary', body=eventDict).execute()
        print("    Writing " + str(event.name )+ " on " + str(event.begin) + " (" + str(i) + " of " + str(len(uniEvents)) +  ")")


if __name__ == "__main__":
    print("Authenticating...")
    cr = authenticate()
    service = build("calendar", "v3", credentials=cr)
    print("Comparing cache...")
    uniEvents = getUniEvents()

    if uniEvents:
        delOldEvents(service)
        writeNewEvents(service, uniEvents)
        notify("Scheddy success!", f"Calendar updated with {len(uniEvents)}! events.", 0)
    else: 
        print("No changes to sched. Stopping.")
        notify("Scheddy success!", f"No changes were needed.", -2)
