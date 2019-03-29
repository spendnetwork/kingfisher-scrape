kingfisher-scrape for OCDS
==========================

kingfisher-scrape is a tool to download `OCDS <http://standard.open-contracting.org>`_ data from various sources, and to store it on disk and/or send it to an instance of `kingfisher-process <https://github.com/open-contracting/kingfisher-process>`_. It is built using the `Scrapy <https://scrapy.org/>`_ crawler framework.

kingfisher-scrape makes available several sources, written as Scrapy spiders, from known OCDS publishers. If you want to download data from a source not included in the list, you can write and include your own spider. See the instructions in :ref:`writing-scrapers`.

kingfisher-scrape can be used in two ways:

- *Standalone*, which allows to download from sources manually. Can be used for downloading data from a single source, or for development and testing of scrapers.
- *As a service*, to schedule and run several spiders in an efficient manner. For this, you will need to use an external tool. We recommend using `scrapyd <https://github.com/scrapy/scrapyd>`_.

For database storage (plus analytics utilities), please take a look at `kingfisher-process <https://github.com/open-contracting/kingfisher-process>`_, which works in conjunction with kingfisher-scrape.

The Open Contracting Partnership operate a hosted instance of kingfisher-scrape, which is available to OCP staff and the OCDS Team. For information about how to access this, see the `hosted kingfisher documentation <https://ocdskingfisher.readthedocs.io/en/latest/#hosted-kingfisher>`_.

`Scrapy Cloud <https://scrapinghub.com/scrapy-cloud>`_ is an alternative to run kingfisher-scrape as a service in the cloud for free. The developers have tested kingfisher-scrape on Scrapy Cloud and it works, but the limitations of the service (specifically, not being able to write to a readable file storage and send to the Process API at the same time) mean that it's not suitable for OCP use. You may, however, find this a helpful service.

.. toctree::

   setup.rst
   sources.rst
   use-standalone.rst
   use-scrapyd.rst
   use-hosted.rst
   use-scrapycloud.rst
   writing-scrapers.rst
   old.rst
