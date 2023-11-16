from firebase_admin import initialize_app, firestore
import os
from faker import Faker
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta
from scripts import get_month_data, get_cookie_fronius
from auroravision import get_month_data_auroravision, get_cookie_auroravision
import pathlib

fake = Faker()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(
    pathlib.Path().resolve()) + "/cred.json"
app = initialize_app()
db = firestore.client(app)

start_date_fronius = datetime(2020, 6, 1)
start_date_auroravision = datetime(2022, 12, 1)
current_date = datetime.now()

top_level_collection = 'Solar Arrays'


def populate_month(month_data, year, document):
    doc_id = document.id
    doc_ref = db.collection(top_level_collection).document(doc_id)

    output_collection_ref = doc_ref.collection('Output')

    year_doc_ref = output_collection_ref.document(str(year))

    data_to_merge = {
        'Output': month_data
    }

    year_doc_ref.set(data_to_merge, merge=True)


def populate_past_data_fronius(start_date, current_date, pvSystemId, document):
    running_date = start_date
    while running_date <= current_date:
        month_data = get_month_data(running_date.month, running_date.year, pvSystemId)
        populate_month(month_data, running_date.year, document)
        running_date += relativedelta(months=1)
        
def populate_past_data_auroravision(eids, start_date, end_date, cookie, document):
    running_date = start_date
    while running_date <= current_date:
        # to avoid complications with the year
        if running_date.month == 12 and running_date.day != 1 and running_date.day != 2:
            running_date = datetime(running_date.year, running_date.month, 3)

        month_data = get_month_data_auroravision(eids,
            generate_auroravision_date(running_date), generate_auroravision_date(running_date + relativedelta(days=30)), cookie)
        
        if month_data != None:
            populate_month(month_data, running_date.year, document)
        
        running_date += relativedelta(days=30)

def generate_auroravision_date(date):
    return str(date.year) + str(date.month).zfill(2) + str(date.day).zfill(2)
    
if __name__ == '__main__':
    get_cookie_fronius()
    documents = db.collection(top_level_collection).stream()
    for document in documents:
        if document.to_dict()["type"] == "fronius":
            pvSystemId = document.to_dict()["pvSystemId"]
            populate_past_data_fronius(start_date_fronius, current_date, pvSystemId, document)
        elif document.to_dict()["type"] == "auroravision":
            eids = document.to_dict()["entityId"]
            auroravision_cookie = get_cookie_auroravision(eids)
            populate_past_data_auroravision(eids, start_date_auroravision, current_date, auroravision_cookie, document)
            
