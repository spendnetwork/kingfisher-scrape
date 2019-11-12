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
        current_year = datetime.datetime.now().year
        current_month = datetime.datetime.now().month
        earliest_year = 2007
        if hasattr(self, 'year'):
            current_year = int(self.year)
            earliest_year = current_year - 1
            current_month = 12
        for year in range(current_year, earliest_year, -1):
            for month in range(12, 0, -1):
                # skip months later than current
                if current_year == year and month > current_month:
                    continue
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
