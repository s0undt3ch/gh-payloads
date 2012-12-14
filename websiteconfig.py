# -*- coding: utf-8 -*-
"""
    websiteconfig.py
    ~~~~~~~~~~~~~~~~

    Flask application configuration

    :codeauthor: :email:`Pedro Algarvio (pedro@algarvio.me)`
    :copyright: © 2012 by the UfSoft.org Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""
import os

DEBUG = True
SERVER_PORT = 5123
SERVER_NAME = 'gh-payloads.ufsoft.org'
INTERNAL_SERVER_NAME = 'localhost'
PROPAGATE_EXCEPTIONS = True
LOGFILE = os.path.join(os.path.dirname(__file__), 'gh-payloads.log')
