from twilio.rest import Client
from fastapi import HTTPException

from api.config.settings import TwilioSettings

_settings = TwilioSettings()

_client = Client(_settings.account_sid, _settings.auth_token)

def send_message(to: str, body: str) -> str:
    """
    Envia um SMS via Twilio.
    Retorna o SID da mensagem se bem-sucedido,
    ou levanta HTTPException em caso de erro.
    """
    try:
        message = _client.messages.create(
            to=to,
            from_=_settings.from_phone,
            body=body
        )
        return message.sid
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))