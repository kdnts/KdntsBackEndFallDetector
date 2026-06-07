from fastapi import APIRouter

from api.schema import PairDeviceRequest, UnpairDeviceRequest, AddContactRequest
from firebase.firestoreService import getDevice, pairDevice, isDeviceOwner, unpairDevice, addContact, getContact, deleteContact, getNotifications, markNotificationRead

router = APIRouter()

@router.post("/pair-device")
def pair_device(request: PairDeviceRequest):

    device = getDevice(request.deviceId)

    if device is None:
        return{"success": False, "message": "cant find device"}
    
    if device["devicePassword"] != request.devicePassword:
        return{"success": False, "message": "wrong password"}
    
    pairDevice(
        request.deviceId,
        request.userId
    )

    return{"success": True}


@router.post("/unpair-device")
def unpair_device(request: UnpairDeviceRequest):

    if not isDeviceOwner(request.deviceId, request.userId):
        return{"succes": False, "message": "not owner"}

    unpairDevice(
        request.deviceId, 
        request.userId
    )

    return{"success": True}

@router.post("/contacts")
def add_contact(request: AddContactRequest):
    addContact(request.userId, request.name, request.phone)

    return{"success": True}

@router.get("/contacts/{userId}")
def get_contact(userId):

    return getContact(userId)

@router.delete("/contacts/{userId/{contactId}")
def delete_contact(contactId, userId):
    deleteContact(userId, contactId)

    return {"success": True}

@router.get("/notifications/{userId}")
def get_notifications(userId):
    return getNotifications(userId)

@router.post("/notifications/{notificationId}/read")
def mark_read(notificationId):
    markNotificationRead(notificationId)

    return {"success": True}
