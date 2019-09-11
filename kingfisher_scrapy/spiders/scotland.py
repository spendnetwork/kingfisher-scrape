import scrapy
import datetime

from kingfisher_scrapy.base_spider import BaseSpider


class Scotland(BaseSpider):
    name = 'scotland'
    custom_settings = {
        'ITEM_PIPELINES': {
            'kingfisher_scrapy.pipelines.KingfisherPostPipeline': 400
        },
        'HTTPERROR_ALLOW_ALL': True,
    }

    notice_types = [
        1,  # OJEU - F1 - Prior Information Notice
        2,  # OJEU - F2 - Contract Notice
        3,  # OJEU - F3 - Contract Award Notice
        4,  # OJEU - F4 - Prior Information Notice(Utilities)
        5,  # OJEU - F5 - Contract Notice(Utilities)
        6,  # OJEU - F6 - Contract Award Notice(Utilities)
        7,  # OJEU - F7 - Qualification Systems(Utilities)
        12,  # OJEU - F12 - Design Contest Notice
        13,  # OJEU - F13 - Results Of Design Contest
        14,  # OJEU - F14 - Corrigendum
        15,  # OJEU - F15 - Voluntary Ex Ante Transparency Notice
        20,  # OJEU - F20 - Modification Notice
        21,  # OJEU - F21 - Social And other Specific Services(Public Contracts)
        22,  # OJEU - F22 - Social And other Specific Services(Utilities)
        23,  # OJEU - F23 - Social And other Specific Services(Concessions)
        24,  # OJEU - F24 - Concession Notice
        25,  # OJEU - F25 - Concession Award Notice
        101,  # Site Notice - Website Contract Notice
        102,  # Site Notice - Website Prior Information Notice
        103,  # Site Notice - Website Contract Award Notice
        104,  # Site Notice - Quick Quote Award
    ]

    def start_requests(self):
        now = datetime.datetime.today()
        if self.is_sample():
            marker = now - datetime.timedelta(days=14)
            for notice_type in self.notice_types:
                yield scrapy.Request(
                    url='https://api.publiccontractsscotland.gov.uk/v1/Notices?dateFrom={}&outputType=1&noticeType={}'.format(
                        marker, notice_type),
                    meta={'kf_filename': 'sample_{}.json'.format(notice_type)}
                )
        else:
            # It's meant to go back a year, but in testing it seemed to be year minus one day!
            marker = now - datetime.timedelta(days=364)
            while marker <= now:
                datestring = '{:04d}-{:02d}-{:02d}'.format(marker.year, marker.month, marker.day)
                for notice_type in self.notice_types:
                    yield scrapy.Request(
                        url='https://api.publiccontractsscotland.gov.uk/v1/Notices?dateFrom={}&outputType=1&noticeType={}'.format(
                            datestring, notice_type),
                        meta={'kf_filename': '{}_type_{}.json'.format(datestring, notice_type)}
                    )
                marker = marker + datetime.timedelta(days=14)

    def parse(self, response):
        if response.status == 200:
            yield self.save_response_to_disk(response, response.request.meta['kf_filename'], data_type="release_package")
        else:
            yield {
                'success': False,
                'file_name': response.request.meta['kf_filename'],
                "url": response.request.url,
                "errors": {"http_code": response.status}
            }
