import asyncio
import logging
from typing import Optional
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.schema import HumanMessage
from src.database.chroma_db import chromadb_retrieve
from src.services.remedy_service import get_remedy
from config import OPENAI_API_KEY, OPENAI_MODEL, EMBED_MODEL, TOP_K, TEMPERATURE, MAX_TOKENS
from src.utils.helper import normalize_metadata, pack_retrieved_text, _unwrap_ai_message
from src.prompts.astro_prompt import COMBINED_PROMPT_SIMPLE
from src.models.prompt_model import AnswerOutput
from langchain.output_parsers import PydanticOutputParser

# ---------------- Output Parser ----------------
output_parser = PydanticOutputParser(pydantic_object=AnswerOutput)

# ---- Initialize LLM and Embeddings ----
llm = ChatOpenAI(model=OPENAI_MODEL, api_key=OPENAI_API_KEY, temperature=TEMPERATURE, max_tokens=MAX_TOKENS)


embeddings = OpenAIEmbeddings(model=EMBED_MODEL, api_key=OPENAI_API_KEY)


# Fill format instructions automatically for parser
COMBINED_PROMPT_SIMPLE = COMBINED_PROMPT_SIMPLE.partial(
    format_instructions=output_parser.get_format_instructions()
)


# ---------------- Main Processing Methods ----------------
async def process_question_with_context(question: str, context: Optional[str] = None) -> dict:
    if not question or not isinstance(question, str):
        raise ValueError("Question must be a non-empty string.")

    try:
        
        data = {"question": question, "context": context or ""}

        # Step 1: Retrieval (question + context) concurrently
       
        tasks = [chromadb_retrieve(data["question"], TOP_K)]
        if data.get("context"):
            tasks.append(chromadb_retrieve(data["context"], TOP_K))
        else:
            tasks.append(asyncio.sleep(0, result=[]))  # dummy for alignment

        retrieved_docs_question, retrieved_docs_context = await asyncio.gather(*tasks)
        
        

        # Deduplicate retrieved docs
        combined_docs_map = {doc['text']: doc for doc in (retrieved_docs_question + retrieved_docs_context)}
        combined_docs = list(combined_docs_map.values())
        data["retrieved_docs"] = combined_docs
        data["retrieved_text"] = pack_retrieved_text(data["retrieved_docs"])
        data["context_block"] = f"Additional Context:\n{data['context']}" if data.get("context") else ""

    

        # Step 2: Generate category + answer in **one LLM call**
        
        human_msg = HumanMessage(content=COMBINED_PROMPT_SIMPLE.format(
            question=data["question"],
            retrieved_block=f"Retrieved texts:\n{data['retrieved_text']}" if data["retrieved_text"] else "",
            context_block=data["context_block"]
        ))

        combined_response = await llm.agenerate([[human_msg]])
        combined_text = combined_response.generations[0][0].text
       

        # Step 3: Parse & validate JSON output
       
        try:
            parsed_output = output_parser.parse(combined_text)
            data["category"] = parsed_output.category.title()
            data["answer"] = parsed_output.answer
        except Exception as e:
            logging.error(f"JSON parsing failed: {e}")
            data["category"] = "General"
            data["answer"] = _unwrap_ai_message(combined_text)
        

        # Step 4: Remedy lookup
      
        remedy = get_remedy(data.get("category"))

        return {
            "question": question,
            "category": data["category"],
            "answer": data["answer"],
            "remedy": remedy,
            "retrieved_sources": [normalize_metadata(d.get("metadata")) for d in data.get("retrieved_docs", [])],
        }

    except Exception as e:
        logging.error(f"Error: {e}")
        raise


async def process_question(question: str, context: Optional[str] = None) -> dict:
    """
    Same as above but only question-based retrieval (no extra context)
    """
    if not question or not isinstance(question, str):
        raise ValueError("Question must be a non-empty string.")

    try:
        
        data = {"question": question, "context": context or ""}

        # Step 1: Retrieval (question only)
        
        retrieved_docs_question = await chromadb_retrieve(data["question"], TOP_K)
        
      

        data["retrieved_docs"] = retrieved_docs_question
        data["retrieved_text"] = pack_retrieved_text(data["retrieved_docs"])
        data["context_block"] = f"Additional Context:\n{data['context']}" if data.get("context") else ""

    

        # Step 2: Generate category + answer
      
        human_msg = HumanMessage(content=COMBINED_PROMPT_SIMPLE.format(
            question=data["question"],
            retrieved_block=f"Retrieved texts:\n{data['retrieved_text']}" if data["retrieved_text"] else "",
            context_block=data["context_block"]
        ))

        combined_response = await llm.agenerate([[human_msg]])
        combined_text = combined_response.generations[0][0].text
    
       

        # Step 3: Parse & validate

        try:
            parsed_output = output_parser.parse(combined_text)
            data["category"] = parsed_output.category.title()
            data["answer"] = parsed_output.answer
        except Exception as e:
            logging.error(f"JSON parsing failed: {e}")
            data["category"] = "General"
            data["answer"] = _unwrap_ai_message(combined_text)
        
        
        # Step 4: Remedy lookup
        
        remedy = get_remedy(data.get("category"))
        

        return {
            "question": question,
            "category": data["category"],
            "answer": data["answer"],
            "remedy": remedy,
            "retrieved_sources": [normalize_metadata(d.get("metadata")) for d in data.get("retrieved_docs", [])],
        }

    except Exception as e:
        logging.error(f"Error: {e}")
        raise