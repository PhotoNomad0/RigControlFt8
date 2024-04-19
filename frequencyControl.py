import requests
import json
import socket
import socketserver
import pywsjtx
import serial

SDR_ANGEL_URL = 'http://127.0.0.1:8091/sdrangel/deviceset/0/device/settings'
# WSJT-X UDP server details
WSJTX_IP = '127.0.0.1'  # Replace with actual IP if needed
WSJTX_PORT = 2237

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
    json_data = put_json_to_url(SDR_ANGEL_URL, newSettings)
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
    json_data = get_json_from_url(SDR_ANGEL_URL)
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
# start_udp_server(WSJTX_PORT)

# def sendCommandToWSJTx(command):
#     with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
#         encoded = command.encode()
#         sock.sendto(encoded, (WSJTX_IP, WSJTX_PORT))
#         print('Sent command', command)
#         print('Sent encoded', encoded)
# 
# # Example commands
# #sendCommandToWSJTx("FA000140740")  # Set frequency to 14.000 MHz
# sendCommandToWSJTx("FA000280740")  # Set frequency to 14.000 MHz


# # Create a WSJT-X packet with the desired frequency
# packet = pywsjtx.WsjtxPacket(
#     packet_type=pywsjtx.PacketType.FREQUENCY,
#     frequency=14076000  # Frequency in Hz
# )
# 
# # Send the packet to WSJT-X
# pywsjtx.udp_send(packet, 'localhost', 2237)  # Assumes WSJT-X is running on localhost and listening on port 2237


# # Open serial port
# ser = serial.Serial(
#     port='/dev/ttys003',  # replace with your serial port
#     baudrate=38400,      # set baud rate
#     bytesize=8,         # number of data bits (5, 6, 7, 8)
#     stopbits=1,         # number of stop bits (1, 1.5, 2)
#     parity='N'          # parity check ('N'- None, 'E'- Even, 'O'- Odd)
# )
# 
# print("Starting...")
# 
# while True:
#     # Read a line from the serial port
#     line = ser.readline().decode('utf-8').strip()
# 
#     # Print the line
#     print(f"Received: '{line}'")
# 
#     # Write the line back to the serial port
#     ser.write((line + '\n').encode('utf-8'))

class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.msg = self.request.recv(1024).strip()
        if self.msg == b"on<EOF>":
            print("Turning On...")
            self.request.sendall(b"SUCCESS<EOF>")
        elif self.msg == b"off<EOF>":
            print("Turning Off...")
            self.request.sendall(b"SUCCESS<EOF>")


HAMLIB_PORT = 4533
host, port = WSJTX_IP, HAMLIB_PORT
server = socketserver.TCPServer((host, port), TCPHandler)
print("Server is starting on", host, port)
server.serve_forever()
