# Post Website Server - Python
This is the server application for the Post Website, built using Python, FastAPI and mysql. 

You can find the client code here: [https://github.com/Zoe92R/ssr-posts-website-client](https://github.com/Zoe92R/ssr-posts-website-client). 

# Prerequisites
Before running this project, ensure you have the following prerequisites installed:

- Python
- uvicorn
- mysql-connector-python

# Installation

- Set MySQL:

Make sure you have MySQL installed on your system. If not, download and install MySQL from https://www.mysql.com/.

- Create a MySQL Schema:

After installing MySQL, create a new schema (database) named "post_schema". You can do this using a MySQL management tool or the MySQL command line.
Configure MySQL Connection:

Open the "create_and_load.py" file in the server directory using a text editor.
Look for the "db_config" dictionary in the file and replace the placeholders with your actual MySQL database credentials (hostname, username, and password).

- Create and Load Data:

In the terminal, navigate to the project directory (server directory).
Run the following command to create and load data into the "post_schema" schema:

```bash
python create_and_load.py
```

- Configure MySQL Connection in main.py:

Open the "main.py" file in the server directory.
Find the "db_config" dictionary and replace the placeholders with your actual MySQL database credentials (hostname, username, and password).

- To run the server, navigate to the server directory and run the following command:

```bash
python -m uvicorn main:app --reload
```

Uvicorn will run on http://127.0.0.1:8000
