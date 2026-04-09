from langchain_text_splitters import RecursiveCharacterTextSplitter

# Splitter
text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", " "],
    chunk_size=100,
    chunk_overlap=10
)

sample_text = """
Shall I compare thee to a summer’s day?
Thou art more lovely and more temperate:
Rough winds do shake the darling buds of May,
And summer’s lease hath all too short a date;
Sometime too hot the eye of heaven shines,
And often is his gold complexion dimm'd;
And every fair from fair sometime declines,
By chance or nature’s changing course untrimm'd;
"""
sample_splitted = text_splitter.split_text(sample_text)

print(sample_splitted)
# ['Shall I compare thee to a summer’s day?\nThou art more lovely and more temperate:', 
#  'Rough winds do shake the darling buds of May,\nAnd summer’s lease hath all too short a date;', 
#  "Sometime too hot the eye of heaven shines,\nAnd often is his gold complexion dimm'd;", 
#  "And every fair from fair sometime declines,\nBy chance or nature’s changing course untrimm'd;"]

