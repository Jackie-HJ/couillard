from generate_past_data import populate_past_data
from datetime import datetime

if __name__=='__main__':
    # running in UTC timezone in GH action
    yesterday = datetime.fromtimestamp(datetime.now().timestamp() - 24*60*60) # datetime 24 hours ago
    populate_past_data(yesterday, yesterday)
