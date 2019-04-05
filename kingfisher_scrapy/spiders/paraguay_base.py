from datetime import datetime

import requests
from scrapy import Request
from scrapy.http import Headers
from scrapy.utils import spider

from kingfisher_scrapy.base_spider import BaseSpider

# All the Paraguay services has a auth system that is based on access token that expires after a certain amount of
# request or a certain amount of time, with this class we manage the generation and regeneration of that access token

class ParaguayBase(BaseSpider):

    max_auth_attempts = 5

    custom_settings = {
        'ITEM_PIPELINES': {
            'kingfisher_scrapy.pipelines.KingfisherPostPipeline': 400
        },
        'HTTPERROR_ALLOW_ALL': True,
    }
    request_token = None
    
    # Generate a new access token or return the existing one if it is still valid
    def get_access_token(self):
        if not hasattr(self,'access_token'):
            self.access_token = self.generate_access_token()
        return self.access_token

    # Generate a new access token
    def generate_access_token(self):
        self.logger.info('Requesting new access token...')
        attempts = 1
        token = None
        while token is None and attempts <= ParaguayBase.max_auth_attempts:
            r = requests.post('https://www.contrataciones.gov.py:443/datos/api/oauth/token',
                              headers={'Authorization': self.request_token})
            if 'access_token' in r.json():
                token = r.json()['access_token']
            attempts += 1
        if token is None:
            raise RuntimeException('Negociation of an access token has failed {} times.'.format(attempts))
        self.logger.info('New access token retrieved: {}'.format(token))
        return 'Bearer ' + token


# A custom request class to use as header the most updated access token, with this, we can have concurrent request
# and we can recover a 401 status
class AuthTokenRequest(Request):
    def __init__(self, *args, **kwargs):
        if 'meta' in kwargs and 'access_token' in kwargs['meta']:
            access_token=kwargs['meta']['access_token']
            if not 'headers' in kwargs:
                kwargs['headers'] = {}
            kwargs['headers']['Authorization'] = access_token
        super(AuthTokenRequest, self).__init__(*args, **kwargs)
