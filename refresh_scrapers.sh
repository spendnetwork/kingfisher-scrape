#!/bin/bash

# get the list of all the scrapers, less the ones that have run recently or are currently running

psql -U ocdskfpreadonly -d ocdskingfisherprocess -h localhost -c "select source_id from collection where
transform_from_collection_id is null and ( store_end_at is null or store_end_at >= now() - interval '1 month')" -qAtX > /tmp/recent_scrapes.$$

echo "__init__\n" >> /tmp/recent_scrapes.$$
echo "test_fail\n" >> /tmp/recent_scrapes.$$

for spider in $(ls /home/ocdskfs/ocdskingfisherscrape/kingfisher_scrapy/spiders | sed 's/.py//' | grep -vf /tmp/recent_scrapes.$$); do 
  /usr/bin/curl http://localhost:6800/schedule.json -d project=kingfisher -d spider=${spider}
done;	

rm -f /tmp/recent_scrapes.$$
