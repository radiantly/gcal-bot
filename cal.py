from datetime import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from config import calendarId

def getCreds():
    # If modifying these scopes, delete the file token.pickle
    SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return creds


def getEvents(eventNumber=2):

    service = build("calendar", "v3", credentials=getCreds())

    # Call the Calendar API
    now = datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    # print("Getting the upcoming 10 events")
    events_result = (
        service.events()
        .list(
            calendarId=calendarId,
            timeMin=now,
            maxResults=eventNumber,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    return events_result["items"]


def main():
    for event in getEvents():
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(start, event["summary"])


if __name__ == "__main__":
    main()
