# -*- coding: utf-8 -*-

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
#request.requires_https()

## connect to Google BigTable (optional 'google:datastore://namespace')
db = DAL('google:datastore+ndb')
from gluon.contrib.memdb import MEMDB
from google.appengine.api.memcache import Client
session.connect(request, response, db = MEMDB(Client()))
#session.connect(request, response, db=db)

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)
