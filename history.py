import uuid
import chainlit as cl
import chainlit.data as cl_data
from literalai.helper import utc_now

async def push_msg_to_db(text: str, type: str):
  random_id = str(uuid.uuid4())

  print(cl.context.session.thread_id)

  await cl_data._data_layer.create_step({
    "id": random_id,
    "threadId": cl.context.session.thread_id,
    "type": type,
    "createdAt": utc_now(),
    "output": text,
    "push": True
  })