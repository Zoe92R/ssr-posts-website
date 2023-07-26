from typing import Union
from fastapi import FastAPI, HTTPException, Query, Response
import json

from models import HPData, PostsData , PostData

app = FastAPI()


with open("data/hpdata.json", "r") as json_file:
    hp_data = json.load(json_file)

with open("data/postsdata.json", "r") as json_file:
    posts_data = json.load(json_file)


@app.get("/get_hp_data", response_model=HPData)
def read_hp_data():
    response_data = {"res": "OK", "data": hp_data}
    return Response(content=json.dumps(response_data), media_type="application/json")

@app.get("/get_posts", response_model=PostsData)
def read_posts_data():
    response_data = {"res": "OK", "data": posts_data}
    return Response(content=json.dumps(response_data), media_type="application/json")

@app.get("/get_post", response_model=PostData)
def read_item(id: int = Query(..., description="Item ID")):
    for item in posts_data:
        if item["id"] == id:
            response_data = {"res": "OK", "data": item}
            return Response(content=json.dumps(response_data), media_type="application/json")
    # If the item with the specified ID is not found, raise an HTTP 404 Not Found error
    raise HTTPException(status_code=404, detail="Item not found")
