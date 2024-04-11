import requests

def get_json_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception if the request was unsuccessful
        return response.json()  # Parse the JSON data from the response
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while trying to get data from the URL: {e}")
        return None

def getAdsAngelSettings():
    url = "http://127.0.0.1:8091/sdrangel/deviceset/0/device/settings"
    json_data = get_json_from_url(url)
    return json_data

def setAdsAngelFrequency(newFreq):
    settings = getAdsAngelSettings()
    print(settings)
    
    if settings:
        newSettings = settings['rtlSdrSettings']['centerFrequency']
        print(newSettings)
        return newSettings

    return None

settings = setAdsAngelFrequency(14074000)
print('new angel settings:')
print(settings)

