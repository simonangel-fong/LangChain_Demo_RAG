from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_aws import BedrockEmbeddings, ChatBedrockConverse
from langchain_core.messages import SystemMessage, HumanMessage


# =========================
# Config
# =========================
FILE_URL = 'https://www.upl-ltd.com/images/people/downloads/Leave-Policy-India.pdf'
AWS_PROFILE = "default"
AWS_REGION = "us-east-1"

EMBEDDING_MODEL_ID = "amazon.titan-embed-text-v1"
CHATBOT_MODEL_ID = "anthropic.claude-haiku-4-5-20251001-v1:0"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 3


# =========================
# Ingestion
# =========================
def load_pdf(file_path: str):
    """Load PDF and return LangChain documents."""
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    return docs


def split_documents(docs, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP):
    """Split documents into chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    chunks = text_splitter.split_documents(docs)
    return chunks


def create_embeddings():
    """Create Bedrock embeddings client."""
    return BedrockEmbeddings(
        model_id=EMBEDDING_MODEL_ID,
        credentials_profile_name=AWS_PROFILE,
        region_name=AWS_REGION,
    )


def build_vectorstore(chunks, embeddings):
    """Create FAISS vector store from chunks."""
    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore


def build_retriever(vectorstore, k: int = TOP_K):
    """Create retriever from vector store."""
    return vectorstore.as_retriever(search_kwargs={"k": k})


# =========================
# LLM
# =========================
def create_llm():
    """Create Bedrock chat model client."""
    return ChatBedrockConverse(
        model=CHATBOT_MODEL_ID,
        credentials_profile_name=AWS_PROFILE,
        region_name=AWS_REGION,
        temperature=0,
    )


# =========================
# Retrieval + Prompt
# =========================
def retrieve_documents(retriever, question: str):
    """Retrieve relevant documents for a user question."""
    return retriever.invoke(question)


def format_context(retrieved_docs):
    """Format retrieved docs into a context string for the LLM."""
    context_text = "\n\n".join(
        [
            f"Page {doc.metadata.get('page')}: {doc.page_content}"
            for doc in retrieved_docs
        ]
    )
    return context_text


def build_messages(question: str, context_text: str):
    """Build system and user messages for the LLM."""
    return [
        SystemMessage(
            content=(
                "You are a helpful assistant for question answering over a PDF. "
                "Answer only from the provided context. "
                "Do not infer beyond the context. "
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

Answer the question directly and briefly.
If possible, mention the relevant page number.
"""
        ),
    ]


def generate_answer(llm, messages):
    """Invoke the LLM and return the answer text."""
    response = llm.invoke(messages)
    return response


# =========================
# End-to-end RAG
# =========================
def setup_rag(file_path: str):
    """Run ingestion once and return reusable objects."""
    docs = load_pdf(file_path)
    chunks = split_documents(docs)
    embeddings = create_embeddings()
    vectorstore = build_vectorstore(chunks, embeddings)
    retriever = build_retriever(vectorstore)
    llm = create_llm()

    return {
        "docs": docs,
        "chunks": chunks,
        "embeddings": embeddings,
        "vectorstore": vectorstore,
        "retriever": retriever,
        "llm": llm,
    }


def ask_question(question: str, retriever, llm, show_sources: bool = True):
    """Run retrieval + generation for one question."""
    retrieved_docs = retrieve_documents(retriever, question)
    context_text = format_context(retrieved_docs)
    messages = build_messages(question, context_text)
    response = generate_answer(llm, messages)

    print("ANSWER:")
    print(response.content)

    if show_sources:
        print("\nSOURCES:")
        for i, doc in enumerate(retrieved_docs, 1):
            print("=" * 80)
            print(f"Result {i} | Page: {doc.metadata.get('page')}")
            print(doc.page_content[:500])

    return response, retrieved_docs


# =========================
# Main
# =========================
if __name__ == "__main__":
    rag = setup_rag(FILE_URL)

    print(f"Loaded pages: {len(rag['docs'])}")
    print(f"Created chunks: {len(rag['chunks'])}")

    ask_question(
        question="Who is covered by this leave policy?",
        retriever=rag["retriever"],
        llm=rag["llm"],
        show_sources=True,
    )
