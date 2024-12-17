
from pydantic import BaseModel
from typing import Optional
import logging
import os
from email_validator import validate_email, EmailNotValidError
from dotenv import load_dotenv

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


def _config():
    # Use the correct file path
    load_dotenv()
    URI = os.getenv("URI")
    # Create a new client and connect to the server
    client = MongoClient(URI, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    return client


def process_user(dbres):
        # For now let's assume only one page is associated to the user (BAD, need to scale)
        # Means that dbres len == 1
        if not dbres: return 
        
        return UserInDB(
            username=dbres.get("username"),
            email=dbres.get("email"),
            full_name=dbres.get("full_name"),
            disabled=dbres.get("disabled"),
            notion_token=dbres.get("hashed_notion_token"),
            permitted_pages=dbres.get("permitted_pages", []),
            hashed_password=dbres.get("hashed_password")
        )

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    notion_token: str | None = None
    permitted_pages: list[str] | None = None


class UserInDB(User):
    hashed_password: str


class MongoDbManager(BaseModel):
    def register_user(self, 
                      username: str, 
                      email: str, 
                      hashed_password: str, 
                      hashed_notion_token: str, 
                      disabled: Optional[bool] = False, 
                      full_name: Optional[str] = None):
        # Setup logging
        logging.basicConfig(filename='./logs/db_errors.log', level=logging.ERROR)

        try:
            valid = validate_email(email, check_deliverability=True)
            email = valid.email  # Extract the normalized email address
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email: {e}")

        connection = _config()
        db = connection["fruitsdb"]
        collection = db["users"]
        # Inserting the record
        record = {
            "username": username,
            "email": email,
            "full_name": full_name,
            "hashed_password": hashed_password,
            "disabled": disabled,
            "hashed_notion_token": hashed_notion_token,
            "permitted_pages": []
        }
        collection.insert_one(record)
        print("Record inserted successfully")
        


    def get_user(self, username: str):
        connection = _config()
        db = connection["fruitsdb"]
        collection = db["users"]
        record = collection.find_one({"username": username})
        return process_user(record)


    def register_users(self):
        pass

    def insert_permitted_page(user_id, page_id):
        pass
