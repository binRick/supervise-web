"""
Helper functions to be used in Jinja templates
"""
import datetime


def daemon_row_css_class(daemon_data):
    # success, error, warning, info
    if not daemon_data['alive']:
        return 'supervise_not_running'
    elif not daemon_data['daemon_up']:
        return 'daemon_not_running'
    elif datetime.datetime.now() - daemon_data['daemon_timestamp'] < datetime.timedelta(seconds=15):
        return 'daemon_starting'
    else:
        return 'daemon_running'


def daemon_action_buttons(daemon_data):
    if not daemon_data['alive']:
        return '<button class="btn-start-supervise">Start Supervise</button>'
    if daemon_data['daemon_up']:
        return '<button class="btn-stop">Stop</button>'
    else:
        return '<button class="btn-start">Start</button>'


def daemon_status(daemon_data):
    if not daemon_data['alive']:
        return 'not supervised'
    if not daemon_data['daemon_up']:
        return 'not running'
    now = datetime.datetime.now()
    ts = daemon_data['daemon_timestamp']
    delta = now - ts if now >= ts else datetime.timedelta()
    if delta < datetime.timedelta(seconds=15):
        return 'just started, running for %s' % timedelta_to_str(delta)
    return 'running for %s' % timedelta_to_str(delta)


def timedelta_to_str(delta):
    out = ''
    if delta.days:
        out += '%d day%s ' % (delta.days, 's' if delta.days > 1 else '')
    seconds = delta.seconds
    hours = seconds / 3600
    seconds -= hours * 3600
    minutes = seconds / 60
    seconds -= minutes * 60

    if out or hours or minutes:
        out += '%02d:%02d:%02d' % (hours, minutes, seconds)
    else:
        out += '%d secs' % seconds
    return out