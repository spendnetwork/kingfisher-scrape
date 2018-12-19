# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import hashlib
import urllib.parse

from scrapy.pipelines.files import FilesPipeline
from scrapy.utils.python import to_bytes
from scrapy.http import FormRequest


class KingfisherFilesPipeline(FilesPipeline):

    def file_path(self, request, response=None, info=None):
        stats = info.spider.crawler.stats.get_stats()
        start_time = stats.get("start_time")
        start_time_str = start_time.strftime("%Y%m%d_%H%M%S")
        
        url = request.url
        media_guid = hashlib.sha1(to_bytes(url)).hexdigest()
        media_ext = os.path.splitext(url)[1]

        if not media_ext:
            media_ext = '.json'
        # Put files in a directory named after the scraper they came from, and the scraper starttime
        return '%s/%s/%s%s' % (info.spider.name, start_time_str, media_guid, media_ext)

    def item_completed(self, results, item, info):

        """
        This is triggered when a JSON file has finished downloading.
        """

        completed_files = []

        for ok, file_data in results:
            file_url = file_data.get("url")
            local_path = file_data.get("path")

            item_data = {
                "collection_source": info.spider.name,
                "collection_data_version": "??",
                "file_name": "TODO.json",  # TODO set to original filename?
                "file_url": file_url,
                "file_data_type": item.get("data_type"),
                "file_encoding": "",
                "local_path": local_path
            }

            completed_files.append(item_data)

        return completed_files

            


class KingfisherPostPipeline(object):

    def _build_api_url(self, spider):
        api_uri = spider.settings['KINGFISHER_API_URI']
        api_item_uri = spider.settings['KINGFISHER_API_ITEM_URI']
        api_key = spider.settings['KINGFISHER_API_KEY']
        
        # TODO: deprecate this. We want to send key in Auth header when possible
        params = {"API_KEY": api_key}
        url_parts = list(urllib.parse.urlparse(api_uri))
        query = dict(urllib.parse.parse_qsl(url_parts[4]))
        query.update(params)
        url_parts[4] = urllib.parse.urlencode(query)
        url = urllib.parse.urlunparse(url_parts)

        return url

    def process_item(self, item, spider):
        url = self._build_api_url(spider)
        local_path = item.get("local_path")
        print(url)
        print(item)
        return item

        # ????
        # request = scrapy.Request(url)
        # dfd = spider.crawler.engine.download(request, spider)
        # dfd.addBoth(self.return_item, item)
        # return dfd

        # with open(local_path, 'rb') as file:
        #     yield FormRequest(
        #         url,
        #         formdata=item,
        #         files={file_url: file},
        #         headers={'Content-Type': 'multipart/form-data'}
        #     )

