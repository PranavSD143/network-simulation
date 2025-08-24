from transport_layer.udp_transport import SimpleUDPTransport

udp = SimpleUDPTransport(dest_ip="127.0.0.1", dest_port=9999)
response = udp.send(b"hello udp server")
print("response:", response)


