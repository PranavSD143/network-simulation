import threading
import time
from application_layer.http_client import BrowserHTTPClient as ob
from transport_layer.tcp_transport import TCPTransport
from network_layer.network_layer import SimpleIPNetwork

# Your existing code
url = "http://localhost:8000/echo"
method = "GET"
headers = {
    "Content-Type": "application/json",
    "Connection": "close"
}
body = "Testing the stack"

client = ob(method, url, headers, body)
http_bytes = client.build_http_request_bytes()
host, port = client.get_host_port()
dest_ip = "127.0.0.1"
net = SimpleIPNetwork("127.0.0.1", dest_ip)

def sender():
    print("Sender: Sending packet...")
    tcp = TCPTransport("127.0.0.1", dest_ip, 12345, 80, net)
    tcp.send(http_bytes)
    print("Sender: Packet sent.")

def receiver():
    print("Receiver: Waiting for packet...")
    tcp = TCPTransport("127.0.0.1", dest_ip, 12345, 80, net)
    try:
        response = tcp.receive()
        if response:
            print("Receiver: Packet received.")
            print(response.decode('utf-8'))
        else:
            print("Receiver: No packet received.")
    except UnicodeDecodeError:
        print("Receiver: Decode error. Received data is likely a header.")
    finally:
        print("Receiver: Finished.")

# Create threads for the sender and receiver
sender_thread = threading.Thread(target=sender)
receiver_thread = threading.Thread(target=receiver)

# Start both threads
receiver_thread.start()
time.sleep(1) # Give the receiver a moment to start listening
sender_thread.start()

# Wait for both threads to complete
sender_thread.join()
receiver_thread.join()