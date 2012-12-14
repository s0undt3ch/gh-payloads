# -*- coding: utf-8 -*-
"""
    ghpayloads
    ~~~~~~~~~~

    Simple flask application which will get hit with GitHub payloads.

    :codeauthor: :email:`Pedro Algarvio (pedro@algarvio.me)`
    :copyright: © 2012 by the UfSoft.org Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

from flask import abort, Flask, json, jsonify, request
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.config.from_object('websiteconfig')
app.wsgi_app = ProxyFix(app.wsgi_app)  # Fix proxied environment variables

GH_PAYLOAD_IPS = (
    '207.97.227.253', '50.57.128.197', '108.171.174.178'
)


@app.before_request
def check_remote_ips():
    app.logger.debug('PRE: {0}  {1}'.format(app.view_functions, app.url_map))
    if request.remote_addr not in ('127.0.0.1',) + GH_PAYLOAD_IPS:
        abort(401)


@app.route('/', methods=['GET', 'POST'])
#@app.route('/')
def index():
    print 4
    app.logger.debug(
        'Incoming GitHub payload:\n{0}'.format(
            json.loads(request.data)
        )
    )
    return jsonify({'result': 'OK'})


@app.route('/foo')
def foo():
    pass


def run_app():
    app.run(
        app.config.get('SERVER_NAME', 'localhost'),
        app.config.get('SERVER_PORT', 5000),
        debug=app.config.get('DEBUG', False)
    )