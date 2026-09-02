from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    os.environ["OPENAI_API_KEY"] = api_key

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


response = llm.invoke(
    "Explain what a health insurance deductible is in simple terms."
)


print(response.content)