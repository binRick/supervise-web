from supervise_web import core, helpers
from flask import Flask, render_template, abort
app = Flask(__name__)
app.jinja_env.globals['helpers'] = helpers


@app.route('/')
def overview():
    return render_template('overview.html')


@app.route('/_daemons.html')
def _daemons():
    return render_template('_daemons.html', daemons=core.daemon_info())


@app.route('/daemon/<daemon_id>/<action>', methods=['POST'])
def daemon_action(daemon_id, action):
    if action == 'start':
        return 'ok' if core.start_daemon(daemon_id) else ''
    elif action == 'stop':
        return 'ok' if core.stop_daemon(daemon_id) else ''
    else:
        abort(400)