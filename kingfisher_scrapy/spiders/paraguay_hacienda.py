import json

import requests

from kingfisher_scrapy.spiders.paraguay_base import ParaguayBase, AuthTokenRequest


class ParaguayHacienda(ParaguayBase):

    name = 'paraguay_hacienda'

    base_list_url = 'https://datos.hacienda.gov.py:443/odmh-api-v1/rest/api/v1/pagos/cdp?page={}'
    release_ids = []
    client_secret = None

    def start_requests(self):
        self.request_token = self.settings.get('KINGFISHER_PARAGUAY_HACIENDA_REQUEST_TOKEN')
        self.client_secret = self.settings.get('KINGFISHER_PARAGUAY_HACIENDA_CLIENT_SECRET')
        if self.request_token is None or self.client_secret is None:
            raise RuntimeError('No request token or client secret available')
        # Paraguay Hacienda has a service that return all the ids that we need to get the releases packages
        # so we first iterate over this list that is paginated
        yield AuthTokenRequest(self.base_list_url.format(1), meta={'meta': True, 'first': True, 'access_token': self.get_access_token()})

    def parse(self, response):
        if response.status == 200:

            data = json.loads(response.body_as_unicode())
            base_url = 'https://datos.hacienda.gov.py:443/odmh-api-v1/rest/api/v1/ocds/release-package/{}'

            # If is the first URL, we need to iterate over all the pages to get all the process ids to query
            if response.request.meta['first'] and not self.is_sample():
                total_pages = data['meta']['totalPages']
                for page in range(2,  total_pages+1):
                    yield AuthTokenRequest(
                        url=self.base_list_url.format(page),
                        meta={'meta': True, 'first': False, 'access_token': self.get_access_token()},
                        dont_filter=True
                    )

            # if is a meta request it means that is the page that have the process ids to query
            if response.request.meta['meta']:
                if self.is_sample():
                    data['results'] = data['results'][:50]

                # Now that we have the ids we iterate over them, without duplicate them, and make the
                # final requests for the release_package this time
                for row in data['results']:
                    if row['idLlamado'] and row['idLlamado'] not in self.release_ids:
                        self.release_ids.append(row['idLlamado'])
                        yield AuthTokenRequest(
                            url=base_url.format(row['idLlamado']),
                            meta={'meta': False, 'first': False,
                                  'kf_filename': 'release-{}.json'.format(row['idLlamado']),
                                  'access_token': self.get_access_token()},
                            dont_filter=True
                        )
            else:
                self.save_response_to_disk(response, response.request.meta['kf_filename'])
                yield {
                    'success': True,
                    'file_name': response.request.meta['kf_filename'],
                    'data_type': 'release_package',
                    'url': response.request.url,
                }
        elif response.status == 401:
            # request a new access token if needed
            self.logger.info('401! Authorization header: {}'.format(response.request.meta['access_token']))
            if response.request.meta['access_token'] == self.get_access_token():
                self.access_token = self.generate_access_token()

            meta = response.request.meta.copy()
            meta['access_token'] = self.get_access_token()
            yield AuthTokenRequest(
                url=response.request.url,
                meta=meta
            )

        else:
            yield {
                'success': False,
                'file_name': response.request.meta['kf_filename'],
                'url': response.request.url,
                'errors': {'http_code': response.status}
            }

    def generate_access_token(self):
        token = None
        attempts = 1
        self.logger.info('Requesting new access token...')
        while token is None and attempts <= ParaguayHacienda.max_auth_attempts:
            r = requests.post("https://datos.hacienda.gov.py:443/odmh-api-v1/rest/api/v1/auth/token",
                              headers={"Authorization": self.request_token},
                              json={"clientSecret": "%s" % self.client_secret})
            if 'accessToken' in r.json():
                token = r.json()['accessToken']
            attempts += 1
        if token is None:
            raise RuntimeException('Negociation of an access token has failed {} times.'.format(attempts))
        self.logger.info('New access token retrieved: {}'.format(token))
        return token
