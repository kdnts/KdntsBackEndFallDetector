import threading

from fastapi import FastAPI
from mqtt.mqttClient import start_mqtt
from api.routes import router

app = FastAPI()

app.include_router(router)

mqttThread = threading.Thread(
    target= start_mqtt,
    daemon= True
)

mqttThread.start()
print("backend started")

@app.get("/")
def root():
    return{"message": "backend running"}