from supervise_web import core, helpers
from flask import Flask, render_template
app = Flask(__name__)
app.jinja_env.globals['helpers'] = helpers


@app.route('/')
def overview():
    return render_template('overview.html', daemons=core.daemon_info())