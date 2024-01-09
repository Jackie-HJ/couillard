from firebase_admin import initialize_app, firestore
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
from scripts import get_month_data, get_cookie_fronius
from auroravision import get_month_data_auroravision, get_cookie_auroravision
import pathlib

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(
    pathlib.Path().resolve()) + "/cred.json"
app = initialize_app()
db = firestore.client(app)

start_date_fronius_g = datetime(2020, 6, 1)
start_date_auroravision_g = datetime(2022, 12, 1)

top_level_collection = 'Solar Arrays'


def populate_month(month_data, year, document):
    doc_id = document.id
    doc_ref = db.collection(top_level_collection).document(doc_id)

    output_collection_ref = doc_ref.collection('Output')

    year_doc_ref = output_collection_ref.document(str(year))

    data_to_merge = {
        'Output': month_data,
    }

    print(month_data)



    year_doc_ref.set(data_to_merge, merge=True)
    doc_ref.set({'update_required': False}, merge=True)


def populate_past_data_fronius(start_date, current_date, pvSystemId, document):
    running_date = start_date
    while running_date <= current_date:
        month_data = get_month_data(running_date.month, running_date.year, pvSystemId)
        populate_month(month_data, running_date.year, document)
        running_date += relativedelta(months=1)
        
def populate_past_data_auroravision(eids, start_date, current_date, cookie, document):
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

def populate_past_data(start_date_fronius, start_date_auroravision):
    current_date = datetime.now()
    get_cookie_fronius()
    documents = db.collection(top_level_collection).stream()
    for document in documents:
        if document.to_dict()["type"] == "fronius":
            pvSystemId = document.to_dict()["id"]

            if document.to_dict().get('update_required', False):
                populate_past_data_fronius(start_date_fronius_g, current_date, pvSystemId, document)

            populate_past_data_fronius(start_date_fronius, current_date, pvSystemId, document)
        elif document.to_dict()["type"] == "auroravision":
            eids = document.to_dict()["id"]
            auroravision_cookie = get_cookie_auroravision(eids)

            if document.to_dict().get('update_required', False):
                populate_past_data_auroravision(eids, start_date_auroravision_g, current_date, auroravision_cookie, document)

            populate_past_data_auroravision(eids, start_date_auroravision, current_date, auroravision_cookie, document)
    
def generate_auroravision_date(date):
    return str(date.year) + str(date.month).zfill(2) + str(date.day).zfill(2)
    
if __name__ == '__main__':
    populate_past_data(start_date_fronius_g, start_date_auroravision_g)

            
