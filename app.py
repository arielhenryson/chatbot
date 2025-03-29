from dotenv import load_dotenv
load_dotenv()
import os
from typing import Dict, Optional
import chainlit as cl
import chainlit.data as cl_data
from history import push_msg_to_db
from mongo_datalayer import MongoDBDataLayer

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
async def main(message: cl.Message):
    await push_msg_to_db(message.content, "user_message")
    # Your custom logic goes here...

    ai_msg = f"Received: {message.content}"

    await push_msg_to_db("Received: " + message.content, "assistant_message")

    # Send a response back to the user
    await cl.Message(
        content=ai_msg,
    ).send()

if __name__ == "__main__":
    from chainlit.cli import run_chainlit
    run_chainlit(__file__)