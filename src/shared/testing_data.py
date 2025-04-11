# A file to load testing data into the database.

import sqlite3
from faker import Faker
import random
import os
from datetime import datetime, timedelta

from src.shared.objects import Member
from src.shared.funcs import path

class TestingData:
    def __init__(self):
        self.chat_connection = sqlite3.connect(path("data/chat.sqlite"))
        self.gym_connection = sqlite3.connect(path("data/gym.sqlite"))
        
        self.chat_cursor = self.chat_connection.cursor()
        self.gym_cursor = self.gym_connection.cursor()
        
        # Faker instance.
        self.faker = Faker("en_GB")
    
        self.member_count = 100
        self.chats_per_member = 10
        self.classes_to_generate = 10
        
        self.add_members()
        self.add_chats()
        self.add_classes()
    
    def add_members(self):
        # Get current members.
        self.gym_cursor.execute("SELECT * FROM members")
        fetch = self.gym_cursor.fetchall()
        
        needed_members = self.member_count
        
        if len(fetch) >= 0:
            needed_members -= len(fetch)
        
        if needed_members <= 0:
            return
        
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
            
            if float(chats_remaining) <= 0:
                return
            
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
        # Get the current tutors.
        self.gym_cursor.execute("SELECT * FROM members WHERE is_tutor = 1")
        tutor_fetch = self.gym_cursor.fetchall()
        
        # Get all members that aren't tutors.
        self.gym_cursor.execute("SELECT * FROM members WHERE is_tutor = 0")
        member_fetch = self.gym_cursor.fetchall()        
        
        # Get all available classes.
        self.gym_cursor.execute("SELECT * FROM classes")
        classes_fetch = self.gym_cursor.fetchall()
        
        remaining_classes = self.classes_to_generate
        remaining_classes -= len(classes_fetch)
        
        if remaining_classes <= 0:
            return # Return early.
        
        print(f"Adding {remaining_classes} classes.")
        
        classes = [
            {
                "Title": "Swimming Class",
                "Description": "We will be teaching you how to swim!"
            },
            {
                "Title": "Weight Lifting",
                "Description": "Weight lifting best practises."
            },
            {
                "Title": "Marathon",
                "Description": "Marathon event, come join!"
            },
            {
                "Title": "Treadmill Class",
                "Description": "Let's listen to some jams and tread!"
            },
            {
                "Title": "Dietry",
                "Description": "Best dietry options to gain muscle."
            }
        ]
        
        for x in range(remaining_classes):
            creating_class = random.choice(classes)
            title = creating_class["Title"]
            description = creating_class["Description"]
            start_date = datetime.now() + timedelta(days = random.randint(7, 24))
            start_date = datetime.strftime(start_date, "%Y-%m-%d %H:%M")
            
            tutor = random.choice(tutor_fetch)
            tutor_id = tutor[0]
            
            applied_members : list[int] = []
            
            for i in range(random.randint(0, 5)):
                mem = random.choice(member_fetch)
                applied_members.append(mem[0])
            
            # Add the class to the classes table.
            self.gym_cursor.execute(
                "INSERT INTO classes"
                "(tutor_id, applied_members, title, description, start_date) VALUES"
                "(?, ?, ?, ?, ?)",
                (tutor_id, str(applied_members), title, description, str(start_date))
            )
            
            self.gym_connection.commit()