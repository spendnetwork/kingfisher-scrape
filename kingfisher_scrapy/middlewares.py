# -*- coding: utf-8 -*-
import scrapy
import requests
import logging

from kingfisher_scrapy import spiders


class ParaguayAPIMiddleware(object):
    
    request_token = None
    access_token = None
    _lock = False

    def __init__(self, request_token=None):
        if request_token is None:
            raise RuntimeError('No request token available')
        ParaguayAPIMiddleware.request_token = request_token

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings.get('KINGFISHER_PARAGUAY_REQUEST_TOKEN'))

    def _request_access_token(self):
        logging.info('Using request token: ' + ParaguayAPIMiddleware.request_token)
        response = requests.post("https://www.contrataciones.gov.py:443/datos/api/oauth/token", headers={"Authorization": ParaguayAPIMiddleware.request_token})
        try:
            ParaguayAPIMiddleware.access_token = response.json()['access_token']
            logging.info('New request access token: ' + ParaguayAPIMiddleware.access_token)
        except requests.exceptions.RequestException:
            raise RuntimeError('Exception when requesting API Key')

    def _get_auth_string(self):
        if ParaguayAPIMiddleware.access_token is None:
            return None
        return 'Bearer ' + ParaguayAPIMiddleware.access_token

    def process_request(self, request, spider):
        if 'include_auth_header' in request.meta and request.meta['include_auth_header'] == False:
            return None # a few initial requests do not require the authentication header
        
        if ParaguayAPIMiddleware.access_token is None:
            self._request_access_token()

        if not 'Authorization' in request.headers:
            request.headers['Authorization'] = self._get_auth_string()
        return None # request goes ahead as planned

    def process_response(self, request, response, spider):
        if response.status == 401: # unauthorized!
            logging.warning('Expired API token when retrieving ' + request.url)
            if 'Authorization' in request.headers \
                and request.headers['Authorization'] == self._get_auth_string():
                # request new key
                self._request_access_token() 
            request.headers['Authorization'] = self._get_auth_string()
            return request # drop the response, put this modified request in scheduler queue
        return response
