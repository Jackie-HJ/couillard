from firebase_admin import initialize_app, firestore, credentials
import os

creds_path = os.environ.get('CREDS_PATH', 'cred.json')
cred = credentials.Certificate(creds_path)
app = initialize_app(cred)
db = firestore.client(app)