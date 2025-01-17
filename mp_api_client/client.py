import requests
import json
from ftplib import FTP
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

load_dotenv()

# datetime
current_date = datetime.now()
start_date = current_date.strftime('%m/%d/%Y')
end_date = (current_date + timedelta(days=7)).strftime('%m/%d/%Y')

url = 'https://standrew.ministryplatform.com/ministryplatformapi/procs/api_church_specific_get_events'
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'Bearer {os.getenv("BEARER_TOKEN")}'
}

# payload
payload = {
    "@StartDate": start_date,
    "@EndDate" : end_date
}

# POST request
response = requests.post(url, headers=headers, json=payload)

# Check the request
if response.status_code == 200:
    data = response.json()
    formatted_json = json.dumps(data, indent=4)
    json_filename = 'events.json'
    with open('events.json', 'w') as json_file:
        json_file.write(formatted_json)
    txt_filename = 'events.txt'
    with open('events.txt', 'w') as text_file:
        text_file.write(formatted_json)
    print("Data successfully saved to events.json and events.txt")
# else:
#     print(f"Failed to fetch data: {response.status_code} - {response.text}")

    def upload_to_ftp(host, username, password, file_path, remote_path):
        try:
        # Connect to FTP Server
            ftp = FTP(host)
            ftp.login(username, password)
            print(f"Connected to FTP server: {host}")

        # open the file in binary mode and upload it
            with open(file_path, 'rb') as file:
                ftp.storbinary(f'STOR {remote_path}', file)
            print(f"Uploaded {file_path} to {remote_path}")

        # Close connection
            ftp.quit()
        except Exception as e:
            print(f"FTP upload failed: {e}")

# load FTP creds from .env
    ftp_host = os.getenv("FTP_HOST")
    ftp_username = os.getenv("FTP_USERNAME")
    ftp_password = os.getenv("FTP_PASSWORD")

# Upload JSON file
    upload_to_ftp(ftp_host, ftp_username, ftp_password, 'events.json', '/SAMC FTP/calender/FS_Cal/events.json')
    upload_to_ftp(ftp_host, ftp_username, ftp_password, 'events.txt', '/SAMC FTP/calender/FS_Cal/events.txt')

else:
    print(f"Failed to fetch data: {response.status_code} - {response.text}")