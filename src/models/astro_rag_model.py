from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class AIRequests(BaseModel):
    question: str
    context: Optional[str] = None
    rag_with_context: Optional[bool] = False  # default to False
    # use_history: Optional[bool] = False
    # session_id: Optional[str] = None


class AIResponses(BaseModel):
    question: str
    category: str
    answer: str
    remedy: str
    retrieved_sources: List[Dict[str, Any]] = []
