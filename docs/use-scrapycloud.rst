Use - Scrapy Cloud (on Scrapinghub)
===================================

Configure Scrapy Cloud
------------------------

You will need an account on Scrapinghub.com, and to create a project in the Scrapy cloud.

You can create a test project for free in your user account (not an organisation).


Configure Local Scripts
-----------------------

Install the ``shub`` package.

.. code-block:: bash

  pip3 install shub

Login to shub

.. code-block:: bash

  shub login

Edit scrapinghub.yml and set the id of the project you want to use.


Deploying Scrapers
------------------

The code must be packaged up and deployed to the server

.. code-block:: bash

    shub deploy


Scheduling a run
----------------

Do this from the web interface.

To schedule a sample run, when you click run you can add arguments. Add one with the name of "sample" and the value of "true".

Output - Disk
-------------

Unfortunately, Scrapy Cloud does not let you access the files downloaded.

Instead, you have to use extra pipe line to save to Google Cloud.

Create a new Google Cloud Storage bucket. In settings, set that name in FILES_STORE.

.. code-block:: python

    FILES_STORE = 'gs://your-bucket-name-here/'

Also in settings.py, make sure ``ITEM_PIPELINES`` includes ``KingfisherFilesPipeline``.

.. code-block:: python

    ITEM_PIPELINES = {
        'kingfisher_scrapy.pipelines.GCSFilePipeline': 1,
    }

Then go to "IAM & Admin" and "service accounts". Create a new service account.
You  do not need to  "Grant this service account access to the project (optional)" or
"Grant users access to this service account (optional)", but do create a JSON Key and save that.

Go back to the storage bucket, and go to permissions.
Add the user you just created with the roles "Storage Object Creator" and "Storage Object Viewer".

Finally, take the JSON Key and edit it so it is all on one line. Go to the Scrapy Cloud project and select "Spiders" and "Settings" from the left menu.
Add the options under the "Raw Settings" tab. The format is:

.. code-block:: text

    GOOGLE_APPLICATION_CREDENTIALS = {"type": "service_account", "project_id": "...............

Output - Kingfisher Process
---------------------------

If you have set up disk output, make sure ``ITEM_PIPELINES`` includes``KingfisherPostPipeline``
 and that the 3 API variables are set to load from the environment. For example:

.. code-block:: python

    ITEM_PIPELINES = {
        'kingfisher_scrapy.pipelines.GCSFilePipeline': 1,
        'kingfisher_scrapy.pipelines.KingfisherPostPipeline': 3,
    }

    FILES_STORE = 'gs://your-bucket-name-here/'

    KINGFISHER_API_FILE_URI = os.environ.get('KINGFISHER_API_FILE_URI')
    KINGFISHER_API_ITEM_URI = os.environ.get('KINGFISHER_API_ITEM_URI')
    KINGFISHER_API_KEY = os.environ.get('KINGFISHER_API_KEY')

If you have NOT set up disk output, make sure ``ITEM_PIPELINES`` includes ``KingfisherFilesPipeline`` and ``KingfisherPostPipeline``,
that ``FILES_STORE`` is set and that the 3 API variables are set to load from the environment. For example:

.. code-block:: python

    ITEM_PIPELINES = {
        'kingfisher_scrapy.pipelines.KingfisherFilesPipeline': 2,
        'kingfisher_scrapy.pipelines.KingfisherPostPipeline': 3,
    }

    FILES_STORE = 'data'

    KINGFISHER_API_FILE_URI = os.environ.get('KINGFISHER_API_FILE_URI')
    KINGFISHER_API_ITEM_URI = os.environ.get('KINGFISHER_API_ITEM_URI')
    KINGFISHER_API_KEY = os.environ.get('KINGFISHER_API_KEY')

In other words, ``ITEM_PIPELINES`` should NOT contain both ``KingfisherFilesPipeline`` and ``GCSFilePipeline`` - only one of these is needed.

The ``kingfisher-process`` API endpoint variables are currently accessed from the Scrapy Cloud environment.
To configure these, go to the Scrapy Cloud project and select "Spiders" and "Settings" from the left menu.
Add the options under the "Raw Settings" tab. The format is:

.. code-block:: text

    KINGFISHER_API_FILE_URI = https://kingfisher.example/api/v1/submit/file/
    KINGFISHER_API_ITEM_URI = https://kingfisher.example/api/v1/submit/item/
    KINGFISHER_API_KEY = api-key-here


