from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from api.database.database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(255), index=True, nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    direction = Column(String(50), nullable=False)
    provider_message_id = Column(String(255), unique=True, nullable=True, index=True)
    content_type = Column(String(50), nullable=False, default="text")

    def __repr__(self):
        return (f"<Message(id={self.id}, phone_number={self.phone_number}, "
                f"content={self.content[:20]}, timestamp={self.timestamp},"
                f" direction={self.direction})>"
        )
