import scrapy


class CanadaBuyAndSell(scrapy.Spider):
    name = "canada_buyandsell"
    start_urls = ['https://buyandsell.gc.ca']

    def parse(self, response):
        urls = [
            {
                "file_urls": ['https://buyandsell.gc.ca/cds/public/ocds/tpsgc-pwgsc_ocds_EF-FY-13-14.json'],
                "data_type": "release_package",
                "filename": "13-14.json",
            },
            {
                "file_urls": ['https://buyandsell.gc.ca/cds/public/ocds/tpsgc-pwgsc_ocds_EF-FY-14-15.json'],
                "data_type": "release_package",
                "filename": "14-15.json",
            },
            {
                "file_urls": ['https://buyandsell.gc.ca/cds/public/ocds/tpsgc-pwgsc_ocds_EF-FY-15-16.json'],
                "data_type": "release_package",
                "filename": "15-16.json",
            },
            {
                "file_urls": ['https://buyandsell.gc.ca/cds/public/ocds/tpsgc-pwgsc_ocds_EF-FY-16-17.json'],
                "data_type": "release_package",
                "filename": "16-17.json",
            },
        ]
        if hasattr(self, 'sample') and self.sample == 'true':
            urls = [ urls[0] ]

        for url in urls:
            yield url
