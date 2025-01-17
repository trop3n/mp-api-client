import requests
import json
from ftplib import FTP_TLS
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TOKEN_URL = os.getenv("TOKEN_URL") # API Endpoint

def fetch_bearer_token():
    try:
        response = requests.post(
            TOKEN_URL,
            data={
                "grant_type": "client_credentials",
                "client_id" : CLIENT_ID,
                "client_secret" : CLIENT_SECRET,                 
                "scope" : "http://www.thinkministry.com/dataplatform/scopes/all"
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        response.raise_for_status() # raise an error for bad codes
        token_data = response.json()
        print("Bearer token fetched successfully!")
        return token_data["access_token"], datetime.now() + timedelta(hours=1)
    except Exception as e:
        print(f"Failed to fetch Bearer token: {e}")
        return None, None

def get_bearer_token():
    bearer_token = os.getenv("BEARER_TOKEN")
    token_expiration = os.getenv("TOKEN_EXPIRATION")
    if not bearer_token or (token_expiration and datetime.now() > datetime.fromisoformat(token_expiration)):
        print("Bearer token not found in .env. Fetching a new one...")
        new_token, new_expiration = fetch_bearer_token()
        if new_token:
            with open(".env", "r") as env_file:
                lines = env_file.readlines()
            
            # update constants in .env
            updated_lines = []
            for line in lines:
                if line.startswith("BEARER_TOKEN="):
                    updated_lines.append(f"BEARER_TOKEN={new_token}\n")
                elif line.startswith("TOKEN_EXPIRATION="):
                    updated_lines.append(f"TOKEN_EXPIRATION={new_expiration.isoformat()}\n")
                else:
                    updated_lines.append(line)  
            
            with open(".env", "w") as env_file:
                env_file.writelines(updated_lines)
            print("New Bearer token saved to .env!")
            return new_token
        else:
            raise Exception("Failed to fetch a new Bearer token.")
        
    print("Using existing Bearer token.")   
    return bearer_token

def upload_to_ftp(host, username, password, file_path, remote_path):
    try:
        ftp = FTP_TLS()
        ftp.login(username, password)
        ftp.prot_p()
        print(f"Connected to FTPS server: {host}")
        with open(file_path, "rb") as file:
            ftp.storbinary(f"STOR {remote_path}", file)
        print(f"Uploaded {file_path} to {remote_path}")
        # close connection
        ftp.quit()
    except Exception as e:
        print(f'FTPS upload failed: {e}')

# Main
def main():
    bearer_token = get_bearer_token()
    if not bearer_token:
        print("Unable to proceed without valid Bearer token.")
        return
    url = "https://standrew.ministryplatform.com/ministryplatformapi/procs/api_church_specific_get_events"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {bearer_token}"
    }

    # Define the payload with dynamic dates
    current_date = datetime.now()
    payload = {
        "@StartDate": current_date.strftime("%m/%d/%Y"),
        "@EndDate": (current_date + timedelta(days=7)).strftime("%m/%d/%Y")
    }
    response = requests.post(url, headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        # parse the JSON response
        data = response.json()

        # Readability format
        formatted_json = json.dumps(data, indent=4)
        
        # Save the formatted JSON to file
        json_filename = "events.json"
        with open(json_filename, 'w') as json_file:
            json_file.write(formatted_json)

        # Save the formatted JSON to text file
        txt_filename = "events.txt"
        with open(txt_filename, "w") as text_file:
            text_file.write(formatted_json)

        print("Data successfully saved to events.json and events.txt")

        # Load FTP creds
        ftp_host = os.getenv("FTP_HOST")
        ftp_username = os.getenv("FTP_USERNAME")
        ftp_password = os.getenv("FTP_PASSWORD")

        # Upload JSON
        upload_to_ftp(ftp_host, ftp_username, ftp_password, json_filename, "/calender/FS_CAL/events.json")

        # Upload TXT
        upload_to_ftp(ftp_host, ftp_username, ftp_password, txt_filename, "calender/FS_CAL/events.txt")
    else:
        print(f"Failed to fetch data: {response.status_code} - {response.text}")
    
if __name__ == "__main__":
    main()