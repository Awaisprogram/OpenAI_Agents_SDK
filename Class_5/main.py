import os
from agents import Runner, Agent, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv
import chainlit as cl

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

provider = AsyncOpenAI(
  api_key = gemini_api_key,
  base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
  model = "gemini-2.0-flash",
  openai_client = provider,
)

config = RunConfig(
  model = model,
  model_provider = provider,
  tracing_disabled = True,
)

agent = Agent(
  name = "Streaming Agent",
  instructions = "You are helpful agent help with user quries",
  model = model
)

@cl.on_chat_start
async def handle_chat():
  cl.user_session.set("history", [])
  await cl.Message(content = "Hello, How can I help you today?").send()

@cl.on_message
async def handle_message(message: cl.Message):
  history = cl.user_session.get("history")
  msg = cl.Message(content= "")
  await msg.send()

  history.append(
    {
      "role" : "user",
      "content" : message.content
      }
  )
  result = Runner.run_streamed(
    agent,
    input = history,
    run_config = config
  )
  async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            await msg.stream_token(event.data.delta)

  history.append(
    {
      "role" : "assistant",
      "content" : result.final_output
      }
  )
  cl.user_session.set("history", history)

  
