import datetime

def generate_date(str_date):
    if str_date == "":
        return None
    return datetime.datetime.strptime(str_date, "%Y%m%d").date()