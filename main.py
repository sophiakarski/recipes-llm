from openai import OpenAI
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel # allows us to define data models for request and response bodies

# OpenAI class will automatically read the OPENAI_API_KEY from your environment variables
load_dotenv()
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

class ChatRequest(BaseModel):
    recipe_question: str

@app.post("/chat/")
def chat(req: ChatRequest):
    
    client = OpenAI()
    
    input_text = req.recipe_question
    
    response = client.responses.create(
        model="gpt-5.5",
        input=input_text
    )

    return {"output": response.output_text}

# Only running main() function when running main.py file
# You see this when you write python modules 
# if __name__ == "__main__":