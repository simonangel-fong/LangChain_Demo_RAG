from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_aws import BedrockEmbeddings
from langchain_community.vectorstores import FAISS

FILE_URL = 'https://www.upl-ltd.com/images/people/downloads/Leave-Policy-India.pdf'

# 1. Load PDF
loader = PyPDFLoader(FILE_URL)
docs = loader.load()

# 2. Split documents
text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", " ", ""],
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(docs)

# 3. Bedrock embeddings
embeddings = BedrockEmbeddings(
    model_id="amazon.titan-embed-text-v1",
    credentials_profile_name="default",
    region_name="us-east-1"
)

vectorstore = FAISS.from_documents(chunks, embeddings)

print("vector store created")

# 5. Test similarity search
query = "What is the leave policy for annual leave?"
results = vectorstore.similarity_search(query, k=3)

print(f"top results: {len(results)}")
# top results: 3


# for i, doc in enumerate(results, 1):
#     print("\n" + "=" * 80)
#     print(f"Result {i}")
#     print("Metadata:", doc.metadata)
#     print("Content:")
#     print(doc.page_content[:500])

# ================================================================================
# Result 1
# Metadata: {'producer': 'PDFium', 'creator': 'PDFium', 'creationdate': 'D:20210727120109', 'keywords': 'Classification=t_class_2', 'source': 'https://www.upl-ltd.com/images/people/downloads/Leave-Policy-India.pdf', 'total_pages': 8, 'page': 4, 'page_label': '5'}
# Content:
# every year. 
     
# In order to rest and recuperate, all employees will have 21 working days of privilege leave 
# in a calendar year. It is expected that employees take their privilege leave and spend some 
# quality time with family and friends or to develop a hobby or just to rest and relax.  
 
# There is no leave encashment available for unutilized or lapsed leave except when employee 
# separates due to resignation, termination of employment, superannuation, or demise of an 
# employee.

# ================================================================================
# Result 2
# Metadata: {'producer': 'PDFium', 'creator': 'PDFium', 'creationdate': 'D:20210727120109', 'keywords': 'Classification=t_class_2', 'source': 'https://www.upl-ltd.com/images/people/downloads/Leave-Policy-India.pdf', 'total_pages': 8, 'page': 7, 'page_label': '8'}
# Content:
# not sent the leave application, it tantamount to misconduct and may lead to disciplinary
#   action.
# b)  Leave period for all leave type is calendar year, i.e, 1st January to 31st December.
#  c)  New hires will have their leave entitlements pro-rated from the date of hire till 31st
#   December
# d)  Any unauthorized leave will result in loss of pay.
# e)        Note that UPL is currently in the process of launching a digital leave management tool

# ================================================================================
# Result 3
# Metadata: {'producer': 'PDFium', 'creator': 'PDFium', 'creationdate': 'D:20210727120109', 'keywords': 'Classification=t_class_2', 'source': 'https://www.upl-ltd.com/images/people/downloads/Leave-Policy-India.pdf', 'total_pages': 8, 'page': 3, 'page_label': '4'}
# Content:
# 1. Purpose
# The objective is to provide information to all the employees about the leaves and
# holidays followed in UPL India. Employees need adequate time to celebrate festival
# holidays, rest and recuperate and spend quality time with family and friends. This policy
# is effective from 1st October 2020.

# 2. Scope
# All permanent employees, trainees, will be covered by this leave policy except the
# manufacturing employees in “worker” category with specific employment conditions.

# 6. test Retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

retrieved_docs = retriever.invoke("Who is eligible for leave?")
print(f"\nretriever returned: {len(retrieved_docs)} documents")
# retriever returned: 3 documents