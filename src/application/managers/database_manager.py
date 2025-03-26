# Python imports.
import sqlite3

# Object imports.
from src.shared.objects import Member

class DatabaseManager:
    def __init__(
            self,
            database_src: str
    ):
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
    
    def get_member(
            self,
            id: int = None,
            email: str = None
    ) -> Member | None:
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
        
        if fetch == "()":
            return None
        
        # Create a member object and return it.
        return Member(
            fetch[0],
            fetch[1],
            fetch[2],
            fetch[3],
            fetch[4],
            fetch[5]
        )
    
    def add_member(
            self,
            member: Member
    ) -> bool | Member:
        """A function to add a member to the members table.

        Args:
            member (Member): Member object of the user to add to the database.
        
        Returns:
            Member | None: If the member was added to the database successfully, it will return a Member object. if it isn't it will return False.
        """
        query = "INSERT INTO members (forename, surname, email, phone, password) VALUES (?, ?, ?, ?, ?)"
        
        self.cursor.execute(
            query,
            (
                member.forename,
                member.surname,
                member.email,
                member.phone,
                member.password
            )
        ) # Add the user to the database.
        
        # Commit the insert.
        self.connection.commit()
        
        # Check if the insert was successfully by attempting to get the user.
        fetched_member = self.get_member(email = member.email)
        
        if fetched_member is None:
            # Unsuccessful insert.
            return False
        
        elif fetched_member is Member:
            # If it's a member object.
            return fetched_member