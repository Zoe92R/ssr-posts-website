import json
from typing import List
from fastapi import FastAPI, HTTPException, Query, Response
from pydantic import BaseModel
import mysql.connector

from models import CreatePost, HPData, Post, PostDataRes, PostsDataRes

app = FastAPI()

with open("data/hpdata.json", "r") as json_file:
    hp_data = json.load(json_file)

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "cFRvK#uJH?!I06",
    "database": "post4_schema",
}

def get_connection():
    return mysql.connector.connect(**db_config)

def execute_query(query, *args):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, args)
        return connection, cursor
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error")

# Get Home Page data
@app.get("/get_hp_data", response_model=HPData)
def read_hp_data():
    response_data = {"res": "OK", "data": hp_data}
    return Response(content=json.dumps(response_data), media_type="application/json")

# Get Posts list
@app.get("/get_posts", response_model=PostsDataRes)
def get_data_from_database():
    query = "SELECT * FROM posts_data"
    connection, cursor = execute_query(query)
    try:
        result = cursor.fetchall()

        # Convert the result into the desired format
        formatted_data = []
        for row in result:
            formatted_data.append({
                "id": row[0],
                "title": row[1],
                "content": row[2]
            })

        response = {
            "res": "OK",
            "data": formatted_data
        }

        return response

    finally:
        cursor.close()
        connection.close()

# Get post by id
@app.get("/get_post/", response_model=PostDataRes)
async def read_post(id: str = Query(..., description="The ID of the post to retrieve")):
    try:
        post_id = int(id)  # Convert the id from string to int
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid id format")

    query = "SELECT id, title, content FROM posts_data WHERE id = %s"
    connection, cursor = execute_query(query, post_id)
    try:
        post = cursor.fetchone()

        if post is None:
            raise HTTPException(status_code=404, detail="Post not found")

        return PostDataRes(
            res="OK",
            data=Post(id=post[0], title=post[1], content=post[2])
        )

    finally:
        cursor.close()
        connection.close()

# Helper function - Get id number for new post
def get_next_post_id():
    query = "SELECT MAX(id) FROM posts_data"
    connection, cursor = execute_query(query)
    try:
        max_id = cursor.fetchone()[0]
        next_id = max_id + 1 if max_id is not None else 1

        return next_id

    finally:
        cursor.close()
        connection.close()

# Create new post
@app.post("/posts", response_model=PostDataRes)
async def create_post(post: CreatePost):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Get the next continuous id for the new post
        post_id = get_next_post_id()

        # Create a new post in the database with the generated id
        query = "INSERT INTO posts_data (id, title, content) VALUES (%s, %s, %s)"
        cursor.execute(query, (post_id, post.title, post.content))
        connection.commit()

        new_post = Post(id=post_id, title=post.title, content=post.content)
        return PostDataRes(
            res="OK",
            data=new_post
        )

    finally:
        cursor.close()
        connection.close()

# Update post
@app.put("/posts/{post_id}", response_model=PostDataRes)
async def update_post(post_id: int, post: CreatePost):
    query = "SELECT id FROM posts_data WHERE id = %s"
    connection, cursor = execute_query(query, post_id)
    try:
        existing_post = cursor.fetchone()
        if not existing_post:
            raise HTTPException(status_code=404, detail="Post not found")

        query = "UPDATE posts_data SET title = %s, content = %s WHERE id = %s"
        cursor.execute(query, (post.title, post.content, post_id))
        connection.commit()

        updated_post = Post(id=post_id, title=post.title, content=post.content)
        return PostDataRes(
            res="OK",
            data=updated_post
        )

    finally:
        cursor.close()
        connection.close()

# Delete post
@app.delete("/posts/{post_id}", response_model=dict)
async def delete_post(post_id: int):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Get the post data before deleting
        query = "SELECT id, title, content FROM posts_data WHERE id = %s"
        cursor.execute(query, (post_id,))
        post_data = cursor.fetchone()

        if post_data is None:
            raise HTTPException(status_code=404, detail="Post not found")

        # Delete the post
        delete_query = "DELETE FROM posts_data WHERE id = %s"
        cursor.execute(delete_query, (post_id,))
        connection.commit()

        return {"message": "Post deleted successfully"}

    finally:
        cursor.close()
        connection.close()
