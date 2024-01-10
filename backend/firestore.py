from firebase_admin import initialize_app, firestore, credentials

cred = credentials.Certificate("./cred.json")
app = initialize_app(cred)
db = firestore.client(app)