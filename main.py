from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from router import router
import uuid

# OpenAI class will automatically read the OPENAI_API_KEY from your environment variables
load_dotenv()
app = FastAPI()

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace "*" with your specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Only running main() function when running main.py file
# You see this when you write python modules 
# if __name__ == "__main__":