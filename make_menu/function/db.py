from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv



def create_chroma():
    try:
        db = Chroma(persist_directory="DB")
        db.persist()
        return {"status": "success", "message": "正常にcreateされました"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    

def add_text_chroma(texts):
    try:
    # .envファイルの内容を読み込みます
        load_dotenv()
        
        embeddings_model = OpenAIEmbeddings(
            openai_api_base= os.getenv("URL"),
            openai_api_key = os.getenv("OPEN_API_KEY"),
            )
            
        db = Chroma(persist_directory="DB")
        db = Chroma.from_texts(texts, embeddings_model)
        print(f"count = {db._collection.count()}")
        db.persist()
        return {"status": "success", "message": "正常にaddされました"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def read_text_chroma(query):
    try:
        load_dotenv()
        
        embeddings_model = OpenAIEmbeddings(
            openai_api_base= os.getenv("URL"),
            openai_api_key = os.getenv("OPEN_API_KEY"),
            )
        db = Chroma(persist_directory="DB", embedding_function=embeddings_model)
        results = db.similarity_search_with_score(query, 3)
        print(f"count = {db._collection.count()}")
        return results
    except Exception as e:
        return str(e)