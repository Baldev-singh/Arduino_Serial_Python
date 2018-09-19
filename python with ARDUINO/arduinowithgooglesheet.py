import json
import sys
import time
import serial
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

GDOCS_OAUTH_JSON       = "firstiotprojectjsonfile.json"
GDOCS_SPREADSHEET_NAME = "firstiotsheet"
FREQUENCY_SECONDS      = 4
serialArduino = serial.Serial("COM6", 9600)

def login_open_sheet(oauth_key_file, spreadsheet):
      try:
            scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
            credentials = ServiceAccountCredentials.from_json_keyfile_name(oauth_key_file, scope)
            gc = gspread.authorize(credentials)
            worksheet = gc.open(spreadsheet).sheet1
            return worksheet
      except Exception as ex:
            print('Unable to login and get spreadsheet.  Check OAuth credentials, spreadsheet name, and make sure spreadsheet is shared to the client_email address in the OAuth .json file!')
            print('Google sheet login failed with error:', ex)
            print(" ")
            sys.exit(1)


print('Logging sensor measurements to {0} every {1} seconds.'.format(GDOCS_SPREADSHEET_NAME, FREQUENCY_SECONDS))
print('Press Ctrl-C to quit.')
worksheet = None

while True:
      if worksheet is None:
            worksheet = login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SPREADSHEET_NAME)
            print ("login to google sheet with login details")
      try:
            valueRead = serialArduino.readline()
            value=valueRead.decode()
            print(value)
            worksheet.append_row((str(value) ))
            print("Written*******************************************")
      
      except:
            print('Append error, logging in again')
            worksheet = None
            time.sleep(FREQUENCY_SECONDS)
            continue
      print('                       Written to Row No. {0}'.format(GDOCS_SPREADSHEET_NAME))
      time.sleep(FREQUENCY_SECONDS)
