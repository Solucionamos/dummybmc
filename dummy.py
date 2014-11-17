#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""

"""

import sys
import cherrypy
import xmlbuilder


def check_login(usr=None, pwd=None, cky=None):
    try:
        user = cky['user'].value
        passwd = cky['password'].value
    except:
        user = usr
        passwd = pwd

    if user == 'lucionamos' and passwd == '6lucio9':
        return True

    return False


@cherrypy.expose
def login(user, password, press):

    auth = check_login(usr=user, pwd=password)

    cherrypy.response.headers['Content-Type'] = 'text/xml'

    if auth:
        cky = cherrypy.response.cookie

        cky['user'] = user
        cky['user']['path'] = '/'
        cky['user']['max-age'] = 3600

        cky['password'] = password
        cky['password']['path'] = '/'
        cky['password']['max-age'] = 3600

    return xmlbuilder.login(auth)


@cherrypy.expose
def data(get=None, set=None):

    check_login(cky=cherrypy.request.cookie)

    if not set:
        return xmlbuilder.build(get)
    else:
        return ''


class Server(object):
    pass


root = Server()
root.data = data
root.data.login = login


if __name__ == '__main__':
    if len(sys.argv) == 1:
        cherrypy.server.socket_port = 8080
    elif len(sys.argv) == 2:
        cherrypy.server.socket_port = int(sys.argv[1])
    else:
        print 'wrong number of arguments'
        exit(1)

    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.tree.mount(root, '/')
    cherrypy.engine.start()
