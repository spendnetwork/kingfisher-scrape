# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import hashlib
import urllib.parse
import requests

from scrapy.pipelines.files import FilesPipeline
from scrapy.utils.python import to_bytes
from scrapy.http import FormRequest


class KingfisherFilesPipeline(FilesPipeline):

    def _get_start_time(self, spider):
        stats = spider.crawler.stats.get_stats()
        start_time = stats.get("start_time")
        return start_time

    def file_path(self, request, response=None, info=None):
        start_time = self._get_start_time(info.spider)
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

        files_store = info.spider.crawler.settings.get("FILES_STORE")

        completed_files = []

        for ok, file_data in results:
            if ok:
                file_url = file_data.get("url")
                local_path = os.path.join(files_store, file_data.get("path"))

                start_time = self._get_start_time(info.spider)

                item_data = {
                    "collection_source": info.spider.name,
                    "collection_data_version": start_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "file_name": local_path,
                    "file_url": file_url,
                    "file_data_type": item.get("data_type"),
                    "file_encoding": "utf-8",
                    "local_path": local_path
                }

                completed_files.append(item_data)

        return completed_files


class KingfisherPostPipeline(object):

    def __init__(self, crawler):
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def _build_api_url(self, spider):
        api_uri = spider.settings['KINGFISHER_API_FILE_URI']
        api_item_uri = spider.settings['KINGFISHER_API_ITEM_URI']
        api_key = spider.settings['KINGFISHER_API_KEY']

        # TODO: figure out which api endpoint based on the data_type

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
        for completed in item:
            
            local_path = completed.get("local_path")
            files = {'file': open(local_path, 'rb')}
            # completed['file'] = files

            # or load json from file and send in 'body'?
            # body=json.loads(file_contents)

            # TODO: figure out what is wrong with Form Request
            # post_request = FormRequest(
            #     url=url,
            #     formdata=completed,
            #     headers={'Content-Type': 'multipart/form-data'},
            #     callback=self.test,
            # )
            # self.crawler.engine.crawl(post_request, spider)

            # Stopgap using `requests`
            # OR we need to separately log success/failure of these
            response = requests.post(url, data=completed, files=files)
        
        raise DropItem("Items posted..")
