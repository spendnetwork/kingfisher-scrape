import datetime
import json

import scrapy

from kingfisher_scrapy.base_spider import BaseSpider


class ChileCompraRecords(BaseSpider):
    name = 'chile_compra_records'
    custom_settings = {
        'ITEM_PIPELINES': {
            'kingfisher_scrapy.pipelines.KingfisherPostPipeline': 400
        },
        'HTTPERROR_ALLOW_ALL': True,
    }
    # the data list service takes too long to be downloaded, so we increase the download timeout
    download_timeout = 300

    def start_requests(self):
        if self.is_sample():
            yield scrapy.Request(
                url='https://apis.mercadopublico.cl/OCDS/data/listaA%C3%B1oMes/2017/10',
                meta={'kf_filename': 'sample.json'}
            )
            return
        until_year = datetime.datetime.now().year + 1
        until_month = datetime.datetime.now().month
        start_year = 2008
        if hasattr(self, 'year'):
            start_year = int(self.year)
            until_year = start_year + 1
            until_month = 12
        for year in range(start_year, until_year):
            for month in range(1, 13):
                # just scrape until the current month when the until year = current year
                if (until_year-1) == year and month > until_month:
                    break
                yield scrapy.Request(
                    url='https://apis.mercadopublico.cl/OCDS/data/listaA%C3%B1oMes/{}/{:02d}'.format(year, month),
                    meta={'kf_filename': 'year-{}-month-{:02d}.json'.format(year, month)}
                )

    def parse(self, response):
        record_url = 'https://apis.mercadopublico.cl/OCDS/data/record/%s'
        if response.status == 200:
            data = json.loads(response.body_as_unicode())
            if 'NumeroError' in data:
                yield scrapy.Request(
                    url=response.request.url,
                    meta={'kf_filename': response.request.meta['kf_filename']}
                )
            elif 'ListadoOCDS' in data.keys():
                for data_item in data['ListadoOCDS']:
                    yield scrapy.Request(
                        url=record_url % data_item['Codigo'].replace('ocds-70d2nz-', ''),
                        meta={'kf_filename': 'data-%s-record.json' % data_item['Codigo']}
                    )

            else:
                yield self.save_response_to_disk(response, response.request.meta['kf_filename'], data_type='record_package')
        else:
            yield {
                'success': False,
                'file_name': response.request.meta['kf_filename'],
                'url': response.request.url,
                'errors': {'http_code': response.status}
            }
