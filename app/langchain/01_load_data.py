from langchain_community.document_loaders import PyPDFLoader

FILE_URL = 'https://www.upl-ltd.com/images/people/downloads/Leave-Policy-India.pdf'

# 1. Load PDF
loader = PyPDFLoader(FILE_URL)
docs = loader.load()

print(f"pages loaded: {len(docs)}")
# pages loaded: 8

print(docs[0].metadata)
# {'producer': 'PDFium', 'creator': 'PDFium', 'creationdate': 'D:20210727120109', 'keywords': 'Classification=t_class_2', 'source': 'https://www.upl-ltd.com/images/people/downloads/Leave-Policy-India.pdf', 'total_pages': 8, 'page': 0, 'page_label': '1'}

print(docs[0].page_content[:300])
# Leave Policy - INDIA
