from core import config as config
import socket
import os

class ListenerSocket:
    def __init__(self) -> None:
        self.config = config.basic
        self.client: socket.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock_path = os.path.join(self.config.RUNTIME_PATH, "ncspot.sock")

    def start_sock(self):
        """Creates our asyncio loop for connect_sock"""


    def connect_sock(self):
        print(f"Starting socket... at {self.config.RUNTIME_PATH}/ncspot.sock")
        print(self.config.RUNTIME_PATH)

        connection = self.client.connect(self.sock_path)

        try:
            while True:
                data = self.client.recv(1024)

                if data:
                    print(f"Recieved:  {data.decode('utf-8')}")
                else:
                    print("Connection closed by server")
                    break

        except KeyboardInterrupt:
            print("Closing.")
        finally:
            self.client.close()
