from firebase_admin import initialize_app, firestore
import random
import os
from dotenv import load_dotenv
from faker import Faker
from datetime import datetime
from datetime import timedelta
import pathlib

fake = Faker()
load_dotenv()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] =  str(pathlib.Path().resolve()) + "/cred.json"
app = initialize_app()
db = firestore.client(app)

# random start date
start_date = datetime(2022, 12, 20)
current_date = datetime.now()

top_level_collection = 'Solar Arrays'

def populate_day(date):
    documents = db.collection(top_level_collection).stream()

    for document in documents:
        doc_id = document.id
        doc_ref = db.collection(top_level_collection).document(doc_id)

        output_collection_ref = doc_ref.collection('Output')

        current_year = date.year

        year_doc_ref = output_collection_ref.document(str(current_year))
        year_output_data = {date.strftime("%Y-%m-%d"): random.randint(1, 100)}

        year_doc_ref.set({'Output': year_output_data}, merge=True)
        
def populate_all_past_data(start_date, current_date):
    running_date = start_date
    while running_date <= current_date:
        populate_day(running_date)
        running_date += timedelta(days=1)
        
# last 24 hours
populate_day(current_date)

# past data since start date
populate_all_past_data(start_date, current_date)
    
    
      















