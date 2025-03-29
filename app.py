from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()
import os
from typing import Dict, Optional
import chainlit as cl
import chainlit.data as cl_data
from history import push_msg_to_db
from mongo_datalayer import MongoDBDataLayer
from langchain_core.messages import HumanMessage, AIMessage
from langchain.schema.runnable.config import RunnableConfig

llm = ChatGoogleGenerativeAI(
   model="gemini-1.5-flash",
)

cl_data._data_layer = MongoDBDataLayer(os.getenv("MONGODB_URI"), "chainlit_db") # type: ignore

@cl.oauth_callback
def oauth_callback(
  provider_id: str,
  token: str,
  raw_user_data: Dict[str, str],
  default_user: cl.User,
) -> Optional[cl.User]:
  return default_user

@cl.on_message
async def main(msg: cl.Message):
    await push_msg_to_db(msg.content, "user_message")
    
    response = llm.invoke(msg.content)

    await cl.Message(content=response.content).send()

    await push_msg_to_db(response.content, "assistant_message")

if __name__ == "__main__":
    from chainlit.cli import run_chainlit
    run_chainlit(__file__)