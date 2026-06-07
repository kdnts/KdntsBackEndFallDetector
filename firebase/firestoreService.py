from firebase.firebaseClient import db
from firebase_admin import firestore

def updateLocation(deviceId, lat, lng):
    docRef = db.collection("devices").document(deviceId)

    docRef.update({
        "lastLat": lat,
        "lastLng": lng,
        "deviceStatus": "online",
        "lastSeen": firestore.SERVER_TIMESTAMP})
    
    print("\nfirestore updated")

def createFall(deviceId, lat, lng):
    db.collection("falls").add({
    "deviceId": deviceId,
    "latitude": lat,
    "longitude": lng,
    "createdAt": firestore.SERVER_TIMESTAMP})

    device = getDevice(deviceId)
    userId = device.get("userId")

    createNotifications(userId, deviceId)
    
    print("\nsaving fall")  

def getDevice(deviceId):
    doc = (
        db.collection("devices").document(deviceId).get()
        )

    if not doc.exists:
        return None
    
    return doc.to_dict()

def pairDevice(deviceId, userId):
    db.collection("devices").document(deviceId).update({"userId": userId})

def unpairDevice(deviceId, userId):
    db.collection("devices").document(deviceId).update({"userId": None})

def isDeviceOwner(deviceId, userId):
    device = getDevice(deviceId)

    if device is None:
        return False
    
    return device.get("userId") == userId

def addContact(userId, name, phone):
    db.collection("users").document(userId).collection("contacts").add({
        "name": name,
        "phone": phone
    })

def getContact(userId):
    contacts = []

    docs = (db.collection("users").document(userId).collection("contacts").stream())

    for doc in docs:
        data = doc.to_dict()
        data["contactId"] = doc.id

        contacts.append(data)

    return contacts

def deleteContact(userId, contactId):
    db.collection("users").document(userId).collection("contacts").document(contactId).delete()

def createNotifications(userId, deviceId):
    db.collection("notifications").add({
        "userId": userId,
        "deviceId": deviceId,
        "title": "Fall Detected",
        "message": f"{deviceId} detected a fall",
        "isRead": False,
        "createdAt": firestore.SERVER_TIMESTAMP
    })

def getNotifications(userId):
    notifications = []

    docs = (db.collection("notifications").where("userId", "==", userId).stream())

    for doc in docs:
        data = doc.to_dict()
        data["notificationId"] = doc.id

        notifications.append(data)

    return notifications
    
def markNotificationRead(notificationId):
    db.collection("notifications").document(notificationId).update({"isRead": True})
