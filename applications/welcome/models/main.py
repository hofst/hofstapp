# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'Sebastian Hofstetter'

import logging
from pprint import pprint
from gluon.storage import Storage
from datetime import datetime, timedelta, time
from google.appengine.ext import ndb
from google.appengine.api import taskqueue
from collections import OrderedDict
from util import s, uni