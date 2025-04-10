# Python imports.
import sqlite3

# Object imports.
from src.shared.objects import *

class DatabaseManager:
    def __init__(self, database_src: str):
        """A class object containing functions to handle query to and from a database from a given source.

        Args:
            database_src (str): Path to the database.
        """
        self.database_src = database_src
        
        self.connection = sqlite3.connect(self.database_src)
        self.cursor = self.connection.cursor()
    
    def close(self):
        """A function to commit and close the connection to the database."""
        self.connection.commit()
        self.connection.close()
    
    def get_member(self, id: int = None, email: str = None) -> Member | None:
        """A function to get a member from the database using their ID or Email.

        Args:
            id (int, optional): ID of the user.
            email (str, optional): Email of the user.

        Returns:
            Member | None: If found a Member object is returned, if not - None is returned.
        """
        extension = f"email = '{email}'" if email is not None else f"id = {id}"
        query = f"SELECT * FROM members WHERE {extension}"
        
        self.cursor.execute(query)
        fetch = self.cursor.fetchone()
        
        if fetch is None:
            return None
        
        # Create a member object and return it.
        return Member(fetch[0], fetch[1], fetch[2], fetch[3], fetch[4], fetch[5], fetch[6], fetch[7])
    
    def add_member(self, member: Member) -> bool | Member:
        """A function to add a member to the members table.

        Args:
            member (Member): Member object of the user to add to the database.
        
        Returns:
            Member | None: If the member was added to the database successfully, it will return a Member object. if it isn't it will return False.
        """
        query = "INSERT INTO members (forename, surname, email, phone, password, is_tutor, profile) VALUES (?, ?, ?, ?, ?, ?, ?)"
        
         # Add the user to the database.
        self.cursor.execute(
            query,
            (
                member.forename, member.surname, member.email,
                member.phone, member.password, 0, member.profile
            )
        )
        
        # Commit the insert.
        self.connection.commit()
        
        # Check if the insert was successfully by attempting to get the user.
        fetched_member = self.get_member(email = member.email)
        
        if fetched_member is None:
            # Unsuccessful insert.
            print(f"Unable to add member to the database: {member.email}")
            
            return False

        print(f"Member successfully added: {member.email}")
        return fetched_member
    
    def get_member_chats(self, member: Member) -> list:
        member_id = member.id
        self.cursor.execute(
            f"SELECT * FROM chats WHERE members "
            f"LIKE '%[{member_id},%'"
            f"OR members LIKE '% {member_id},%'"
            f"OR members LIKE '% {member_id}]%'"
        ) # Search for all instances of the users ID.
        
        fetch = self.cursor.fetchall()
        
        return fetch
    
    def add_message(self, chat: Chat, message: Message):
        chat.messages.append(message) # Add the message to the chat.
        
        message_dicts : list[dict] = [] # Moving the messages to a dictionary to add to database.
        for message in chat.messages:
            message_dicts.append({"user_id": message.member.id, "text": message.text})
        
        # Convert message dicts to json form.
        json_string = json.dumps(message_dicts)
        
        # Add the new json data to the chat in the database.
        self.cursor.execute(f"UPDATE chats SET messages = ? WHERE id = ?", (json_string, chat.id))
        self.connection.commit()
        
    def create_chat(self, sender: Member,receiver: Member) -> None:
        """A function to create a chat between two users."""
        sender_id = sender.id
        receiver_id = receiver.id
        
        members = [sender_id, receiver_id]
        messages = []
        
        self.cursor.execute("INSERT INTO chats (members, messages) VALUES (?, ?)", (str(members), str(messages)))
        self.connection.commit()
    
    def get_personal_chat(self, member_1: Member, member_2: Member) -> None:
        """A function to get any chat that has just two members."""
        member_1_id = member_1.id
        member_2_id = member_2.id
        
        self.cursor.execute(
            f"SELECT * FROM chats WHERE members "
            f"LIKE '[{member_1_id}, {member_2_id}]'"
            f"OR members LIKE '[{member_2_id}, {member_1_id}]'"
        ) # Search for all instances of the users ID.
        
        fetch = self.cursor.fetchone()
        
        return fetch
    
    def get_all_classes(self) -> list[AvailableClass]:
        """A function to retrieve all available classes from the database as a list of class objects.
        
        Returns:
            list[AvailableClass]: An object containing data related to the available class.
        """
        self.cursor.execute("SELECT * FROM classes")
        fetch = self.cursor.fetchall()
        
        available_classes : list[AvailableClass] = []
        for fetch_data in fetch:
            class_data = {
                "id": fetch_data[0],
                "tutor_id": fetch_data[1],
                "applied_members": fetch_data[2],
                "title": fetch_data[3],
                "description": fetch_data[4],
                "start_date": fetch_data[5]
            }
            
            available_classes.append(AvailableClass(class_data))
        
        return available_classes