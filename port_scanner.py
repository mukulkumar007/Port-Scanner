import socket
import threading
from queue import Queue

# Input from user
target = input("Enter target (example: scanme.nmap.org): ")
start_port = int(input("Start port: "))
end_port = int(input("End port: "))

queue = Queue()

# Function to scan ports
def scan():
    while not queue.empty():
        port = queue.get()
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)

            result = s.connect_ex((target, port))

            if result == 0:
                print(f"[OPEN] Port {port}")

                # Service Detection
                if port == 80:
                    print("   Service: HTTP")
                elif port == 443:
                    print("   Service: HTTPS")
                elif port == 22:
                    print("   Service: SSH")
                elif port == 21:
                    print("   Service: FTP")
                elif port == 25:
                    print("   Service: SMTP")

                # Banner Grabbing
                try:
                    s.send(b"Hello\r\n")
                    banner = s.recv(1024)
                    print(f"   Banner: {banner.decode().strip()}")
                except:
                    pass

            s.close()
        except:
            pass

        queue.task_done()

# Add ports to queue
for port in range(start_port, end_port + 1):
    queue.put(port)

# Create threads
for _ in range(100):  # You can change thread count if needed
    t = threading.Thread(target=scan)
    t.daemon = True
    t.start()

# Wait until all tasks are done
queue.join()

print("\nScanning complete!")