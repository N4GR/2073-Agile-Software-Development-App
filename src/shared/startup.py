# File to run as the program starts up.
import os
import sqlite3

from src.shared.funcs import path

def startup() -> bool:
    """A function usedd in startup to check if everything is working as it should be.

    Returns:
        bool: True on fail, False of pass.
    """
    required_databases = ["chat.sqlite", "gym.sqlite"]
    database_list = os.listdir(path("/data"))
    
    print(f"Searching for required files: {required_databases}")
    
    for file in database_list:
        if file in required_databases:
            required_databases.remove(file)
            
            print(f"Found required file: {file}")
    
    # If there's any still left in the required, create the database.
    for database in required_databases:
        database_name = database.replace(".sqlite", "")
        schema_path = path(f"/data/schemas/{database_name}.sql")
        
        print(f"Generating {database} from /data/schemas/{database_name}.sql")
        
        with open(schema_path, "r") as file:
            sql_query = file.read()
        
        # Get seperate queries from the file.
        sql_queries = sql_query.split("\n")
        
        # For each query, call the command.
        for query in sql_queries:
            # Create the database with a cursor.
            connection = sqlite3.connect(path(f"/data/{database}"))
            cursor = connection.cursor()
            
            print(query)
            
            # Try and execute the query from the schema to the database.
            cursor.execute(query)
            connection.commit()

        print(f"Successfully created: {database}")
    
    return False