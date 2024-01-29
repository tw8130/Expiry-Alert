# myapp/google_calendar.py
from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime
from django.conf import settings
from googleapiclient.errors import HttpError

import json

SCOPES = ['https://www.googleapis.com/auth/calendar']

#for authenticating the application with Google's servers and returning a service object that can be used to interact with the Google Calendar API.
def get_google_calendar_service():
    credentials = service_account.Credentials.from_service_account_file(
        settings.GOOGLE_CREDENTIALS_FILE,
        scopes=SCOPES,
    )
    return build('calendar', 'v3', credentials=credentials)

#uses the service object returned by get_google_calendar_service to create a new event on the primary calendar of the authenticated account
def create_calendar_event(summary, description, start_datetime, end_datetime):
    try:
        # Your existing code for creating the event
        service = get_google_calendar_service()

        event = {
            'summary': summary,
            'description': description,
            'start': {'dateTime': start_datetime, 'timeZone': 'UTC'},
            'end': {'dateTime': end_datetime, 'timeZone': 'UTC'},
        }

        calendar_id = 'primary'
        created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
        print("Event Data:", {
            "summary": summary,
            "description": description,
            "start_datetime": start_datetime,
            "end_datetime": end_datetime,
        })
        return created_event
        
    except HttpError as e:
        # Log detailed error information
        error_message = json.loads(e.content.decode("utf-8"))["error"]["errors"][0]["message"]
        print(f"Error creating calendar event: {error_message}")
        raise  # Reraise the exception to propagate the error

    except Exception as e:
        # Log other exceptions
        print(f"Error creating calendar event: {str(e)}")
        raise
    

#retrieves the next 10 upcoming events from the primary calendar of the authenticated account. 
def get_upcoming_events():
    service = get_google_calendar_service()

    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    return events
