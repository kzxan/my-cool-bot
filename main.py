import uvicorn
from fastapi import FastAPI, Form, Response
from twilio.twiml.messaging_response import MessagingResponse
from core.ai_engine import ai_engine

app = FastAPI()

@app.post("/whatsapp")
async def handle_wa(Body: str = Form(...)):
    answer = await ai_engine.get_response(Body)
    twiml = MessagingResponse()
    twiml.message(answer)
    return Response(content=str(twiml), media_type="application/xml")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
