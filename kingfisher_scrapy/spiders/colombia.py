import hashlib
import json
import time
from json import JSONDecodeError

import scrapy

from kingfisher_scrapy.base_spider import BaseSpider


class Colombia(BaseSpider):
    name = 'colombia'
    sleep = 120 * 60
    custom_settings = {
        'ITEM_PIPELINES': {
            'kingfisher_scrapy.pipelines.KingfisherPostPipeline': 400
        },
        'HTTPERROR_ALLOW_ALL': True,
    }

    def start_requests(self):
        base_url = 'https://apiocds.colombiacompra.gov.co:8443/apiCCE2.0/rest/releases?page=%d'
        start_page = 1
        if hasattr(self, 'page'):
            start_page = int(self.page)
        yield scrapy.Request(
            url=base_url % start_page,
            meta={'kf_filename': 'page{}.json'.format(start_page)}
        )

    def parse(self, response):
        # In Colombia, every day at certain hour they run a process in their system that drops the database and make
        # the services unavailable for about 120 minutes, as Colombia has a lot of data,
        # the spider takes more than one day to scrape all the data,
        # so eventually the spider will always face the service problems. For that, when the problem occurs, (503
        # status or invalid json) we wait 120 minutes and then continue
        try:

            if response.status == 503:
                time.sleep(self.sleep)
                yield scrapy.Request(response.url)

            elif response.status == 200:

                yield self.save_response_to_disk(response, response.request.meta['kf_filename'], data_type="release_package")

                json_data = json.loads(response.body_as_unicode())
                if not self.is_sample():
                    if 'links' in json_data and 'next' in json_data['links']:
                        url = json_data['links']['next']
                        yield scrapy.Request(
                            url=url,
                            meta={'kf_filename': hashlib.md5(url.encode('utf-8')).hexdigest() + '.json'}
                        )

            else:

                yield {
                    'success': False,
                    'file_name': response.request.meta['kf_filename'],
                    "url": response.request.url,
                    "errors": {"http_code": response.status}
                }

        except JSONDecodeError:
            time.sleep(self.sleep)
            yield scrapy.Request(response.url)
