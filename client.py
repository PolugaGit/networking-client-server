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
        # TODO: Create the client socket and connect to the server
        print(f"Connected to server: {host} {port}")
        # TODO: Get the username from the user and use the send function to send it to the server

    # A helper function that sends one of three types of messages to the server with the proper encoding. 
    def send(self, type: DataType, payload: str) -> None:
        # TODO: Create a JSON string with type and payload and send it to the server
        pass # delete this
    
    # Runs the main program loop. Gets input from the user then calls the appropriate function.
    def run(self) -> None:
        content: str = ""
        while True:
            print()
            content = input("Enter 1 to send a message, 2 to refresh messages, or 3 to quit and disconnect: ")
            # TODO: Call functions based on content            
        self.client.close()

    # Handles user message send requests. Sends a message to the server with username, body, and timestamp.
    def handleMessage(self) -> None:
        # TODO: Get input from the user, create a message object, and send it
        pass # delete this
    
    
    # Handles user refresh requests. Sends a request to the server then displays message log.
    def handleRefresh(self) -> None:
        
        # TODO: Send a refresh request, decode the response, and call print_messages
        pass # delete this     
       
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
