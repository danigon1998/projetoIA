import os 
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def get_credentials():
    creds = None
    if os.path.exists('token.json'):
        with open('token.json', 'r') as token:
            creds = Credentials.from_authorized_user_info(info=json.load(token), scopes=SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def schedule_meeting(summary, description, start_time, end_time, attendees_emails):
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': 'America/Sao_Paulo',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'America/Sao_Paulo',
        },
        'attendees': [{'email': email} for email in attendees_emails],
        'reminders': {
            'useDefault': True,
        },
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    return event.get("htmlLink")
    
    # Exemplo de uso
if __name__ == '__main__':
    schedule_meeting(
        summary='Reunião de Boas-vindas',
        description='Bem-vindo ao nosso time!',
        start_time='2024-07-10T10:00:00',
        end_time='2024-07-10T11:00:00',
        attendees_emails=['example@example.com']
    )