from fastapi import APIRouter, Form, Response, Depends
from sqlalchemy.orm import Session
from twilio.twiml.messaging_response import MessagingResponse
import datetime
import pytz

from .utils import twilio_menu
from api.database.database import get_db
from api.database.schema.message import MessageCreate
from api.core.utils.crud_message import create_message, count_messages_by_phone_on_local_date


router = APIRouter()

LOCAL_TIMEZONE_STR = "America/Sao_Paulo"

@router.post("/sms")
async def inbound_sms(
    Body: str = Form(...),
    From: str = Form(...),
    MessageSid: str = Form(None),
    db: Session = Depends(get_db)
):
    """
       Webhook Twilio: recebe SMS e devolve um menu ou a resposta escolhida.
    """
    incoming_msg_body = Body.strip()
    sender_phone = From.removeprefix("whatsapp:").strip()
    normalized_incoming_body = incoming_msg_body.lower()

    local_tz = pytz.timezone(LOCAL_TIMEZONE_STR)
    current_local_datetime = datetime.datetime.now(local_tz)
    today_local_date = current_local_datetime.date()

    messages_sent_by_user_today = count_messages_by_phone_on_local_date(
        db=db,
        phone_number=sender_phone,
        local_date=today_local_date,
        timezone_str=LOCAL_TIMEZONE_STR
    )
    is_first_message_of_the_day = (messages_sent_by_user_today == 0)

    incoming_message_schema = MessageCreate(
        phone_number=sender_phone,
        content=incoming_msg_body,
        direction="inbound",
        content_type="text",
        provider_message_id=MessageSid
    )
    create_message(db=db, message_data=incoming_message_schema)

    # Resposta
    response_body_text = ""

    if is_first_message_of_the_day:
        hour_local = current_local_datetime.hour
        greeting = "Olá!"
        if 5 <= hour_local < 12:
            greeting = "Bom dia!"
        elif 12 <= hour_local < 18:
            greeting = "Boa tarde!"
        else:
            greeting = "Boa noite!"

        response_body_text = f"{greeting}\n\n{twilio_menu.MENU_TEXT}"
    else:
        match normalized_incoming_body.lower():
            case "1":
                response_body_text = twilio_menu.TEXT_1
            case "2":
                response_body_text = twilio_menu.TEXT_2
            case "3":
                response_body_text = twilio_menu.TEXT_3
            case "4":
                response_body_text = twilio_menu.TEXT_4
            case "5":
                response_body_text = twilio_menu.TEXT_5
            case "0":
                response_body_text = twilio_menu.TEXT_0
            case "9" | "voltar" | "menu":
                response_body_text = twilio_menu.MENU_TEXT
            case _:
                response_body_text = twilio_menu.MENU_TEXT

    resp = MessagingResponse()
    msg = resp.message()
    msg.body(response_body_text)

    outgoing_message_schema = MessageCreate(
        phone_number=sender_phone,
        content=response_body_text,
        direction="outbound",
        content_type="text",
        provider_message_id=None  # Twilio does not provide an ID for outbound messages in this context
    )
    create_message(db=db, message_data=outgoing_message_schema)

    return Response(content=str(resp), media_type="application/xml")