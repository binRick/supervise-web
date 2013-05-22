from supervise_web.app import app
import mimetypes
from supervise_web import helpers
from flask.ext.scss import Scss

if __name__ == "__main__":
    app.debug = True
    Scss(app, asset_dir='assets', static_dir='static/css')
    app.jinja_env.globals['helpers'] = helpers
    mimetypes.add_type('application/x-font-woff', '.woff')

    app.run(host='0.0.0.0', debug=True)