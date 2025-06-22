import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel,RunConfig
import chainlit as cl



load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

provider = AsyncOpenAI(
  api_key=gemini_api_key, 
  base_url="https://generativelanguage.googleapis.com/v1beta/openai",
)

model = OpenAIChatCompletionsModel(
  model = "gemini-2.0-flash",
  openai_client = provider
)

config = RunConfig(
    model=model,
    model_provider= provider,
    tracing_disabled=True
)

agent = Agent(
  name = "Chainlit agent",
  instructions = "You are an agent that helps users",
  model = model
)


@cl.on_chat_start
async def handle_chat_start():

    cl.user_session.set("history", [])  

    await cl.Message(
        content="Hello! How can I help you today?"
    ).send()  

@cl.on_message
async def handle_message(message: cl.Message):
    result = await Runner.run(
        agent,
        input=message.content,
        run_config=config
    )
    await cl.Message(content=result.final_output).send()