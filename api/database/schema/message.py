from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class MessageBase(BaseModel):
    phone_number: str = Field(..., max_length=50, examples=["whatsapp:+5511999998888"])
    content: str = Field(..., examples=["Content of the message"])
    direction: Optional[str] = Field(None, max_length=50, examples=["inbound", "outbound"])
    content_type: Optional[str] = Field("text", examples=["text", "image"])
    provider_message_id: Optional[str] = Field(None, examples=["SMxxxxxxxxxxxxxx"])


class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int = Field(..., examples=[1])
    timestamp: datetime = Field(..., examples=["2023-10-01T12:00:00Z"])

    class Config:
        from_attributes: bool = True
        json_schema_extra: dict[str, dict[str, str | int]] = {
            "example": {
                "id": 1,
                "phone_number": "whatsapp:+5511999998888",
                "content": "Content of the message",
                "timestamp": "2023-10-01T12:00:00Z",
                "direction": "outbound",
                "content_type": "text",
                "provider_message_id": "SMxxxxxxxxxxxxxx"
            }
        }
