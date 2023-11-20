from generate_past_data import populate_month
from scripts import get_month_data, get_cookie_fronius
from datetime import datetime

def populate_day_data(date):
    get_cookie_fronius()
    get
    populate_month(get_month_data(date.month, date.year), date.year)
    
if __name__=='__main__':
    get_cookie_fronius()
    documents = db.collection(top_level_collection).stream()
    for document in documents:
        if document.to_dict()["type"] == "fronius":
            pvSystemId = document.to_dict()["pvSystemId"]
        elif document.to_dict()["type"] == "auroravision":
            eids = document.to_dict()["entityId"]
            auroravision_cookie = get_cookie_auroravision(eids)
    populate_day_data(datetime.now())