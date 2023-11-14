from generate_past_data import populate_month
from scripts import get_month_data, get_cookie
from datetime import datetime

def populate_day_data(date):
    populate_month(get_month_data(date.month, date.year), date.year)
    
if __name__=='__main__':
    get_cookie()
    populate_day_data(datetime.now())