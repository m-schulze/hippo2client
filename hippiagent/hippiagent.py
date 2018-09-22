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

def create_file_entry(file_name, mime_type=None):
        """ Create file entry for object-item data or achievement. """
        # Check first if the file is available
        if not os.path.isfile(file_name):
            emsg = "File '{}' is not available".format(file_name)
            raise ArgumentException(emsg)

        if not mime_type:
            mime_type, _ = mimetypes.guess_type(file_name)
            if mime_type is None:
                mime_type = TestMimeTypes.guess_type(file_name)

        with open(file_name, "rb") as f:
            file_content = base64.b64encode(f.read())

        return file_content.decode(), mime_type

class Agent(object):

    # Supported HTTP methods
    HTTP_GET  = "GET"
    HTTP_POST = "POST"

    # URL path
    URL_API_OBJECTS = "api/v1/entity"

    def __init__(self, url=None, timeout=REQUEST_TIMEOUT):
        self.timeout = timeout
        self.url = url
        self.entities = list()

    def set_url(self, url):
        self.url = url

    def add(self, entity):
        self.entities.append(entity)

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
        full_url = "{}{}{}".format(self.url, seperator, Agent.URL_API_OBJECTS)
        data = str.encode(data)
        print(full_url)
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

    def __init__(self, id_, name='', submitter=None, lifetime=None):
        self.id = id_
        self.entries = list()
        self.name = name
        self.submitter = submitter if submitter else getpass.getuser()
        self.lifetime_group = lifetime if lifetime else 'standard'

    def add_markdown(self, name, content):
        d = dict()
        d['name'] = name
        d['content'] = content
        d['mime-type'] = 'text/markdown'
        self.entries.append(d)

    def add_file(self, name, path):
        d = dict()
        file_content, mime_type = create_file_entry(path)
        d['name'] = name
        d['content'] = file_content
        d['mime-type'] = mime_type
        d['base64-encoded'] = "true"
        self.entries.append(d)

    def encode(self):
        o = dict()
        o['type'] = 'major'
        o['major-id'] = self.id
        o['submitter'] = self.submitter
        # meta can be overwritten (but this is logged)
        o['meta'] = dict()
        o['meta']['lifetime-group'] = self.lifetime_group
        o['majors'] = self.entries
        return json.dumps(o, sort_keys=True, separators=(',', ': '))

if __name__ == "__main__":
    c = MajorEntity('ddd')
    sys.stderr.write("Python client library to interact with HippoD\n")
    sys.stderr.write("Please import this file and use provided function\n")
