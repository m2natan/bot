import uuid
import pandas as pd
from constants import months
def generate_assignments(update, context):
    
    return

def audio_video_schedule(name_to_search, df ):
  found_on = list()
  task = tuple()
  for col in df.columns:
      for index, value in df[col].items():
          for name in name_to_search:
              if name in value:
                found_on.append((index, col))
  return found_on

def insert_into_calendar(index_found, df):
  formateed_str = '''BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//UnOffical API to make life easy//NONSGML v1.0//EN'''
  for i, j in index_found:
    month = months[df.iloc[i]['ወር'].replace('\n','')]
    day_number = f"{int(df.loc[i, 'ቀን'][0]):02d}"  # Convert to int and then format
    day_string = df.loc[i, 'ቀን'][1]
    if day_string == 'ሮብ':
      reminder = '150000'
    else:
      reminder = '050000'
    duty = f'''
BEGIN:VEVENT
SUMMARY:{j}
UID:{str(uuid.uuid4())}
DTSTAMP:2025{month}{day_number}T{reminder}Z
DTSTART:2025{month}{day_number}T{reminder}Z
DESCRIPTION:{df.iloc[i][j]}
LOCATION:Congregation Assignment
BEGIN:VALARM
ACTION:DISPLAY
DESCRIPTION:Reminder
TRIGGER:-PT1H
END:VALARM
END:VEVENT'''
    formateed_str += duty
  formateed_str += '''
END:VCALENDAR'''
  return formateed_str
def save_to_ics(calander):
  file_name = str(uuid.uuid4())
  with open(f"uploads/{file_name}_event.ics", "w", encoding="utf-8") as file:
      file.write(calander)

  print("ICS file saved successfully!")
  return f"{file_name}_event.ics"