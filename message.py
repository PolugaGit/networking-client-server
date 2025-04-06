from enum import IntEnum


# The Message class is used to represent a message sent from a client. A message has...
# sender_id - the username of the sender
# body - the message content
# timestamp - the timestamp at which the message was sent
class Message:
    def __init__(
        self,
        sender_id: str,
        body: str,
        timestamp: str
    ) -> None:
        self.sender_id: str = sender_id
        self.body: str = body
        self.timestamp: str = timestamp

    # This function converts the Message object to a python dictionary. Useful for json methods...
    def to_dict(self):
        return {'sender_id': self.sender_id, 'body': self.body, 'timestamp': self.timestamp}

    # This static method converts a python dict to a Message object. Useful for json methods...
    @staticmethod
    def from_dict(data):
        return Message(sender_id=data['sender_id'], body=data['body'], timestamp=data['timestamp'])



# Represents the different types of data that the client can send to or request from the server.
class DataType(IntEnum):
    USERNAME = 1
    MESSAGE = 2
    REFRESH = 3

