from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_aws import BedrockEmbeddings, ChatBedrockConverse
from langchain_core.messages import SystemMessage, HumanMessage

FILE_URL = 'https://www.upl-ltd.com/images/people/downloads/Leave-Policy-India.pdf'

# 1. Load PDF
loader = PyPDFLoader(FILE_URL)
docs = loader.load()

# 2. Split
text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", " ", ""],
    chunk_size=500,
    chunk_overlap=50
)
chunks = text_splitter.split_documents(docs)

# 3. Embeddings
embeddings = BedrockEmbeddings(
    model_id="amazon.titan-embed-text-v1",
    credentials_profile_name="default",
    region_name="us-east-1"
)

# 4. Vector store
vectorstore = FAISS.from_documents(chunks, embeddings)

# 5. Retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 6. Claude Haiku
llm = ChatBedrockConverse(
    model="us.anthropic.claude-haiku-4-5-20251001-v1:0",
    credentials_profile_name="default",
    region_name="us-east-1",
    temperature=0,
)

# 7. User question
question = "Who is covered by this leave policy?"

# 8. Retrieve relevant chunks
retrieved_docs = retriever.invoke(question)
print(retrieved_docs)

# 9. Build context string
context_text = "\n\n".join(
    [
        f"Page {doc.metadata.get('page')}: {doc.page_content}"
        for doc in retrieved_docs
    ]
)
print(context_text)
# Page 6: employee must apply the sick leave in the prescribed online platform immediately on return to 
# work.

# Any misuse of the sick leave provision will attract disciplinary action and may lead to termination
# of an employee.

# 4.5 Maternity Leave

# Eligibility - Total of 26 weeks twice in the service tenure as governed by ‘The Maternity
# Benefit Act” & Maternity Benefit (amendment) Bill 2017.
# Apart from the standard Maternity leaves mentioned above, women will be

# Page 4: proceeding on leave desires an extension thereof, he/she shall make an application in writing
# to the company for this purpose.
# 5. The Management reserves the right to reject or extend the leave at its discretion and without
# assigning any reason whatsoever.
# 6. When an employee takes a PL, weekend and other holidays will not be included while
# calculating leave.
# 7. In the event of the an employee resigning, retrenchment or termination of services by the

# Page 6: pregnancy/ or leave for miscarriage, the request for such leave needs to be forwarded to
# immediate supervisor along with supporting medical documents.
#  On approval of the leave, the leave details are to be updated along with necessary
# documents in the leave management system.

# 10. Prompt Claude with retrieved context
messages = [
    SystemMessage(
        content=(
            "You are a helpful assistant for question answering over a PDF. "
            "Answer only from the provided context. "
            "If the answer is not in the context, say: "
            "'I do not know based on the provided document.'"
        )
    ),
    HumanMessage(
        content=f"""
Context:
{context_text}

Question:
{question}

Please answer clearly and briefly.
"""
    ),
]
print(messages)
# [SystemMessage(content="You are a helpful assistant for question answering over a PDF. Answer only from the provided context. If the answer is not in the context, say: 'I do not know based on the provided document.'", additional_kwargs={}, response_metadata={}), HumanMessage(content='\nContext:\nPage 6: employee must apply the sick leave in the prescribed online platform immediately on return to \nwork. \n \nAny misuse of the sick leave provision will attract disciplinary action and may lead to termination \nof an employee. \n \n4.5 Maternity Leave  \n \nEligibility - Total of 26 weeks twice in the service tenure as governed by ‘The Maternity \nBenefit Act” & Maternity Benefit (amendment) Bill 2017.  \nApart from the standard Maternity leaves mentioned above, women will be\n\nPage 4: proceeding on leave desires an extension thereof, he/she shall make an application in writing \nto the company for this purpose. \n5. The Management reserves the right to reject or extend the leave at its discretion and without \nassigning any reason whatsoever. \n6. When an employee takes a PL, weekend and other holidays will not be included while \ncalculating leave. \n7. In the event of the an employee resigning, retrenchment or termination of services by the\n\nPage 6: pregnancy/ or leave for miscarriage, the request for such leave needs to be forwarded to \nimmediate supervisor along with supporting medical documents. \n\uf0b7 On approval of the leave, the leave details are to be updated along with necessary \ndocuments in the leave management system.\n\nQuestion:\nWho is eligible for leave?\n\nPlease answer clearly and briefly.\n', additional_kwargs={}, response_metadata={})]

response = llm.invoke(messages)
print(response)
# content='Based on the provided context, the following employees are eligible for leave:\n\n1. Employees are eligible for sick leave, which they must apply for immediately on return to work through the prescribed online platform. Misuse of sick leave can lead to disciplinary action and termination.\n\n2. Employees are eligible for maternity leave, with a total of 26 weeks of maternity leave twice during their service tenure, as governed by the Maternity Benefit Act and Maternity Benefit (Amendment) Bill 2017.\n\n3. Employees can apply for an extension of their personal leave, and the management reserves the right to reject or extend the leave at its discretion.\n\n4. Employees who are proceeding on leave can request an extension in writing to the company.\n\nI do not have enough information from the provided context to determine if there are any other types of leave that employees are eligible for.' additional_kwargs={} response_metadata={'ResponseMetadata': {'RequestId': '6cf6c80d-37b7-45f4-8d13-e7156e672962', 'HTTPStatusCode': 200, 'HTTPHeaders': {'date': 'Wed, 08 Apr 2026 21:49:00 GMT', 'content-type': 'application/json', 'content-length': '1107', 'connection': 'keep-alive', 'x-amzn-requestid': '6cf6c80d-37b7-45f4-8d13-e7156e672962'}, 'RetryAttempts': 0}, 'stopReason': 'end_turn', 'metrics': {'latencyMs': [2212]}, 'model_provider': 'bedrock_converse', 'model_name': 'anthropic.claude-3-haiku-20240307-v1:0'} id='lc_run--019d6f11-ea15-7760-8fe4-1392b5828a22-0' tool_calls=[] invalid_tool_calls=[] usage_metadata={'input_tokens': 377, 'output_tokens': 194, 'total_tokens': 571, 'input_token_details': {'cache_creation': 0, 'cache_read': 0}}

# 11. Print answer
print("ANSWER:")
print(response.content)
# ANSWER:
# Based on the provided context, the following employees are eligible for leave:

# 1. Employees are eligible for sick leave, which they must apply for immediately on return to work through the prescribed online platform. Misuse of sick leave can lead to disciplinary action and termination.

# 2. Eligible female employees are entitled to 26 weeks of maternity leave, twice during their service tenure, as governed by the Maternity Benefit Act and Maternity Benefit (Amendment) Bill 2017.

# 3. Employees who are proceeding on leave can apply in writing to the company for an extension, which the management reserves the right to reject or extend at its discretion.

# 4. Employees who are taking personal leave (PL) will not have weekends and other holidays included in the calculation of their leave.

# I do not have enough information in the provided context to determine if there are any other types of leave that employees are eligible for.


# 12. Print sources
print("\nSOURCES:")
for i, doc in enumerate(retrieved_docs, 1):
    print("=" * 80)
    print(f"Result {i} | Page: {doc.metadata.get('page')}")
    print(doc.page_content[:500])
# ANSWER:

# SOURCES:
# ================================================================================
# Result 1 | Page: 6
# employee must apply the sick leave in the prescribed online platform immediately on return to
# work.

# Any misuse of the sick leave provision will attract disciplinary action and may lead to termination
# of an employee.

# 4.5 Maternity Leave

# Eligibility - Total of 26 weeks twice in the service tenure as governed by ‘The Maternity
# Benefit Act” & Maternity Benefit (amendment) Bill 2017.
# Apart from the standard Maternity leaves mentioned above, women will be
# ================================================================================
# Result 2 | Page: 4
# proceeding on leave desires an extension thereof, he/she shall make an application in writing
# to the company for this purpose.
# 5. The Management reserves the right to reject or extend the leave at its discretion and without
# assigning any reason whatsoever.
# 6. When an employee takes a PL, weekend and other holidays will not be included while
# calculating leave.
# 7. In the event of the an employee resigning, retrenchment or termination of services by the
# ================================================================================
# Result 3 | Page: 6
# pregnancy/ or leave for miscarriage, the request for such leave needs to be forwarded to
# immediate supervisor along with supporting medical documents.
#  On approval of the leave, the leave details are to be updated along with necessary
# documents in the leave management system.