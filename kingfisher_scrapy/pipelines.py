# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging

from scrapy.pipelines.files import FilesPipeline


logger = logging.getLogger(__name__)


class KingfisherScrapyPipeline(object):
    def process_item(self, item, spider):
        return item


class KingfisherFilesPipeline(FilesPipeline):

    def file_path(self, request, response=None, info=None):
        url = request.url
        media_guid = hashlib.sha1(to_bytes(url)).hexdigest()
        media_ext = os.path.splitext(url)[1]
        logger.debug(info)
        return 'test/%s%s' % (media_guid, media_ext)