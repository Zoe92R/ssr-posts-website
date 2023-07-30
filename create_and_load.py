import json
import mysql.connector
from mysql.connector import Error

# Please enter your MySQL details and ensure that you create a schema named 'post_schema'
db_config = {
    "host": "<host>",
    "user": "<user_name>",
    "password": "<password>",
    "database": "post_schema",
}

json_file_path = "data/postsdata.json"
table_name = "posts_data"

def create_schema():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Create the schema (database)
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {db_config['database']}")

        print("Schema created successfully!")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def load_data_to_table():
    try:
        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Create the table if it does not exist
        create_table_query = (
            f"CREATE TABLE IF NOT EXISTS {db_config['database']}.{table_name} "
            "(id INT PRIMARY KEY, title VARCHAR(255), content TEXT)"
        )
        cursor.execute(create_table_query)

        # Truncate the table to remove any existing data (optional)
        truncate_query = f"TRUNCATE TABLE {db_config['database']}.{table_name}"
        cursor.execute(truncate_query)

        # Insert the data into the table
        insert_query = f"INSERT INTO {db_config['database']}.{table_name} (id, title, content) VALUES (%s, %s, %s)"
        for item in data:
            cursor.execute(insert_query, (item["id"], item["title"], item["content"]))

        connection.commit()
        print("Data loaded successfully!")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    create_schema()
    load_data_to_table()
