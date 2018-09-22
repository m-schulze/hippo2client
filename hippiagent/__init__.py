# -*- coding: utf-8 -*-
import sys

if sys.version_info < (3, 0):
    from hippiagent import Agent
    from hippiagent import MajorEntity
else:
    from hippiagent.hippiagent import Agent
    from hippiagent.hippiagent import MajorEntity


