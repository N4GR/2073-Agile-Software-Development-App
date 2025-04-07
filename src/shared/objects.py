# Python imports
import json

# Third-party imports.
from PySide6.QtWidgets import QApplication

class Member:
    def __init__(
            self,
            id: int,
            forename: str,
            surname: str,
            email: str,
            phone: str,
            password: str
    ):
        """An object containing data related to a member.

        Args:
            id (int): ID of the user.
            forename (str): Forename of the user.
            surname (str): Surname of the user.
            email (str): Email of the user.
            phone (str): Phone number of the user.
        """
        self.id = id
        self.forename = forename
        self.surname = surname
        self.email = email
        self.phone = phone
        self.password = password

class Message:
    def __init__(
            self,
            member: Member,
            text: str
    ):
        """An object containing the data of a message.

        Args:
            member (Member): Member that sent the message.
            text (str): Text content of the message.
        """
        self.member = member
        self.text = text

class Chat:
    def __init__(
        self,
        chat_data: tuple
    ):
        """An object containing chat data related to a member.

        Args:
            chat_data (tuple): Chat data retrieved from the database.
        """
        self.chat_data = chat_data
        
        self.id = self.chat_data[0]
        self.members = self.get_members()
        self.messages = self.get_messages()
    
    def get_members(self) -> list[Member]:
        """A function to retrieve the member objects inside the chat."""
        # Connection to the gym database to obtain member data.
        database = QApplication.instance().property("DatabaseManager")("data/gym.sqlite")
        
        members : list[Member] = [] # Member storage.
        chat_ids = self.chat_data[1].replace("[", "").replace("]", "").split(", ") # [113, 114] -> list.
        
        for id in chat_ids:
            members.append(database.get_member(id = id))
        
        return members
    
    def get_messages(self) -> list[Message]:
        message_dicts = self.chat_data[2].replace("[", "").replace("]", "").split("}, ")
        
        if message_dicts[0] == "":
            return [] # Return early.
        
        raw_messages : list[dict] = [] # List of dictionary storage.
        for message in message_dicts:            
            if message[-1] != "}":
                message = message + "}"
            
            raw_messages.append(json.loads(message))
        
        messages : list[Message] = [] # Storage for Messages
        for message in raw_messages:
            user_id = message["user_id"]
            
            # Get the Member object of the user who sent the message.
            for member in self.members:
                if member.id == user_id:
                    # Create a message object from found member object.
                    messages.append(Message(member, message["text"]))
        
        return messages