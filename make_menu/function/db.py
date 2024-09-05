from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv
from chromadb.utils import embedding_functions


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
        db.persist()
        return {"status": "success", "message": "正常にaddされました"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def read_text_chroma(query):
    # Sentence Transformersを使用した埋め込み関数を設定
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    # Chromaインスタンスを作成し、埋め込み関数を設定
    db = Chroma(persist_directory="DB", embedding_function=sentence_transformer_ef)
    
    # クエリの類似検索を実行
    results = db.similarity_search_with_score(query, 3)
    return results