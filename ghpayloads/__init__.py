# -*- coding: utf-8 -*-
"""
    ghpayloads
    ~~~~~~~~~~

    Simple flask application which will get hit with GitHub payloads.

    :codeauthor: :email:`Pedro Algarvio (pedro@algarvio.me)`
    :copyright: © 2012 by the UfSoft.org Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import sys
import logging
import pprint
from flask import abort, Flask, json, jsonify, request
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.config.from_object('websiteconfig')
app.wsgi_app = ProxyFix(app.wsgi_app)  # Fix proxied environment variables

GH_PAYLOAD_IPS = (
    '207.97.227.253', '50.57.128.197', '108.171.174.178'
)


formatter = logging.Formatter(
    '%(asctime)s,%(msecs)03.0f [%(name)-17s][%(levelname)-8s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logfile = logging.FileHandler(app.config.get('LOGFILE', '/tmp/gh-payloads.log'))
logfile.setLevel(logging.DEBUG)
logfile.setFormatter(formatter)

console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.DEBUG)
console.setFormatter(formatter)

logging.getLogger().addHandler(console)
logging.getLogger().addHandler(logfile)
logging.getLogger().setLevel(logging.DEBUG)


log = logging.getLogger(__name__)


@app.before_request
def check_remote_ips():
    if request.remote_addr not in ('127.0.0.1',) + GH_PAYLOAD_IPS:
        # Only accept requests from GitHub, or localhost for develoment
        abort(401)


@app.route('/', methods=['POST'])
def index():
    try:
        log.debug(
            'Incoming GitHub payload:\n{0}'.format(
                pprint.pformat(
                    json.loads(request.form.get('payload')),
                    indent=2
                )
            )
        )
    except:
        log.debug('RAW DATA: {0}'.format(request.data))
        log.debug('Args: {0}'.format(request.args))
        log.debug('Values: {0}'.format(request.values))
    return jsonify({'result': 'OK'})


@app.route('/foo')
def foo():
    pass


def run_app():
    app.run(
        app.config.get(
            'INTERNAL_SERVER_NAME',
            app.config.get('SERVER_NAME', 'localhost')
        ),
        app.config.get('SERVER_PORT', 5000),
        debug=app.config.get('DEBUG', False)
    )
