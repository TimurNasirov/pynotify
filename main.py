from fastapi import FastAPI
from routes import router
import crud

app = FastAPI()

@app.on_event('startup')
async def startup():
    await crud.db.init()
    await crud.db.create_tables()

app.include_router(router)