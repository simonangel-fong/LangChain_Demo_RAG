from langchain_aws import BedrockEmbeddings

embeddings = BedrockEmbeddings(
    model_id="amazon.titan-embed-text-v1",
    credentials_profile_name="default",
    region_name="us-east-1"
)

vector = embeddings.embed_query("What is LangChain?")

print(f"embedding length: {len(vector)}")
print(vector[:5])
# embedding length: 1536
# [0.23046875, -0.4921875, -0.228515625, -0.0179443359375, 0.921875]