from application_layer.http_client import BrowserHTTPClient as ob
from transport_layer.tcp_transport import TCPTransport
from network_layer.network_layer import SimpleIPNetwork
import socket

url = "http://localhost:8000/echo"
method = "GET"
headers = {
    "Content-Type": "application/json",
    "Connection": "close"
}
body = "Testing the stack"

client = ob(method,url,headers,body)

http_bytes = client.build_http_request_bytes()
# print(http_bytes)
# 2. Create and use transport layer
host,port = client.get_host_port()
# dest_ip = socket.gethostbyname(host)

dest_ip = "127.0.0.1"

net = SimpleIPNetwork("127.0.0.1",dest_ip)
tcp = TCPTransport("127.0.0.1",dest_ip,12345,80,net)
tcp.send(http_bytes)

response = tcp.receive()

# 3. Print response
print(response.decode())
