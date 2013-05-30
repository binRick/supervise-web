from supervise_web import core
from supervise_web.app import app
import mimetypes
from supervise_web import helpers
from flask.ext.scss import Scss
import ConfigParser


if __name__ == "__main__":
    app.debug = True
    Scss(app, asset_dir='supervise_web/assets', static_dir='supervise_web/static/css')
    app.jinja_env.globals['helpers'] = helpers
    mimetypes.add_type('application/x-font-woff', '.woff')

    core.config = ConfigParser.RawConfigParser()
    with open('supervise_web.cfg', 'r') as f:
        core.config.readfp(f)


    app.run(host='0.0.0.0', debug=True)