#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""

"""

import cherrypy


def check_login(usr=None, pwd=None, cky=None):
    try:
        user = cky['user'].value
        passwd = cky['password'].value
    except:
        user = usr
        passwd = pwd

    if user == 'lenovo' and passwd == 'len0vO':
        return True

    raise cherrypy.HTTPError(401, 'Authentication failed')


@cherrypy.expose
def login(user, password, press):

    check_login(usr=user, pwd=password)

    cherrypy.response.headers['Content-Type'] = 'text/xml'
    cky = cherrypy.response.cookie

    cky['user'] = user
    cky['user']['path'] = '/'
    cky['user']['max-age'] = 3600

    cky['password'] = password
    cky['password']['path'] = '/'
    cky['password']['max-age'] = 3600

    return '<?xml version="1.0" encoding="UTF-8"?><root> <status>ok</status> <authResult>0</authResult> <forwardUrl>index.html</forwardUrl> </root>'


@cherrypy.expose
def data(get=None):

    check_login(cky=cherrypy.request.cookie)

    return "HAI BRO"


class Server(object):
    pass


root = Server()
root.data = data
root.data.login = login


if __name__ == '__main__':
    cherrypy.quickstart(root, '/')
