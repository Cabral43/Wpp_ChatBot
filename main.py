import os
import uvicorn

import api.model.message

from fastapi import FastAPI
from api.database.database import engine, Base

Base.metadata.create_all(bind=engine)

from api.router.routes import router as sms_router


app = FastAPI(
    title="Way Fitness API",
    description="API para o sistema de atendimento da Way Fitness",
)

app.include_router(sms_router)

@app.get("/")
def healthcheck():
    return {"status": "ok", "message": "API is running!"}


if __name__ == "__main__":
    reload_flag = os.getenv("RELOAD", "false").lower() == "true"
    homolog_mode = os.getenv("HOMOLOG_MODE", "false").lower() == "true"
    port = int(os.getenv("PORT", 8000))

    host = "127.0.0.1" if homolog_mode else "0.0.0.0"

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload_flag,
    )

