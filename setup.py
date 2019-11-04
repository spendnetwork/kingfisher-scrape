from setuptools import setup

# Note this project is not intended to be released or used as a library!
# But because of how we deploy these scrapers into scrapyd, we need a setup.py file.

setup(
    packages=[
        'kingfisher_scrapy',
        'kingfisher_scrapy.spiders',
        'ocdskingfisher',
        'ocdskingfisher.sources',
        'ocdskingfisher.metadatabase',
        'ocdskingfisher.metadatabase.migrations',
        'ocdskingfisher.metadatabase.migrations.versions',
        'ocdskingfisher.cli',
        'ocdskingfisher.cli.commands'
    ],
    entry_points={'scrapy': ['settings = kingfisher_scrapy.settings']},
)
