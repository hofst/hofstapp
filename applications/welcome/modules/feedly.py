# -*- coding: UTF-8 -*-
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
    
    def get_access_token(self,redirect_uri,code):
        if self.access_token:
            return self.access_token
        params = dict(
                      client_id=self.client_id,
                      client_secret=self.client_secret,
                      grant_type='authorization_code',
                      redirect_uri=redirect_uri,
                      code=code
                      )
        
        quest_url=self._get_endpoint('v3/auth/token')
        res = requests.post(url=quest_url, params=params).json()
        # assert 'errorCode' not in res.keys(), 'The authentication failed: error code %s' % res['errorCode']
        self.access_token = res.get('access_token')
        return res
    
    def refresh_access_token(self,refresh_token):
        '''obtain a new access token by sending a refresh token to the feedly Authorization server'''
        params = dict(
                      refresh_token=refresh_token,
                      client_id=self.client_id,
                      client_secret=self.client_secret,
                      grant_type='refresh_token',
                      )
        quest_url=self._get_endpoint('v3/auth/token')
        res = requests.post(url=quest_url, params=params)
        return res.json()

    def get_user_subscriptions(self):
        '''return list of user subscriptions'''
        headers = {'Authorization': 'OAuth '+ self.access_token}
        quest_url = self._get_endpoint('v3/subscriptions')
        res = requests.get(url=quest_url, headers=headers).json()

        feeds = [Storage(feed) for feed in res][:2]
        for feed in feeds:
            feed.pubDate = datetime(1, 1, 1) + timedelta(microseconds=feed.updated)
            feed_items = [Storage(item) for item in self.get_feed_content(feed.id)["items"]]
            feed.feed_items = []
            for item in feed_items:
                new_item = Storage()
                new_item.title = item.title
                new_item.content = item.summary.get("content")
                new_item.link = item.alternate[0]["href"] if item.alternate else ""
                new_item.author = item.author
                new_item.guid = item.id
                new_item.pubDate = datetime(1, 1, 1) + timedelta(microseconds=item.published)
                new_item.unread = item.unread
                new_item.keywords = item.keywords
                new_item.image = item.enclosure[0]["href"] if item.enclosure else item.visual["url"] if item.visual else ""
                feed.feed_items += [new_item]

        return feeds
    
    def get_feed_content(self, streamId, unreadOnly=True, newerThan=0):
        '''return contents of a feed'''
        headers = {'Authorization': 'OAuth '+ self.access_token}
        quest_url=self._get_endpoint('v3/streams/contents')
        params = dict(
                      streamId=streamId,
                      unreadOnly=unreadOnly,
                      newerThan=newerThan
                      )
        res = requests.get(url=quest_url, params=params,headers=headers)
        return res.json()
    
    def mark_article_read(self, access_token, entryIds):
        '''Mark one or multiple articles as read'''
        headers = {'content-type': 'application/json',
                   'Authorization': 'OAuth ' + access_token
        }
        quest_url = self._get_endpoint('v3/markers')
        params = dict(
                      action="markAsRead",
                      type="entries",
                      entryIds=entryIds,
                      )
        res = requests.post(url=quest_url, data=json.dumps(params), headers=headers)
        return res
    
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
