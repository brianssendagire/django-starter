import datetime
import json
from time import strftime, gmtime

import pytz as pytz
from dateutil import relativedelta
from django.conf import settings
from django.template import Library
from django.template.defaultfilters import stringfilter
from django.utils import timezone

register = Library()


def current_time():
    return pytz.timezone(settings.TIME_ZONE).localize(datetime.datetime.now(), is_dst=None)


def calculate_tomorrow(date):
    return date + relativedelta.relativedelta(days=1)


@register.filter(name='user_header_name')
def user_header_name(user):
    names = ""
    if user.is_authenticated:
        names = "{} {}".format(user.first_name, user.last_name).title()
    return names


@register.filter(name="shared_expiry_statements")
def shared_expiry_statements(expiry_date):
    message = ""
    if expiry_date and expiry_date >= current_time():
        message = "Please note that this share token expires on {}".format(expiry_date.strftime('%d %B, %Y'))
    elif expiry_date and expiry_date < current_time():
        message = "This payment_request sharing token expired, you can share it again"
    return message


@register.filter(name="check_expiry_statements")
def check_expiry_statements(expiry_date):
    status = False
    if expiry_date and expiry_date >= current_time():
        status = False
    elif expiry_date and expiry_date < current_time():
        status = True
    return status


@register.filter(name='landing_page')
def landing_page(user):
    landing = 'home'
    if not user.is_authenticated:
        landing = 'home'
    return landing


@register.filter(name='membership_validity')
def membership_validity(end_date):
    valid = False
    if end_date and end_date > datetime.datetime.today():
        valid = True
    return valid


@register.filter(name='compare_today')
def compare_today(date):
    exact = False
    if date and date == timezone.now().date():
        exact = True
    return exact


@register.filter(name='user_first_name')
def user_first_name(first_name):
    return str(first_name).title()


@register.filter(name="format_only_date")
def format_only_date(appointment_date):
    return appointment_date.strftime('%d %B, %Y')


@register.filter(name="format_short_date")
def format_short_date(date):
    return date.strftime('%d %b, %Y')


@register.filter(name="format_only_time")
def format_only_time(appointment_time):
    return appointment_time.strftime('%I:%M %p')


@register.filter(name="format_date_time")
def format_date_time(date):
    message = "No date provided"
    if date:
        _date = timezone.localtime(date)
        if _date.year == datetime.date.today().year:
            message = "{} at {}".format(_date.strftime('%d %B,'), _date.strftime('%I:%M %p'))
        else:
            message = "{} at {}".format(_date.strftime('%d %B, %Y'), _date.strftime('%I:%M %p'))
    return message


@register.filter(name="format_short_date_time")
def format_short_date_time(date):
    message = "No date provided"
    if date:
        _date = timezone.localtime(date)
        if _date.year == datetime.date.today().year:
            message = "{} at {}".format(_date.strftime('%d %b,'), _date.strftime('%I:%M %p'))
        else:
            message = "{} at {}".format(_date.strftime('%d %b, %Y'), _date.strftime('%I:%M %p'))
    return message


@register.filter(name="format_activity_time")
def format_activity_time(date):
    date = timezone.localtime(date)
    if date.date() == datetime.date.today():
        return "at {}".format(date.strftime('%I:%M %p'))
    else:
        return "{} on {}".format(date.strftime('%I:%M %p'), date.strftime('%d %B'))


@register.filter(name="format_money_commas")
def format_money_commas(amount):
    amount = f'{float(amount):,.2f}'
    if '.00' in str(amount):
        amount = str(amount).replace('.00', '')
    return amount


@register.filter(name="format_currency")
def format_currency(currency):
    prefix = "Ushs. "
    if currency == "USD":
        prefix = "USD. "
    elif currency == "GBP":
        prefix = "GBP. "
    elif currency == "EUR":
        prefix = "EUR. "
    return prefix


@register.filter(name="increment_one")
def increment_one(counter):
    count = 1
    if counter:
        count = int(counter)
        count += 1
    return count


@register.filter(name="status_color")
def status_color(status):
    color = "blue-text"
    if status == "Pending":
        color = "grey-text text-darken-4"
    elif status == "Closed":
        color = "green-text text-darken-1"
    return color


@register.filter(name="icon_color")
def icon_color(status):
    color = "blue-text text-darken 1"
    if status == "Pending":
        color = "amber-text text-darken-2"
    elif status in ["Approve", "Approve & Sign", "Endorse", "Signed", "Complete", "Approved"]:
        color = "green-text text-darken-1"
    elif status in ["Reject", "Rejected", "Defer", "Deferred", "Flag as Inappropriate"]:
        color = "red-text"
    return color


@register.filter(name="score_color")
def score_color(status):
    color = "blue-text text-darken 1"
    if status == "Pending":
        color = "amber-text text-darken-2"
    elif status in ["Approve", "Approve & Sign", "Endorse", "Signed", "Complete", "Approved"]:
        color = "green-text text-darken-1"
    elif status in ["Reject", "Rejected", "Defer", "Deferred", "Flag as Inappropriate"]:
        color = "red-text"
    return color


@register.filter(name="badge_color")
def badge_color(status):
    color = "blue lighten-1"
    if status == "Pending":
        color = "amber darken-2"
    elif status in 'Initiated':
        color = 'grey lighten-1'
    elif status in ["Approve", "Approve & Sign", "Endorse", "Signed", "Complete", "Approved"]:
        color = "green darken-1"
    elif status in ["Reject", "Rejected", "Defer", "Deferred", "Flag as Inappropriate"]:
        color = "red"
    return color


@register.filter(name="status_clean")
def status_clean(status):
    if status == 'Assigned':
        status = 'Assigned to Branch'
    return status


@register.filter(name="glow_color")
def glow_color(status):
    color = "ongoing"
    if status == "Pending":
        color = "pending"
    elif status in ["Approve", "Approve & Sign", "Signed", "Complete", "Approved"]:
        color = "green"
    elif status == "Reject" or status == "Rejected":
        color = "red"
    return f'{color}-glow'


@register.filter(name="text_color")
def text_color(days):
    color = "info"
    if days == 20:
        color = "amber-text text-darken-2"
    elif days < 20:
        color = "brown-text darken-4"
    elif days > 20:
        color = "red-text text-darken-1"
    return color


@register.filter(name="show_approvals")
def show_approvals(request):
    show = False
    allowed_roles = ['manager', 'human resource', 'internal auditor', 'director', 'executive director']
    overseers = ['robert.gumisiriza', 'frank.egesa', 'medard.nahurira', 'beatrice.sekabembe', 'lailah.nalukwago', 'arthur.munanura',
                 'michael.baleke', 'shamsa.mungoma', 'evadio.katsigazi', 'agnes.nsubuga']
    if request.user.role.lower() in allowed_roles or request.user.username.lower() in overseers:
        show = True
    return show


@register.filter(name="generic_leave")
def generic_leave(request):
    show = False
    overseers = ['julian.rweju', 'beatrice.sekabembe', 'lailah.nalukwago', 'arthur.munanura', 'agnes.nsubuga', 'brian.ssendagire', 'admin']
    if request.user.is_supervisor or request.user.is_line_manager or request.user.username.lower() in overseers and not request.user.is_director:
        show = True
    return show


@register.filter(name="directorate_leave")
def directorate_leave(request):
    show = False
    overseers = ['osbert.osamai', 'julian.rweju', 'beatrice.sekabembe', 'lailah.nalukwago', 'arthur.munanura', 'agnes.nsubuga', 'brian.ssendagire', 'admin']
    if request.user.is_line_manager or request.user.username.lower() in overseers or request.user.is_director or request.user.is_supervisor:
        show = True
    return show


@register.filter(name="history_link")
def history_link(request):
    show = 'processes:officer_history'
    managers = ['manager', 'human resource']
    overseers = ['robert.gumisiriza', 'frank.egesa', 'medard.nahurira', 'lailah.nalukwago', 'arthur.munanura',
                 'beatrice.sekabembe', 'agnes.nsubuga', 'brian.ssendagire', 'admin']
    """
    Add Procurement, finance, administration, human resource, service desk, epa
    """
    if request.user.username.lower() in overseers:
        show = 'processes:reports'
    elif request.user.role.lower() in managers:
        show = 'processes:manager_history'
    elif request.user.role.lower() == 'internal auditor':
        show = 'processes:ia_history'
    elif request.user.role.lower() == 'director':
        show = 'processes:director_history'
    elif request.user.role.lower() == 'executive director':
        show = 'processes:ed_history'
    return show


@register.filter(name="action_name")
def action_name(status):
    action = "Pending"
    if status in ["Approve", 'Approve & Sign']:
        action = "Approved"
    elif status == 'Defer':
        action = 'Deferred'
    elif status == 'Ongoing':
        action = 'Ongoing'
    elif status == 'Signed':
        action = 'Signed'
    elif status == 'Assign':
        action = 'Assigned'
    elif status == 'Accept':
        action = 'Accepted'
    elif status == 'Modified':
        action = 'Modified'
    elif status == 'Endorse':
        action = 'Assigned'
    elif status == 'Forward':
        action = 'Forwarded to Executive Director'
    elif status == "Reject":
        action = "Rejected"
    elif status == 'Flag as Inappropriate':
        action = 'Flagged Inappropriate'
    return action


@register.filter(name="get_json")
def get_json(query):
    return json.loads(query)


@register.filter(name="convert_directorate")
def convert_directorate(directorate):
    if directorate and directorate.lower() in "nita egovernment":
        directorate = "Directorate of e-Government Services"
    elif directorate and directorate.lower() in "nita finance & admin":
        directorate = "Directorate of Finance & Administration"
    elif directorate and directorate.lower() in "nita legal services":
        directorate = "Directorate of Regulation & Legal Services"
    elif directorate and directorate.lower() in "nita information security":
        directorate = "Directorate of Information Security"
    elif directorate and directorate.lower() in "nita technical services":
        directorate = "Directorate of Technical Services"
    elif directorate and directorate.lower() in "nita planning research & dev":
        directorate = "Directorate of Planning, Research & Development"
    elif directorate and directorate.lower() in "nita exco":
        directorate = "Executive Committee"
    else:
        directorate = "Directorate of e-Government Services"
    return directorate


# return ', '.join([a.admin_name for a in self.admins.all()])
# { % for place in places %}
# Name: {{place.name}}, Area: {{place.area.all | join: ", "}}
# { % endfor %}

@register.filter(name='letter_action')
def letter_action(action):
    color = 'blue'
    if action == 'defer':
        color = 'red'
    return color


@register.filter(name='letter_approver')
def letter_approver(user):
    allow = False
    _epas = ['lailah.nalukwago', 'emmanuel.tamale', 'admin', 'epa']
    if user.username in _epas:
        allow = True
    return allow


@register.filter(name='epa_designated_url')
def epa_designated_url(letter):
    url = 'processes:letter_detail'
    if (letter.recipient_status == 'Complete' and letter.epa_status == 'Pending') or letter.ed_intervention_status in ['Recommend', 'Defer'] or letter.rep_status == \
            'Defer':
        url = 'processes:assign_letter_detail'
    elif letter.epa_response_status == 'Pending' and letter.director_status == 'Approve':
        url = 'processes:epa_review_letter_detail'  # TODO create view
    return url


@register.filter(name='ed_designated_url')
def ed_designated_url(letter):
    url = 'processes:letter_detail'
    if letter.ed_status == 'Pending' and letter.director_status == 'Approve' and letter.task_owner_actioned:
        url = 'processes:ed_letter_detail'
    elif letter.ed_intervention and letter.ed_intervention_status == 'Pending':
        url = 'processes:ed_input_letter_detail'
    return url


@register.filter(name='letter_viewers')
def letter_viewers(user):
    allow = False
    viewers = ['NITA eGovernment', 'Administration', 'Registry', 'NITA Executive Director\'s Office', 'eDOC Directorate']
    if user.directorate in viewers:
        allow = True
    return allow


@register.filter(is_safe=True)
@stringfilter
def remove_underscore(value):
    value = value.replace('_', ' ')
    return value.title()


@register.filter(is_safe=True)
@stringfilter
def blank(value):
    if str(value) in ["", "None"]:
        return "________________"
    return value


@register.filter(is_safe=True)
@stringfilter
def empty(value):
    if str(value) == "None":
        return ""
    return value


@register.filter(is_safe=True)
@stringfilter
def verbosity(value):
    if int(value) == 1:
        return "{0} Sitting".format(value)
    return "{0} Sittings".format(value)


@register.filter(is_safe=True)
@stringfilter
def engagement_verb(value):
    if int(value) == 1:
        return "{0} engagement".format(value)
    return "{0} engagements".format(value)


@register.filter(name='username_clean')
def username_clean(username):
    names = ''
    if username:
        names = username.replace('.', " ").title()
    return names


@register.filter(name='to_hours_mins_secs')
def to_hours_mins_secs(seconds):
    duration = '0'
    if seconds:
        duration = strftime("%Hh %Mm %Ss", gmtime(seconds))
    return duration


@register.filter(name="check_engage_update_expiry")
def check_engage_update_expiry(expiry_date):
    status = False
    if expiry_date and expiry_date < current_time():
        status = True
    return status


@register.filter(name="user_profile_name")
def user_profile_name(user):
    names = ""
    if user.is_authenticated:
        try:
            names = "{} {}".format(user.profile.firstname, user.profile.surname)
        except AttributeError:
            if user.first_name and user.last_name:
                names = "{} {}".format(user.first_name, user.last_name).title()
            pass
    return names


@register.filter(name="truncate_names")
def truncate_names(names):
    _names = ""

    if names:
        all_names = names.split()
        try:
            if len(all_names) > 1: _names = "{} {}".format(all_names[0], all_names[1])
        except Exception:
            _names = names
    return _names


@register.filter(name="profile_actions")
def profile_actions(profile):
    show = False
    try:
        if profile.is_branch_manager or profile.is_vmo or profile.is_volunteer or profile.is_project_manager or profile.is_finance_manager or profile.is_supervisor:
            show = True
    except AttributeError:
        pass
    return show


@register.filter(name="show_member_links")
def show_member_links(profile):
    show = True
    try:
        if profile.is_secretary_general or profile.is_vmo or profile.is_finance_manager or profile.is_project_manager or profile.is_branch_manager or \
                profile.is_supervisor:
            show = False
    except AttributeError:
        pass
    return show


@register.filter(name='delta_days')
def delta_days(project):
    days = 0
    if project.start_date and project.end_date:
        days = (project.end_date - project.start_date).days
    return days


@register.filter(name='round_to_one')
def round_to_one(num):
    try:
        num = f'{num:.1f}'
    except Exception:
        pass
    return num


@register.simple_tag
def score_color(score, pass_mark):
    color = "blue-text text-darken 1"
    if score >= pass_mark:
        color = "green-text text-darken-1"
    else:
        color = "red-text"
    return color
