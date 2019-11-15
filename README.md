# kingfisher-scrape for OCDS

kingfisher-scrape is part of the [OCDS Kingfisher](https://github.com/open-contracting/kingfisher) suite of tools for downloading, storing and analysing data that uses the OCDS standard. 

kingfisher-scrape allows users to download OCDS data from various publishers, using the [Scrapy](https://scrapy.org/) crawler framework. 

Full documentation can be found on [ReadTheDocs](https://kingfisher-scrape.readthedocs.io/en/latest/)


# Run Spider on webapps
    curl http://104.155.19.156:6800/schedule.json -d project=king -d spider=somespider
    curl http://104.155.19.156/schedule.json -d project=kingfisher -d spider=chile_compra_records -d note="Started by Sim."
    curl http://104.155.19.156/schedule.json -d project=kingfisher -d spider=uk_contracts_finder -d note="Started by Sim."

### Cancel

    curl http://104.155.19.156/cancel.json -d project=kingfisher -d job=ed2eeae0053611ea8d7442010af0c9b1

# Install on webapps

    mnt drive

clone to

    /mnt/disks/disk-1/kingfisher/kingfisher-scrape
    
# Start servers

start scrapy

    

# Webapps setup
    
    cd /mnt/disks/disk-1
    mkdir kingfisher
    

