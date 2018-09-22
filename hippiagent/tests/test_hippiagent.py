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

    def test_major_hello_world(self):
        e = hippiagent.MajorEntity('v2.0.0-real-good')
        e.add_markdown('0001.md', '# Real Good Example')

        path_to_image = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graph.png")
        e.add_file("graph.png", path_to_image)
        e.add_markdown('0002.md', '![graph](graph.png)')

        a = hippiagent.Agent(url=URL, timeout=TIMEOUT)
        a.add(e)
        a.upload()

    def test_major_image(self):
        e = hippiagent.MajorEntity('v1.2.3')
        path_to_image = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graph.png")
        e.add_file("graph.png", path_to_image)
        e.add_markdown('001.md', '![graph](graph.png)')

        a = hippiagent.Agent(url=URL, timeout=TIMEOUT)
        a.add(e)
        a.upload()

    def test_major_mass(self):
        return
        e = hippiagent.MajorEntity('v1.2.3-23-g82f7a727')
        for i in range(300):
            randno = random.randint(1, 1000)
            name = "{}.md".format(randno)
            e.add_markdown(name, '# title')

        a = hippiagent.Agent(url=URL, timeout=TIMEOUT)
        a.add(e)
        a.upload()

    def mass(self):
        for i in range(5000):
            pass
