# kingfisher-scrape for OCDS

kingfisher-scrape is part of the [OCDS Kingfisher](https://github.com/open-contracting/kingfisher) suite of tools for downloading, storing and analysing data that uses the OCDS standard. 

kingfisher-scrape allows users to download OCDS data from various publishers, using the [Scrapy](https://scrapy.org/) crawler framework. 

Full documentation can be found on [ReadTheDocs](https://kingfisher-scrape.readthedocs.io/en/latest/)


# Run Spider on webapps
curl http://104.155.19.156:6800/schedule.json -d project=king -d spider=somespider


# Install

    clone
    mnt drive

symlink drive

    ln -s /mnt/disks/disk-1/sim/kingfisher-scrape data