from fastapi import FastAPI
import socket
import threading

def udp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(("0.0.0.0", 9999))
        print("[UDP] Server listening on port 9999")
        while True:
            data, addr = s.recvfrom(1024)
            print(f"[UDP] Got {data} from {addr}")
            s.sendto(b"ack", addr)

# Start UDP server in background thread
threading.Thread(target=udp_server, daemon=True).start()

# HTTP (FastAPI) server
app = FastAPI()

@app.get("/echo")
async def hello():
    return {"message": "Hello from FastAPI (HTTP over TCP) + UDP server"}