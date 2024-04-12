import requests
import json
import socket

sdrAngelUrl = 'http://127.0.0.1:8091/sdrangel/deviceset/0/device/settings'

def put_json_to_url(url, data_dict):
    try:
        headers = {'Content-Type': 'application/json'}  # Define the correct headers for a JSON payload
        response = requests.put(url, data=json.dumps(data_dict), headers=headers)  # Convert the dictionary to a JSON string
        response.raise_for_status()  # Raise exception if the request was unsuccessful
        return response.json()  # Parse the JSON data from the response
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while trying to put data to the URL: {e}")
        return None

def setSdrAngelSettings(newSettings):
    json_data = put_json_to_url(sdrAngelUrl, newSettings)
    return json_data

def get_json_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception if the request was unsuccessful
        return response.json()  # Parse the JSON data from the response
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while trying to get data from the URL: {e}")
        return None

def getSdrAngelSettings():
    json_data = get_json_from_url(sdrAngelUrl)
    return json_data

def setAdsAngelFrequency(newFreq):
    settings = getSdrAngelSettings()
    print(settings)
    
    if settings:
        newSettings = settings
        newSettings['rtlSdrSettings']['centerFrequency'] = newFreq
        print(newSettings)
        response = setSdrAngelSettings(newSettings)
        return response

    return None

# settings = setAdsAngelFrequency(28074000)
# print('new angel settings:')
# print(settings)

def start_udp_server(port):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to the port
    server_address = ('localhost', port)
    sock.bind(server_address)

    while True:
        print("\nWaiting to receive message on port", port)
        data, address = sock.recvfrom(4096)

        print("Received %s bytes from %s" % (len(data), address))

        try:
            message = data.decode('utf-8')
            print("Message content: ", message)
        except UnicodeDecodeError as e:
            print(f'Error decoding message: {e}', data)


        # Assuming the data is in JSON format, you can parse it like this:
        # try:
        #     message = json.loads(data)
        #     print("Received message: ", message)
        # except json.JSONDecodeError:
        #     print("Received message is not valid JSON")

# Use the function
# 2237 is the port
start_udp_server(2237)