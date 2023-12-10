import json
import requests

# Load the HAR file
with open('www.youtube.com.har', 'r', encoding='utf-8') as file:
    har_data = json.load(file)

# Iterate through the entries in the HAR file
for entry in har_data['log']['entries']:
    request = entry['request']

    # Extract relevant information
    url = request['url']
    method = request['method']
    headers = {header['name']: header['value'] for header in request['headers']}
    body = request.get('postData', {}).get('text', '')

    print(headers)
    # print(body)

    # Send the HTTP request
    # response = requests.request(method, url, headers=headers, data=body)

    # Print or process the response as needed
    # print(f"Request URL: {url}")
    # print(f"Response Status Code: {response.status_code}")
    # print(f"Response Content: {response.text}")

