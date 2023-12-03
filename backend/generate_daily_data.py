from generate_past_data import populate_past_data
from scripts import get_month_data, get_cookie_fronius
from datetime import datetime
from firebase_admin import initialize_app
from dateutil.relativedelta import relativedelta
from scripts import get_month_data, get_cookie_fronius
from auroravision import get_month_data_auroravision, get_cookie_auroravision

if __name__=='__main__':
    populate_past_data(datetime.now(), datetime.now())
