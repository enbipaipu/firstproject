from langchain.vectorstores import Chroma


def create_chroma():
    db = Chroma(persist_directory="DB")  
    

def read_chroma(add_):
    db.add_texts()
print(f"count = {db._collection.count()}")  # count = 5
db.persist()