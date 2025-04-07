import json
import socket
import sys
import threading
from typing import List, Tuple

from message import Message, DataType

# The server class is a single class that can support multiple clients connected at the same time.
# We want to build a server class that can receive messages from clients and send a list of previous messages back to the clients.
class Server:
    
    # The init function (constructor) is used to set up instance variables. Here, we create a socket on the given
    # IP address and port to listen for client connections. We also set up the list of messages we have received and 
    # a lock for multithreading (don't worry about this).  
    def __init__(self, host: str, port: int) -> None:
        self.server: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # TODO: start the server
        self.server.bind((host, port))
        self.server.listen()

        self.messages: List[Message] = []
        self.lock: threading.Lock = threading.Lock()
        
    # This function handles clients who create a connection with the server. We should operate in a loop
    # waiting for data from the client and react appropriately given the DataType. Call other functions
    # to handle certain client requests.
    def handle_client(self, client: socket.socket, addr: Tuple[str, int]) -> None:
        print(f"New client connected from address: {addr}")
        # should we add something here to catch username? 
        username: str = ""
        try:
            while True:
                data = client.recv(4096)
                # TODO: Receive data from the client, decode it, then call the appropriate function
                data_dict = json.loads(data.decode("utf-8"))
       
                dtype = DataType[data_dict.get("type")]

                if dtype == DataType.MESSAGE:
                    self.handle_message(data_dict)
                elif dtype ==  DataType.REFRESH:
                    self.handle_refresh(client)
                elif dtype == DataType.USERNAME:
                    username = data_dict.get("payload")
                
        except Exception as e:
            print(f"Error with {username}: {e}")
        finally:
            client.close()
            print(f"{username} disconnected")
            
    # A helper function to handle new messages from clients. This function should parse the data into a 
    # Message object then add it to the list of messages.
    def handle_message(self, data_dict) -> None:
        with self.lock:
            # TODO: create a Message object and add it do the list
            payload_dict = json.loads(data_dict["payload"])
            msg = Message.from_dict(payload_dict)
            self.messages.append(msg)
        
    # A helper function to handle refresh requests from clients. This function should send a list of messages
    # back to the client.
    def handle_refresh(self, client) -> None:
        with self.lock:
            # TODO: convert the entire list of messages and send it to the client
            all_msgs = [m.to_dict() for m in self.messages]
            response = json.dumps(all_msgs).encode("utf-8")
            client.sendall(response)       
    
    # This is the main program loop. This function waits for client connections then calls handle_client as needed
    def run(self) -> None:
        print("Server running ...")
        while True:
            client: socket.socket
            addr: Tuple[str, int]
            client, addr = self.server.accept()
            
            client_thread: threading.Thread = threading.Thread(
                target=self.handle_client,
                args=(client, addr),
                daemon=True
            )
            client_thread.start()

# Initializes the Server object and runs it.
if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: python server.py [Server Address] [Server Port]")
        
    serv_addr: str = sys.argv[1]
    serv_port: int = int(sys.argv[2])

    server: Server = Server(serv_addr, serv_port)
    server.run()
