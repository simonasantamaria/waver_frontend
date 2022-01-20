import sys

import motor.motor_asyncio

from model import Todo

from dotenv import dotenv_values

config = dotenv_values(".env")
MONGODB_URI = config.get("MONGODB_URI")
print("MONGODB_URI",MONGODB_URI)



client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
print("client",client)
database = client.TodoList
collection = database.todo

async def fetch_one_todo(title):
    document = await collection.find_one({"title": title})
    return document

async def fetch_all_todos():
    todos = []
    cursor = collection.find({})
    async for document in cursor:
        todos.append(Todo(**document))
    return todos

async def create_todo(todo):
    document = todo
    result = await collection.insert_one(document)
    return document

async def update_todo(title, desc):
    await collection.update_one({"title": title}, {"$set": {"description": desc}})
    document = await collection.find_one({"title": title})
    return document

async def remove_todo(title):
    await collection.delete_one({"title": title})
    return True
