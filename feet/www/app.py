# -*- coding: utf8 -*-
# feet TornadoWeb server application
#
# Author:   Romary Dupuis <romary.dupuis@altarika.com>
#
# Copyright (C) 2016 Romary Dupuis
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

"""
TornadoWeb application definition in Feet.
"""
import os
import logging

# tornado Web server
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.httpclient

from feet.www.urls import make_app
from feet.config import settings

tornado_settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
    "login_url": "/login",
    "xsrf_cookies": True,
}


def run(host, port, debug):
    app = make_app()
    app.listen(port)
    logging.info('Feet server listening on port %d' % (port))
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        logging.info('Feet server interrupted')


if __name__ == "__main__":
    # if you run this file as a script, it will start the tornado Web server
    run(host=settings.server.host, port=settings.server.port)
