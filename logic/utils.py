import datetime
from string import digits

import pytz
from dateutil import relativedelta
from django.conf import settings
from django.utils.crypto import get_random_string

"""
1) Display contract period for Supervisor
2) Assigning breaks between periods
3) BM assigns supervisor to project: Supervisor is on payroll
4) Supervisor assigns tasks on the project
5) BM sees report on approved tasks
6) Supervisor can assign break to volunteer
7) Counter reset
8) Display volunteer availability for project
9) 0 days should not appear on projects
10) Notification to remind on periods running down 
"""


def generate_otp_code():
    return get_random_string(length=5, allowed_chars=digits), current_time() + datetime.timedelta(minutes=10)


def current_time():
    return pytz.timezone(settings.TIME_ZONE).localize(datetime.datetime.now(), is_dst=None)


def calculate_tomorrow(date):
    return date + relativedelta.relativedelta(days=1)


def get_landing_page(user):
    landing = 'home'
    return landing


def get_base_url(request):
    if request.is_secure():
        return 'https://' + str(request.get_host())
    else:
        return 'http://' + str(request.get_host())


def trim_phone(phone):
    p = phone
    if phone.startswith('256'):
        start, end = phone[:5], phone[-2:]
        p = abstract_between(phone, start, end)
    elif phone.startswith('+256'):
        start, end = phone[:6], phone[-2:]
        p = abstract_between(phone, start, end)
    elif phone.startswith('07'):
        start, end = phone[:3], phone[-2:]
        p = abstract_between(phone, start, end)
    return p


def abstract_between(s, start, end):
    mid = s[len(start):-len(end)]
    return f"{start}{'X' * len(mid)}{end}"


def calculate_start_day_of_year(date):
    return date - datetime.timedelta(days=360)


def pop_tuple(_t, index):
    lst = list(_t)
    lst.pop(index)
    return tuple(lst)


def extract_name(username):
    if '@gmail.go.ug' in username:
        username = username.replace('@gmail.go.ug', '').strip()
    return username.lower()
