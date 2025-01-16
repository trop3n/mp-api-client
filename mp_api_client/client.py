import requests
import json

url = 'https://standrew.ministryplatform.com/ministryplatformapi/procs/api_church_specific_get_events'
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6InJxeFh2T25od1Y5VXhIQV9GNzZtbHRORlo0cyIsImtpZCI6InJxeFh2T25od1Y5VXhIQV9GNzZtbHRORlo0cyJ9.eyJpc3MiOiJodHRwczovL3N0YW5kcmV3Lm1pbmlzdHJ5cGxhdGZvcm0uY29tL21pbmlzdHJ5cGxhdGZvcm1hcGkvb2F1dGgiLCJhdWQiOiJodHRwczovL3N0YW5kcmV3Lm1pbmlzdHJ5cGxhdGZvcm0uY29tL21pbmlzdHJ5cGxhdGZvcm1hcGkvb2F1dGgvcmVzb3VyY2VzIiwiZXhwIjoxNzM3MDQ5ODM2LCJuYmYiOjE3MzcwNDYyMzYsImNsaWVudF9pZCI6IlBsYXRmb3JtLldlYi5TZXJ2aWNlcyIsInNjb3BlIjoiaHR0cDovL3d3dy50aGlua21pbmlzdHJ5LmNvbS9kYXRhcGxhdGZvcm0vc2NvcGVzL2FsbCIsInN1YiI6IjNlOGE3MTYxLTIyNWEtNDE3NS1iNTUyLWU4YWZmYzc5ZjQ4YSIsImF1dGhfdGltZSI6MTcyODQyMDY0NiwiaWRwIjoiaWRzcnYiLCJhdXRoX2hhc2giOiI0WGpzM0tNS2RjeW9XN1pMOHZKNWx3PT0iLCJuYW1lIjoiSmFzb25LIiwiYW1yIjpbInBhc3N3b3JkIl19.q4b3J2aiZgNVsiDX2t8TD_654QgsB3To5Ql7azaLBXjsY0Ln94NJ9rvvv25gEju6Gt09IUKuY-cBOg08YxnshvQ1eQYaPjyiaAInhBchbeXIbHkMk5rW7jcjfLk-9VRWbOVzPGqpQzGzllX2awyj6PVfdKQV_ke2m7IKEHVJd1aSG1VudiB-_iowio8ssL_G9cWlpBqexBZp_6IFnxBfs3uPKJ05aLvf-oCoM6zp0Nx_omOdQLGftS5y75sRLP11jOSmEmG6AWEra3KurKfizKgcrGAl_Q1OcfyTtdz3x1nbgKExiPQ-23VndhHHYp5Al-A2PdDRZM6Vz-if30DkaA'
}

# payload
payload = {
    "@StartDate": "1/16/2025",
    "@EndDate" : "1/23/2025"
}

# POST request
response = requests.post(url, headers=headers, json=payload)

# Check the request
if response.status_code == 200:
    data = response.json()
    formatted_json = json.dumps(data, indent=4)
    with open('events.json', 'w') as json_file:
        json_file.write(formatted_json)
    with open('events.txt', 'w') as text_file:
        text_file.write(formatted_json)
    print("Data successfully saved to events.json and events.txt")
else:
    print(f"Failed to fetch data: {response.status_code} - {response.text}")