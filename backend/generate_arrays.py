import firebase_admin
import random
import os
from dotenv import load_dotenv
from faker import Faker
from google.cloud import firestore

fake = Faker()
load_dotenv()

service_account_key = os.getenv('SERVICE_ACCOUNT_KEY_PATH')
project_id = os.getenv('PROJECT_ID')
db = firestore.Client.from_service_account_json(service_account_key, project=project_id)
top_level_collection = 'Solar Arrays'

def generate_random_data():
    return {
        'area': random.random() * 100,
        'beta': random.randint(0, 10),
        'gamma': random.randint(0, 10),
        'name': fake.name(),
        'rho_g': random.random() * 10,
        'submit': None
    }

# populate 8 arrays
for i in range(8):
    doc_ref = db.collection(top_level_collection).document()
    doc_ref.set(generate_random_data())








