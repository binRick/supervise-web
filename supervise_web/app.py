from supervise_web import core
from flask import Flask, render_template, abort, Response, request, jsonify

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
                           run_log_file=core.log_file_locations(daemon_id, 'run_log')[0],
                           daemon_log_file=core.log_file_locations(daemon_id, 'daemon_log')[0],
                           autostart=core.daemon_autostart(daemon_id))


@app.route('/daemon/<daemon_id>/start', methods=['POST'])
def daemon_action_start(daemon_id):
    if not core.start_daemon(daemon_id):
        return Response(status=500)
    return Response(status=204)


@app.route('/daemon/<daemon_id>/stop', methods=['POST'])
def daemon_action_stop(daemon_id):
    if not core.stop_daemon(daemon_id):
        return Response(status=500)
    return Response(status=204)


@app.route('/daemon/<daemon_id>/start_supervise', methods=['POST'])
def daemon_action_start_supervise(daemon_id):
    core.start_supervise(daemon_id)
    return Response(status=204)


@app.route('/daemon/<daemon_id>/stop_supervise', methods=['POST'])
def daemon_action_stop_supervise(daemon_id):
    core.stop_supervise(daemon_id)
    return Response(status=204)


@app.route('/daemon/<daemon_id>/autostart', methods=['POST'])
def daemon_action_autostart(daemon_id):
    core.daemon_autostart(daemon_id, enabled=True)
    return Response(status=204)


@app.route('/daemon/<daemon_id>/no_autostart', methods=['POST'])
def daemon_action_no_autostart(daemon_id):
    core.daemon_autostart(daemon_id, enabled=False)
    return Response(status=204)


@app.route('/daemon/<daemon_id>/save_file', methods=['POST'])
def daemon_action_save_file(daemon_id):
    filename = request.form['filename']
    content = request.form['content']
    if filename == 'run':
        core.run_file(daemon_id, content)
    elif filename == 'run-user':
        core.run_file(daemon_id, content, run_user=True)
    else:
        abort(405)
    return Response(status=204)


@app.route('/daemon/<daemon_id>/log_file_locations', methods=['GET', 'POST'])
def daemon_action_log_file_locations(daemon_id):
    log_names = ['run_log', 'daemon_log']
    if request.method == 'GET':
        log_locations = core.log_file_locations(daemon_id, *log_names)
        data = {log_names[i]: log_locations[i] for i in range(len(log_locations))}
        return jsonify(data)
    else:
        kwargs = {n: request.form[n] for n in log_names}
        core.set_log_file_locations(daemon_id, **kwargs)
        return Response(status=204)


@app.route('/fetch_file', methods=['POST'])
def fetch_file():
    return core.fetch_log(request.form['file_path'])
