```sh
python -m venv .venv
python.exe -m pip install --upgrade pip
pip install boto3 langchain fastapi sqlalchemy "fastapi[standard]" pypdf faiss-cpu
pip install -qU langchain-community pypdf
pip install langchain-aws
pip install faiss-cpu
```

data injection workflow

Key Steps:

1. Load data: load pdf and split by page
2. Transform: split data by character
3. Create Embedings
4. Store & index: vector store
