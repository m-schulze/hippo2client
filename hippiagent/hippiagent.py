#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import pprint
import base64
import re
import os
import sys
import datetime
import mimetypes
import getpass
import textwrap

try:
    # python3
    import urllib.request as urllib_request
except ImportError:
    # python2
    import urllib2 as urllib_request

REQUEST_TIMEOUT = 5

# custom exceptions
class ArgumentException(Exception): pass
class ConfigurationException(Exception): pass
class InternalException(Exception): pass
class TransformException(Exception): pass


class Agent(object):

    # Supported HTTP methods
    HTTP_GET  = "GET"
    HTTP_POST = "POST"

    # URL path
    URL_API_OBJECTS = "api/v1/object"

    def __init__(self, url=None, timeout=REQUEST_TIMEOUT):
        self.timeout = timeout
        self.url = url
        self.entities = list()

    def set_url(self, url):
        self.url = url

    def add(self, entity):
        self.entities.append(entities)

    def _check_pre_sync(self):
        if not self.url:
            raise ConfigurationException("no server URL specified")

    def _send_data(self, data):
        self.user_agent_headers = {'Content-type': 'application/json',
                                   'Accept': 'application/json',
                                   'User-Agent' : 'Hippodclient/1.0+'
                                   }
        seperator = "/"
        if self.url.endswith("/"): seperator = ""
        full_url = "{}{}{}".format(self.url, seperator, "api/v1/object")
        data = str.encode(data)
        req = urllib_request.Request(full_url, data, self.user_agent_headers)
        try:
            urllib_request.urlopen(req, timeout=self.timeout)
        except urllib_request.HTTPError as e:
            sys.stderr.write(str(e.read()))
            return (False, e.read())
        return (True, None)

    def _disable_proxy(self):
        # install no proxy, for proxied environments the
        # system proxy is ignore here, for localhost communication
        # this is fine, if you want to communicate via a proxy please
        # remove the following lines
        proxy_support = urllib_request.ProxyHandler({})
        opener = urllib_request.build_opener(proxy_support)
        urllib_request.install_opener(opener)

    def sync(self):
        self._disable_proxy()
        self._check_pre_sync()
        ret_list = list()
        for e in self.entities:
            data = e.encode()
            ret = self._send_data(data)
            ret_list.append(ret)
        return ret_list

    # just an alias for sync
    upload = sync

class MajorEntity(object):

    def __self__(self, id_, name='', submitter=None, lifetime=None):
        self.url = url
        self.entities = list()
        self.name = name
        self.submitter = submitter if submitter else getpass.getuser()
        self.lifetime_group = lifetime if lifetime else 'standard'

    def add_markdown(self, name, content):
        d = dict()
        d['name'] = name
        d['content'] = content
        self.entities.append(d)

    def encode(self):
        o = dict()
        o['type'] = 'major'
        o['major-id'] = self.id
        o['submitter'] = self.submitter
        # meta can be overwritten (but this is logged)
        o['meta'] = dict()
        o['meta']['lifetime-group'] = self.lifetime_group
        o['majors'] = self.entities

        return json.dumps(o, sort_keys=True, separators=(',', ': '))

if __name__ == "__main__":
    sys.stderr.write("Python client library to interact with HippoD\n")
    sys.stderr.write("Please import this file and use provided function\n")
