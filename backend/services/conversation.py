from typing import Dict, Optional
from enum import Enum

class ConversationState(Enum):
    INIT = "INIT"
    WAITING_FOR_PRODUCT = "WAITING_FOR_PRODUCT"
    WAITING_FOR_NAME = "WAITING_FOR_NAME"
    WAITING_FOR_REVIEW = "WAITING_FOR_REVIEW"
    COMPLETED = "COMPLETED"

class ConversationSession:
    def __init__(self):
        self.state = ConversationState.INIT
        self.product_name: Optional[str] = None
        self.user_name: Optional[str] = None
        self.review_text: Optional[str] = None

# In-memory storage for conversation states
# Key: WhatsApp phone number, Value: ConversationSession
sessions: Dict[str, ConversationSession] = {}

def get_session(phone_number: str) -> ConversationSession:
    if phone_number not in sessions:
        sessions[phone_number] = ConversationSession()
    return sessions[phone_number]

def clear_session(phone_number: str):
    if phone_number in sessions:
        del sessions[phone_number]
