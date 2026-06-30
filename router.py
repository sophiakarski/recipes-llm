from pydantic import BaseModel # allows us to define data models for request and response bodies
from datetime import datetime, timezone # <-- Added for human-readable timestamp
from motor.motor_asyncio import AsyncIOMotorClient # <-- Added for MongoDB
from dotenv import load_dotenv
import os
from fastapi import APIRouter
from openai import OpenAI

load_dotenv()
router = APIRouter()
client = OpenAI()
# No longer need root if React app is being used as frontend. 
# React will handle the root route and FastAPI will handle the API routes.
# @router.get("/")
# def read_root():
#     return {"Hello": "World"}

# 1. Setup your MongoDB Connection by pulling from environment variables
MONGO_DETAILS = os.getenv("MONGO_URI")

# Safety Check: ensure the environment variable was actually found
if not MONGO_DETAILS:
    raise ValueError("Critical Error: MONGO_URI environment variable is missing!")

mongo_client = AsyncIOMotorClient(MONGO_DETAILS)
db = mongo_client.recipe_app
recipe_history_collection = db.get_collection("recipe_history")

class ChatRequest(BaseModel):
    message: str
    
# Post can only be activated from the frontend. 
# This is where the user will send their recipe question to the backend.
 
@router.post("/chat")
async def chat(body: ChatRequest):
    print(body.message)
    input_text = body.message
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system", 
                "content": (
                    "You are an expert chef and culinary assistant. Your only job is to provide "
                    "clear, accurate, and delicious recipes based on the user's request. "
                    "Always format your response with a Title, Prep Time, Cook Time, Ingredients List (with measurements), "
                    "and Step-by-Step Instructions. If the user asks for something that isn't a food recipe, "
                    "politely remind them that you only cook up recipes."
                    "Respond with British English spelling and measurements."
                )
            },
            {"role": "user", "content": f"Please give me a great recipe for: {input_text}"}
        ],
        temperature=0.7
    )
    
    reply = response.choices[0].message.content
    
    # 2. Convert OpenAI Unix timestamp to human-readable format (e.g., "2026-06-25 19:31:33 UTC")
    readable_timestamp = datetime.fromtimestamp(response.created, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z')
    
    # 3. Create the document structure to insert into MongoDB
    history_document = {
        "user_request": input_text,
        "ai_response": reply,
        "timestamp": readable_timestamp
    }
    
    # 4. Save to MongoDB (use await because Motor is asynchronous)
    await recipe_history_collection.insert_one(history_document)
    
    # Return the clean data to your frontend
    return {
        "output": reply,
        "timestamp": readable_timestamp
    }