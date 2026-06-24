from openai import OpenAI
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel # allows us to define data models for request and response bodies
from fastapi.middleware.cors import CORSMiddleware

# OpenAI class will automatically read the OPENAI_API_KEY from your environment variables
load_dotenv()
app = FastAPI()
client = OpenAI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace "*" with your specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# No longer need root if React app is being used as frontend. 
# React will handle the root route and FastAPI will handle the API routes.
# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

class ChatRequest(BaseModel):
    message: str

# Post can only be activated from the frontend. 
# This is where the user will send their recipe question to the backend.

@app.post("/chat")
async def chat(body: ChatRequest):
    print(body.message)
    
    input_text = body.message
    
    # Corrected OpenAI SDK call
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            # 1. The System Prompt sets the behavior, constraints, and rules
            {
                "role": "system", 
                "content": (
                    "You are an expert chef and culinary assistant. Your only job is to provide "
                    "clear, accurate, and delicious recipes based on the user's request. "
                    "Always format your response with a Title, Prep Time, Cook Time, Ingredients List (with measurements), "
                    "and Step-by-Step Instructions. If the user asks for something that isn't a food recipe, "
                    "politely remind them that you only cook up recipes."
                )
            },
            # 2. The User Prompt delivers the actual ingredient or dish request
            {
                "role": "user", 
                "content": f"Please give me a great recipe for: {input_text}"
            }
        ],
        temperature=0.7 # Optional: 0.7 gives a good balance of creativity and reliability for food
    )
    
    # Corrected way to extract the text response
    reply = response.choices[0].message.content
    
    return {"output": reply}

# Only running main() function when running main.py file
# You see this when you write python modules 
# if __name__ == "__main__":