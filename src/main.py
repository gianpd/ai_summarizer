from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from api.summarizer_api import router

app = FastAPI()

origins = [
    'http://localhost:3000' # testing the frontend
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping", name="Healtcheck", tags=["Healtcheck"])
async def healtcheck():
    return {"Success": "Pong!"}

app.include_router(router, prefix="/api")

handler = Mangum(app, lifespan='off') # handler for lambda function 