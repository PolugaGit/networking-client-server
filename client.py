import json
import socket
import sys
import time
from typing import List

from message import Message, DataType

# The ChatClient is run on clients to interact with the server. When setting up, we give the class an IPv4 address and port
# number to connect to the server. The client initiates a connection with the server at the given address and port using the socket
# library. Then, it uses the run function to handle interaction from the user. 
class ChatClient:
    
    # The init function (constructor) is used to set up instance variables. Every Client object has a socket connection 
    # and a username. This function sets up the connection to the server and sends the username to the server. 
    def __init__(self, host: str, port: int ) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        print(f"Connected to server: {host} {port}")
        
        self.username = input("Enter your username: ")
        self.send(DataType.USERNAME, self.username)

    # A helper function that sends one of three types of messages to the server with the proper encoding. 
    def send(self, type: DataType, payload: str) -> None:
        # TODO: Create a JSON string with type and payload and send it to the server
        message = {
            "type": type.name,  # Convert enum to string
            "payload": payload
        }
        self.client.sendall(json.dumps(message).encode())
    
    # Runs the main program loop. Gets input from the user then calls the appropriate function.
    def run(self) -> None:
        while True:
            print()
            content = input("Enter 1 to send a message, 2 to refresh messages, or 3 to quit and disconnect: ")
            
            if content == "1":
                self.handleMessage()
            elif content == "2":
                self.handleRefresh()
            elif content == "3":
                self.send(DataType.DISCONNECT, "Client disconnected.")
                print("Disconnected from chat.")
                break
            else:
                print("Invalid input.")
        
        self.client.close()


        # Handles user message send requests. Sends a message to the server with username, body, and timestamp.
    def handleMessage(self) -> None:
        body = input("Enter your message: ")
        msg = Message(sender_id=self.username, body=body, timestamp=self.getTimestamp())
        self.send(DataType.MESSAGE, json.dumps(msg.__dict__))

    
    # Handles user refresh requests. Sends a request to the server then displays message log.
    def handleRefresh(self) -> None:
        self.send(DataType.REFRESH, "")
        response = self.client.recv(4096)
        messages_data = json.loads(response.decode())
        
        messages = [Message(**msg) for msg in messages_data]
        self.print_messages(messages)

       
    # A helper function to print the list of messages. 
    # Do not change this.
    def print_messages(self, messages: List[Message]) -> None:
        print("\nChat History:")
        for msg in messages:
            print(f"[{msg.timestamp}] [{msg.sender_id}] {msg.body}")

       
       
    # A helper function to return a nicely formatted timestamp as a string.  
    # Do not change this.   
    def getTimestamp(self) -> str:
        return time.strftime("%a, %d %b %Y %H:%M:%S")


# Initializes the Client object and runs it.
if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: python client.py [Server Address] [Server Port]")
        
    serv_addr: str = sys.argv[1]
    serv_port: int = int(sys.argv[2])

    client: ChatClient = ChatClient(serv_addr, serv_port)
    client.run()
