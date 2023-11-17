from firebase_admin import initialize_app, firestore
import random
import os
from faker import Faker
import pathlib

fake = Faker()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] =  str(pathlib.Path().resolve()) + "/cred.json"
app = initialize_app()
db = firestore.client(app)
top_level_collection = 'Solar Arrays'

def generate_random_data():
    return {
        'area': random.random() * 100,
        'name': fake.name(),
    }

# populate 8 arrays
for i in range(8):
    doc_ref = db.collection(top_level_collection).document()
    doc_ref.set(generate_random_data())








