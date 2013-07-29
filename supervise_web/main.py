import os
import supervise_web
from supervise_web import core
from supervise_web.app import app
import mimetypes
from supervise_web import helpers
from flask.ext.scss import Scss
import ConfigParser


if __name__ == "__main__":
    app.debug = True
    package_root = os.path.dirname(supervise_web.__file__)
    Scss(app, asset_dir=os.path.join(package_root, 'assets'), static_dir=os.path.join(package_root, 'static/css'))
    app.jinja_env.globals['helpers'] = helpers
    mimetypes.add_type('application/x-font-woff', '.woff')

    core.config = ConfigParser.RawConfigParser()
    with open('supervise_web.cfg', 'r') as f:
        core.config.readfp(f)

    local = core.config.getboolean('Main', 'local')
    host = '127.0.0.1' if local else '0.0.0.0'
    port = core.config.getint('Main', 'port')
    app.run(host=host, port=port, debug=True)
