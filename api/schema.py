from pydantic import BaseModel

class PairDeviceRequest(BaseModel):
    deviceId: str
    devicePassword: str
    userId: str

class UnpairDeviceRequest(BaseModel):
    deviceId: str
    userId: str

class AddContactRequest(BaseModel):
    userId: str
    name: str
    phone:str

class MarkedReadRequest(BaseModel):
    notifications: str