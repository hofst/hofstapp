# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'Sebastian Hofstetter'

import requests
import json
from datetime import datetime, timedelta
from gluon.storage import Storage


class FeedlyClient(object):
    def __init__(self, **options):
        self.client_id = options.get('client_id')
        self.client_secret = options.get('client_secret')
        self.sandbox = options.get('sandbox', True)
        if self.sandbox:
            default_service_host = 'sandbox.feedly.com'
        else:
            default_service_host = 'cloud.feedly.com'
        self.service_host = options.get('service_host', default_service_host)
        self.additional_headers = options.get('additional_headers', {})
        self.secret = options.get('secret')
        self.access_token = options.get('access_token', None)

    def get_code_url(self, callback_url):
        scope = 'https://cloud.feedly.com/subscriptions'
        response_type = 'code'

        request_url = '%s?client_id=%s&redirect_uri=%s&scope=%s&response_type=%s' % (
            self._get_endpoint('v3/auth/auth'),
            self.client_id,
            callback_url,
            scope,
            response_type
        )
        return request_url

    def get_access_token(self, redirect_uri, code):
        if self.access_token:
            return Storage(access_token=self.access_token)
        params = dict(
            client_id=self.client_id,
            client_secret=self.client_secret,
            grant_type='authorization_code',
            redirect_uri=redirect_uri,
            code=code
        )

        quest_url = self._get_endpoint('v3/auth/token')
        res = requests.post(url=quest_url, params=params).json()
        # assert 'errorCode' not in res.keys(), 'The authentication failed: error code %s' % res['errorCode']
        self.access_token = res.get('access_token')
        return res

    def refresh_access_token(self, refresh_token):
        '''obtain a new access token by sending a refresh token to the feedly Authorization server'''
        params = dict(
            refresh_token=refresh_token,
            client_id=self.client_id,
            client_secret=self.client_secret,
            grant_type='refresh_token',
        )
        quest_url = self._get_endpoint('v3/auth/token')
        res = requests.post(url=quest_url, params=params)
        return res.json()

    def get_subscriptions(self):
        '''return list of user subscriptions  '''
        headers = {'Authorization': 'OAuth ' + self.access_token}
        quest_url = self._get_endpoint('v3/subscriptions')
        res = requests.get(url=quest_url, headers=headers).json()
        if "errorCode" in res:
            raise Exception(res["errorMessage"])

        return [Storage(feed) for feed in res]

    def get_news_dics(self, **kwargs):
        news_dics = []
        feeds = self.get_subscriptions()
        for feed in feeds:
            feed.pubDate = datetime(1970, 1, 1) + timedelta(milliseconds=feed.updated) if feed.updated else ""
            news_dics += [Storage(item) for item in self.get_feed_content(feed.id)["items"]]
        return news_dics

    def get_feed_content(self, streamId, unreadOnly=True, newerThan=int((datetime.now() - timedelta(days=2) - datetime(1970, 1, 1)).total_seconds() * 1000)):
        '''return contents of a feed'''
        headers = {}  # {'Authorization': 'OAuth '+ self.access_token}  # authorization is optional! But without authorization unreadOnly does not work. With authorization each call counts to the 250 limit of a developer token
        quest_url = self._get_endpoint('v3/streams/contents')
        params = dict(
            count=1000,
            streamId=streamId,
            unreadOnly=unreadOnly,
            newerThan=newerThan
        )
        res = requests.get(url=quest_url, params=params, headers=headers, timeout=60)
        return res.json()

    def mark_article_read(self, entryIds):
        '''Mark one or multiple articles as read'''
        headers = {'content-type': 'application/json',
                   'Authorization': 'OAuth ' + self.access_token
        }
        quest_url = self._get_endpoint('v3/markers')

        ## Can only mark up to 1000 articels at once ##
        for chunk in [entryIds[x:x + 1000] for x in xrange(0, len(entryIds), 1000)]:
            params = dict(
                action="markAsRead",
                type="entries",
                entryIds=chunk,
            )
            requests.post(url=quest_url, data=json.dumps(params), headers=headers)

    def save_for_later(self, access_token, user_id, entryIds):
        '''saved for later.entryIds is a list for entry id.'''
        headers = {'content-type': 'application/json',
                   'Authorization': 'OAuth ' + access_token
        }
        request_url = self._get_endpoint('v3/tags') + '/user%2F' + user_id + '%2Ftag%2Fglobal.saved'

        params = dict(
            entryIds=entryIds
        )
        res = requests.put(url=request_url, data=json.dumps(params), headers=headers)
        return res

    def _get_endpoint(self, path=None):
        url = "https://%s" % (self.service_host)
        if path is not None:
            url += "/%s" % path
        return url
