from dotenv import load_dotenv 
import os
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

API_KEY = os.getenv("MY_API_KEY")



OPENAI_MODEL=os.getenv("OPENAI_MODEL")
EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.6"))
TOP_K = int(os.getenv("TOP_K", "4"))

MAX_TOKENS = int(os.getenv("MAX_TOKENS", "8000"))

CHROMADB_API_KEY = os.getenv("CHROMADB_API_KEY", "")
CHROMADB_TENANT = os.getenv("CHROMADB_TENANT", "")
CHROMADB_DB_NAME = os.getenv("CHROMADB_DB_NAME", "Astrolozee")
COLLECTION_NAME = os.getenv("CHROMA_COLLECTION", "knowledge_base")




# LangSmith (optional)
LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING")
LANGSMITH_ENDPOINT = os.getenv("LANGSMITH_ENDPOINT")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT")



# # MongoDB for chat history
# MONGO_URI = os.getenv("MONGO_URI")
# MONGO_DB = os.getenv("MONGO_DB")
# MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")
# # ------------------------------------------
# End of config.py