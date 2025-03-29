from dotenv import load_dotenv
load_dotenv()
import os
from typing import Dict, Optional
import chainlit as cl
import chainlit.data as cl_data
from history import push_msg_to_db
from mongo_datalayer import MongoDBDataLayer
from langchain_core.messages import HumanMessage, AIMessage
from langchain.schema.runnable.config import RunnableConfig

os.environ["GOOGLE_API_KEY"] = "AIzaSyAc9UQ5uKUrjIa_cG0XdmRiJ6S_mhsUGVU"
cl_data._data_layer = MongoDBDataLayer(os.getenv("MONGODB_URI"), "chainlit_db") # type: ignore

from flow import graph

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
    # await push_msg_to_db(message.content, "user_message")
    # # Your custom logic goes here...
    config = {"configurable": {"thread_id": cl.context.session.id}}
    cb = cl.LangchainCallbackHandler()
    final_answer = cl.Message(content="")

    config = {"configurable": {"thread_id": cl.context.session.id}}
    cb = cl.LangchainCallbackHandler()
    final_answer = cl.Message(content="")
    
    for msg, metadata in graph.stream({"messages": [HumanMessage(content=msg.content)]}, stream_mode="messages", config=RunnableConfig(callbacks=[cb], **config)):
        if (
            msg.content
            and not isinstance(msg, HumanMessage)
            and metadata["langgraph_node"] == "final"
        ):
            await final_answer.stream_token(msg.content)

    await final_answer.send()

    

     # LangGraph integration
    # await push_msg_to_db(msg.content, "assistant_message")

if __name__ == "__main__":
    from chainlit.cli import run_chainlit
    run_chainlit(__file__)