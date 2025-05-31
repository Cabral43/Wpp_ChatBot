from sqlalchemy.orm import Session
from api.model.message import Message as MessageModel
from api.database.schema.message import MessageCreate
from sqlalchemy import func
from datetime import datetime, date, time
import pytz

def create_message(db: Session, message_data: MessageCreate) -> MessageModel:
    """
    Cria e salva uma nova mensagem no banco de dados.
    """
    db_message = MessageModel(
        phone_number=message_data.phone_number,
        content=message_data.content,
        direction=message_data.direction,
        content_type=message_data.content_type,
        provider_message_id=message_data.provider_message_id
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_messages_by_phone_number(db: Session, phone_number: str, skip: int = 0, limit: int = 100):
    """
    Busca mensagens por número de telefone.
    """
    return (db.query(MessageModel).filter(MessageModel.phone_number == phone_number)
            .order_by(MessageModel.timestamp.desc()).offset(skip).limit(limit).all()
    )

def count_messages_by_phone_on_local_date(
    db: Session,
    phone_number: str,
    local_date: date,
    timezone_str: str = "America/Sao_Paulo"
) -> int:
    """
    Conta as mensagens de um usuário enviadas em uma data local específica.
    Assume que os timestamps no banco (MessageModel.timestamp) estão armazenados em UTC.
    """
    local_tz = pytz.timezone(timezone_str)

    # Define o início do dia na data local especificada
    start_of_day_local = local_tz.localize(datetime.combine(local_date, time.min))
    # Define o fim do dia na data local especificada
    end_of_day_local = local_tz.localize(datetime.combine(local_date, time.max))

    # Converte os limites para UTC para consulta no banco de dados
    start_of_day_utc = start_of_day_local.astimezone(pytz.utc)
    end_of_day_utc = end_of_day_local.astimezone(pytz.utc)

    count = db.query(func.count(MessageModel.id)).filter(
        MessageModel.phone_number == phone_number,
        MessageModel.timestamp >= start_of_day_utc,
        MessageModel.timestamp < end_of_day_utc # Usar < para o final do dia é mais preciso
    ).scalar()
    return count if count is not None else 0