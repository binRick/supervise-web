from supervise_web import core
from functools import wraps
from flask import Flask, render_template, abort, Response, request

app = Flask(__name__)


@app.before_request
def before_request():
    auth = request.authorization
    if not auth or not (core.config.get('Main', 'auth_username') == auth.username
                        and core.config.get('Main', 'auth_password') == auth.password):
        return Response('You need to be authenticated', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route('/')
def overview():
    return render_template('overview.html')


@app.route('/_daemons')
def _daemons():
    return render_template('_daemons.html', daemons=core.daemon_info())


@app.route('/daemon/<daemon_id>/_details')
def _details(daemon_id):
    return render_template('_details.html',
                           daemon_id=daemon_id,
                           run_file_content=core.run_file(daemon_id),
                           run_user_file_content=core.run_file(daemon_id, run_user=True),
                           log_tail=core.log_tail(daemon_id, 1000),
                           autostart=core.daemon_autostart(daemon_id))


@app.route('/daemon/<daemon_id>/<action>', methods=['POST'])
def daemon_action(daemon_id, action):
    if action == 'start':
        if not core.start_daemon(daemon_id):
            return Response(status=500)
    elif action == 'stop':
        if not core.stop_daemon(daemon_id):
            return Response(status=500)
    elif action == 'start_supervise':
        core.start_supervise(daemon_id)
    elif action == 'stop_supervise':
        core.stop_supervise(daemon_id)
    elif action == 'autostart':
        core.daemon_autostart(daemon_id, enabled=True)
    elif action == 'no_autostart':
        core.daemon_autostart(daemon_id, enabled=False)
    elif action == 'save_file':
        filename = request.form['filename']
        content = request.form['content']
        if filename == 'run':
            core.run_file(daemon_id, content)
        elif filename == 'run-user':
            core.run_file(daemon_id, content, run_user=True)
        else:
            abort(405)
    else:
        abort(405)
    return Response(status=204)