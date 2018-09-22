import os
import tempfile
import shutil
import textwrap
import string
import random

from unittest import TestCase

import hippiagent



URL = "http://localhost:8080/"
TIMEOUT = 10


class TestHippiAgent(TestCase):

    def test_is_initiable(self):
        hippiagent.Agent(url=URL, timeout=TIMEOUT)

    def test_hello_world(self):
        e = hippiagent.MajorEntity('v1.2.3-23-g82f7a727')
        e.add_markdown('0001.md', '# title')

        a = hippiagent.Agent(url=URL, timeout=TIMEOUT)
        a.add(e)
        a.upload()

    def mass(self):
        for i in range(5000):
            pass
