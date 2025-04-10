# A file to load testing data into the database.

import sqlite3
from faker import Faker
import random
import os

from src.shared.objects import Member
from src.shared.funcs import path

class TestingData:
    def __init__(self):
        self.chat_connection = sqlite3.connect("data/chat.sqlite")
        self.gym_connection = sqlite3.connect("data/gym.sqlite")
        
        self.chat_cursor = self.chat_connection.cursor()
        self.gym_cursor = self.gym_connection.cursor()
        
        # Faker instance.
        self.faker = Faker("en_GB")
    
        self.member_count = 100
        self.chats_per_member = 10
        
        self.add_members()
        self.add_chats()
    
    def add_members(self):
        # Get current members.
        self.gym_cursor.execute("SELECT * FROM members")
        fetch = self.gym_cursor.fetchall()
        
        needed_members = self.member_count
        
        if len(fetch) >= 0:
            needed_members -= len(fetch)
        
        print(f"Adding {needed_members} random members to the database.")
        
        for x in range(needed_members):
            forename = self.faker.first_name()
            surname = self.faker.last_name()
            email = self.faker.email(safe = True)
            phone = self.faker.phone_number()
            password = self.faker.password(random.randint(5, 13))
            profile = f"{random.randint(1, len(os.listdir(path('/assets/profiles'))))}.png"
            
            # 1 in 10 change for someone to be a tutor.
            is_tutor = 1 if random.randint(1, 10) == 1 else 0
            
            # Add to database.
            self.gym_cursor.execute(
                "INSERT INTO members"
                "(forename, surname, email, phone, password, is_tutor, profile)"
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (forename, surname, email, phone, password, is_tutor, profile)
            )
            self.gym_connection.commit() # Commit change.

    def add_chats(self):
        # Get a list of current members.
        self.gym_cursor.execute("SELECT * FROM members")
        
        members : list[Member] = []
        for member in self.gym_cursor.fetchall():
            members.append(Member(
                member[0],
                member[1],
                member[2],
                member[3],
                member[4],
                member[5],
                True if member[6] == 1 else False,
                f"{random.randint(1, 16)}.png"
            ))
        
        for member in members:
            # Get a list of chats the member is a part of.
            self.chat_cursor.execute(
                f"SELECT * FROM chats WHERE members "
                f"LIKE '%[{member.id},%'"
                f"OR members LIKE '% {member.id},%'"
                f"OR members LIKE '% {member.id}]%'"
            ) # Search for all instances of the users ID.
            
            member_chats = self.chat_cursor.fetchall()
            chats_remaining = self.chats_per_member
            
            if len(member_chats) < chats_remaining:
                chats_remaining -= len(member_chats)
                
            else:
                chats_remaining = 0
            
            if chats_remaining == 0:
                return
            
            else:
                print(f"Adding {chats_remaining} random chats to {member.email}")
            
            # For each remaining chat.
            for x in range(chats_remaining):
                while True:
                    receiver = random.choice(members)
                    
                    if receiver != member: break
                
                db_members = f"[{member.id}, {receiver.id}]"
                db_messages = [
                    {
                        "user_id": member.id,
                        "text": "Heyyyyyy"
                    },
                    {
                        "user_id": receiver.id,
                        "text": "How are you doing?? :)"
                    }
                ]
                
                self.chat_cursor.execute(
                    f"INSERT INTO chats (members, messages) VALUES (?, ?)",
                    (db_members, str(db_messages).replace("'", "\""))
                )
                self.chat_connection.commit()
                    
    def add_classes(self):
        for x in range(self.available_classes):
            pass