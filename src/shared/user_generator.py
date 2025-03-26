# FOR TESTING, TO GENERATE USERS IN THE MEMEBRS TABLE.
import sqlite3
import names
from phone_gen import PhoneNumber
import random

def generate_members(amount: int) -> list[dict]:
    members = []
    
    # Email providers to fill the fake email addresses.
    email_providers = [
        "@gmail.com", "@outlook.com",
        "@icloud.com", "@protonmail.com",
        "@mail.aol.com", "@mail.yandex.com"
    ]

    # Iterate through a set amount of 
    for x in range(amount):
        forename = names.get_first_name()
        surname = names.get_last_name()
        email = f"{forename}{surname}{random.choice(email_providers)}"
        phone = PhoneNumber("GB").get_mobile()
        
        members.append({
            "forename": forename,
            "surname": surname,
            "email": email,
            "phone": phone
        })
        
    return members

def add_to_database(members: list[dict], table: str):
    connection = sqlite3.connect("data/gym.sqlite")
    cursor = connection.cursor()
    
    for member in members:
        forename = member["forename"]
        surname = member["surname"]
        email = member["email"]
        phone = member["phone"]
        
        query = (
            f"INSERT INTO {table}"
            "(forename, surname, email, phone)"
            "VALUES (?, ?, ?, ?)"
        )
        
        cursor.execute(
            query,
            (
                forename,
                surname,
                email,
                phone
            )
        )
        
        connection.commit()

    connection.close()

add_to_database(generate_members(100), "members")