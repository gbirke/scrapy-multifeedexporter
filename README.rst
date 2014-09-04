scrapy-multifeedexporter
========================

This `Scrapy <http://scrapy.org/>`__ extension exports scraped items of
different types to multiple feeds. By default each item gets its own
feed.

Installation
------------

.. code-block:: bash

    $ pip install scrapy-multifeedexporter

Configuration
-------------

You'll have to switch the default ``FeedExporter`` with
``MultiFeedExporter`` by adding the following lines to the
``settings.py`` file of your spider:

.. code:: python

    from multifeedexporter import MultiFeedExporter

    EXTENSIONS = {
        'scrapy.contrib.feedexport.FeedExporter': None,
        'multifeedexporter.MultiFeedExporter': 500,
    }

    # Automatically configure available item names from your module
    MULTIFEEDEXPORTER_ITEMS = MultiFeedExporter.get_bot_items(BOT_NAME)

Usage
-----

When calling ``scrapy crawl`` you need to use the ``%(item_name)s``
placeholder in the output file/URI name. The following calls to
``scrapy crawl`` demonstrate the placeholder:

.. code:: bash

    $ scrapy crawl -o "spider_name_%(item_name)s.csv" -t csv spider_name
    $ scrapy crawl -o "ftp://foo:bar@example.com/spider_name_%(item_name)s.csv" -t csv spider_name

If you omit the placeholder, all items will be placed in one file.

License
-------

scrapy-multifeedexporter is published under MIT license
