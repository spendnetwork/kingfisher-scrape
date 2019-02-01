import csv
import scrapy
from datetime import date


class ParaguayDNCP(scrapy.Spider):
    name = 'paraguay_dncp'

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': { 
            'kingfisher_scrapy.middlewares.ParaguayAPIMiddleware': 1000
        },
        'RETRY_HTTP_CODES': [502, 503, 504, 408] # ignore HTTP 500
    }

    def start_requests(self):
        base_url = 'https://www.contrataciones.gov.py/images/opendata/planificaciones/{:d}.csv'
        max_year = 2011 if hasattr(self, 'sample') and self.sample == 'true' else date.today().year + 1
        for year in range(2010, max_year):
            yield scrapy.Request(base_url.format(year), meta = {'include_auth_header': False})

    def parse(self, response):
        base_url = 'https://www.contrataciones.gov.py:443/datos/api/v2/doc/ocds/record-package/{}'
        reader = csv.reader(response.text.splitlines(), delimiter = ',')
        record_ids = [row[2] for row in reader]

        #if hasattr(self, 'sample') and self.sample == 'true':
        #    record_ids = record_ids[:10]

        for record_id in record_ids:
            yield {
                'file_urls': [base_url.format(record_id)],
                'data_type': 'record_package'
            }
