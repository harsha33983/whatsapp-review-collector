from fastapi import APIRouter, Request, Depends, Form
from sqlalchemy.orm import Session
from twilio.twiml.messaging_response import MessagingResponse
from database import get_db
from services import conversation
from services.conversation import ConversationState
import crud, schemas

router = APIRouter()

@router.post("/whatsapp/webhook")
async def whatsapp_webhook(
    From: str = Form(...),
    Body: str = Form(...),
    db: Session = Depends(get_db)
):
    session = conversation.get_session(From)
    response = MessagingResponse()
    message = Body.strip()

    # State Machine
    if session.state == ConversationState.INIT:
        # Any initial message triggers the flow
        session.state = ConversationState.WAITING_FOR_PRODUCT
        response.message("Hi! Which product is this review for?")
    
    elif session.state == ConversationState.WAITING_FOR_PRODUCT:
        session.product_name = message
        session.state = ConversationState.WAITING_FOR_NAME
        response.message("What's your name?")
    
    elif session.state == ConversationState.WAITING_FOR_NAME:
        session.user_name = message
        session.state = ConversationState.WAITING_FOR_REVIEW
        response.message(f"Please send your review for {session.product_name}.")
    
    elif session.state == ConversationState.WAITING_FOR_REVIEW:
        session.review_text = message
        
        # Save to database
        review_data = schemas.ReviewCreate(
            contact_number=From,
            user_name=session.user_name,
            product_name=session.product_name,
            product_review=session.review_text
        )
        crud.create_review(db, review_data)
        
        response.message(f"Thanks {session.user_name} — your review for {session.product_name} has been recorded.")
        
        # Reset session
        conversation.clear_session(From)

    return str(response)
