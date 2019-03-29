Use - Standalone
================

You can use Scrapy in standalone mode, where you run the process manually.

Using Scrapy in standalone mode is enough if you want to download one or a few sources, or for development and testing purposes. 
For advanced usage, like running several spiders periodically, we recomment using `scrapyd <https://github.com/scrapy/scrapyd>`_, which runs as a service and runs spiders on demand.

Running
-------

To run a single source, we use the commandline interface for spiders provided by Scrapy. 
You need to run the following commands in a CLI, while being located in the folder ``kingfisher_scrape`` in the project directory.

To see available spiders:

.. code-block:: bash

    scrapy list

To run one use:

.. code-block:: bash

    scrapy crawl <spider_name> [-a key=value]

eg.

.. code-block:: bash

    scrapy crawl canada_buyandsell -a note="Started by Fred." -a sample=true

Currently kingfisher-scrape accepts 2 parameters when using the ``-a`` flag:

* **sample**: Downloads a sample of the data. 
  Having a sample is useful to know how the data is structured for a particular source, and we don't need the whole dataset yet.
  The amount of files downloaded when using the sample option depend of the implementation of the spider related to the source.
  The value used should be ``true`` and it cannot be ommited.

* **note** (to be used with kingfisher_process): Includes a note that is send with the dataset to kingfisher_process. 
  This is useful to document who started the scraping process or the reasons, or to add any other information to the dataset that can help in the future.

Output - Disk
-------------

By default, kingfisher_scrape stores the downloaded files in a folder called ``data`` inside the ``kingfisher_scrape`` directory.

Files are stored in ``data/{scraper_name}/{process_start_date_time}``. 
Note that, when the same spider is run 3 times, it means that the whole dataset will be downloaded and saved as 3 different datasets, each one in a folder named as the date and time in which the scraping process started.

If you want to change the name or location of the storage folder, look for the following line in the ``kingfisher_scrape/settings.py`` file:

.. code-block:: python

    FILES_STORE = 'data'

FILES_STORE should be a local folder with writing access for your user.


Output - Kingfisher Process
---------------------------

See the instructions to install and run kingfisher_process [HERE] if you want to use it for the storage of data.

Before running any spider, you need to configure some enviroment variables needed for kingfisher_scrape to communicate with kingfisher_process:

* KINGFISHER_API_URI: The URI in which kingfisher_process listens for requests.
* KINGFISHER_API_KEY: 
* KINGFISHER_API_LOCAL_DIRECTORY: the local directory in which kingfisher_scrape stores files (TODO add ).

In settings.py, make sure the 3 API variables are set to load from the environment. For example:

.. code-block:: python

    KINGFISHER_API_URI = os.environ.get('KINGFISHER_API_URI')
    KINGFISHER_API_KEY = os.environ.get('KINGFISHER_API_KEY')
    KINGFISHER_API_LOCAL_DIRECTORY = os.environ.get('KINGFISHER_API_LOCAL_DIRECTORY')


The ``kingfisher-process`` API endpoint variables are currently accessed from the scraper's environment. To configure:

1. Copy ``env.sh.tmpl`` to ``env.sh``
2. Set the ``KINGFISHER_*`` variables in ``env.sh`` to match your instance (local or server).
3. Run ``source env.sh`` to export them to the scraper environment.
