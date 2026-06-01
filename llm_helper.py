from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os

load_dotenv()  # ✅ this must come first

llm = ChatGroq(model="llama-3.3-70b-versatile")

if __name__ == "__main__":
    response = llm.invoke("What are the two main ingredients in samosa")
    print(response.content)