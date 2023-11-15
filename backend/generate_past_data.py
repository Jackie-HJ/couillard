from firebase_admin import initialize_app, firestore
import os
from faker import Faker
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta
from scripts import get_month_data, get_cookie
import pathlib

fake = Faker()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(
    pathlib.Path().resolve()) + "/cred.json"
app = initialize_app()
db = firestore.client(app)

# start date of fronius
start_date = datetime(2022, 10, 1)
current_date = datetime.now()

top_level_collection = 'Solar Arrays'


def populate_month(month_data, year, document):
    # documents = db.collection(top_level_collection).stream()

    # for document in documents:
    #     doc_id = document.id
    #     doc_ref = db.collection(top_level_collection).document(doc_id)
    #     document_data = document.to_dict();
    #     if (document_data["name"] == name):

    #     output_collection_ref = doc_ref.collection('Output')

    #     year_doc_ref = output_collection_ref.document(str(year))

    #     data_to_merge = {
    #         'Output': month_data
    #     }

    #     year_doc_ref.set(data_to_merge, merge=True)
    doc_id = document.id
    doc_ref = db.collection(top_level_collection).document(doc_id)

    output_collection_ref = doc_ref.collection('Output')

    year_doc_ref = output_collection_ref.document(str(year))

    data_to_merge = {
        'Output': month_data
    }

    year_doc_ref.set(data_to_merge, merge=True)


def populate_past_data(start_date, current_date, pvSystemId, document):
    running_date = start_date
    while running_date <= current_date:
        populate_month(get_month_data(
            running_date.month, running_date.year, pvSystemId), running_date.year, document)
        running_date += relativedelta(months=1)


if __name__ == '__main__':
    pvSystemId = ''
    get_cookie()
    documents = db.collection(top_level_collection).stream()
    documentToPass = None
    for document in documents:
        if document.to_dict()["type"] == "fronius":
            print(document.to_dict())
            pvSystemId = document.to_dict()["pvSystemId"]
            print("pvSystemId: " + pvSystemId)
            documentToPass = document
            populate_past_data(start_date, current_date, pvSystemId, document)
