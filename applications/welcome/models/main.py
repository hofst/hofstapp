# -*- coding: UTF-8 -*-
__author__ = 'Basti'

import logging
from pprint import pprint
from gluon.storage import Storage
from datetime import datetime, timedelta, time
from google.appengine.ext import ndb
from google.appengine.api import taskqueue
from collections import OrderedDict