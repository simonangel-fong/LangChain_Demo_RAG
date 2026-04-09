from langchain_aws import ChatBedrockConverse
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatBedrockConverse(
    model="us.anthropic.claude-haiku-4-5-20251001-v1:0",
    credentials_profile_name="default",
    region_name="us-east-1",
    temperature=0,
)

response = llm.invoke([
    SystemMessage(content="You are a concise assistant."),
    HumanMessage(content="What is RAG?")
])

print(response.content)
