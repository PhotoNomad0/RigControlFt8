import requests

def get_json_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception if the request was unsuccessful
        return response.json()  # Parse the JSON data from the response
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while trying to get data from the URL: {e}")
        return None

# Use the function
url = "http://127.0.0.1:8091/sdrangel/deviceset/0/device/settings"
json_data = get_json_from_url(url)
print(json_data)
