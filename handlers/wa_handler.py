from fastapi import APIRouter, Form, Response
from twilio.twiml.messaging_response import MessagingResponse
from core.ai_engine import ai_engine

router = APIRouter()

@router.post("/whatsapp")
async def handle_wa(Body: str = Form(...)):
    answer = await ai_engine.get_response(Body)
    twiml = MessagingResponse()
    twiml.message(answer)
    return Response(content=str(twiml), media_type="application/xml")