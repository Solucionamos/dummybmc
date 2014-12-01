#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

""" Implementation of a simple HTTP connection module for the BMC. Requires a
    server object on creation. Currently supports the following requests:
        /data/login - with user, password and press data.
        /data/logout - no parameters.
        /data?get=[pwState|temperatures|fans|voltages]
        /data?set=pwState:[0|1|2|3]
"""

import cherrypy

class HttpConnection(object):
    def __init__(self, server, port=8080):
        self.__server = server
        cherrypy.server.socket_port = port
        cherrypy.server.socket_host = '0.0.0.0'
        cherrypy.tree.mount(self.data, '/data')
        cherrypy.tree.mount(self.login, '/data/login')
        cherrypy.tree.mount(self.logout, '/data/logout')
        cherrypy.engine.start()


    @cherrypy.expose
    @cherrypy.tools.response_headers(headers=[('Content-Type', 'text/xml')])
    def login(self, user, password, press):
        """ Login handler, generates a cookie if authentication succeeds. """
        if self.__server.check_login(user, password):
            cookie = cherrypy.response.cookie
            cookie['user'] = user
            cookie['user']['path'] = '/'
            cookie['user']['max-age'] = 3600
            cookie['password'] = password
            cookie['password']['path'] = '/'
            cookie['password']['max-age'] = 3600

        return self.__server.login(user, password)


    @cherrypy.expose
    @cherrypy.tools.response_headers(headers=[('Content-Type', 'text/xml')])
    def data(self, get=None, set=None):
        """ Handler of /data?get= and /data?set= requests. Requires
            authentication cookie.
        """
        auth = self.__check_auth(cherrypy.request.cookie)

        if not auth:
            raise cherrypy.HTTPError(401)

        if set:
            parameter, value = set.split(':')
            if parameter == 'pwState':
                return self.__server.setPwState(int(value))
        else:
            return self.__server.get(get)


    @cherrypy.expose
    def logout(self):
        """ Logout handler. Should return HTTP status 302 for faithfulness with
            actual server response, but it caused problems with Android app.
        """
        return 'Not implemented\n'


    def __check_auth(self, cookie):
        """ Helper method. Checks validity of authentication data within the
            provided cookie.
        """
        if cookie:
            user = cookie['user'].value
            password = cookie['password'].value
            return self.__server.check_login(user, password)
        return False

