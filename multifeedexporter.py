""" Scrapy extension to export scraped items of different types to multiple feeds. """

import inspect
import importlib

from datetime import datetime

from twisted.internet import defer

from scrapy import log
from scrapy.contrib.feedexport import FeedExporter, SpiderSlot

__version__ = '0.1.0'

class MultiFeedExporter(FeedExporter):

    def __init__(self, settings):
        super( MultiFeedExporter, self ).__init__(settings)
        self.item_names = settings['MULTIFEEDEXPORTER_ITEMS']
        self.slots = {}
        self.item2uri = {}

    @classmethod
    def get_bot_items(cls, bot_name):
        """ Get item names from items module of the given bot module name
        """
        item_module = importlib.import_module(bot_name + ".items")
        item_names = [name for name,obj in inspect.getmembers(item_module, inspect.isclass)]
        return item_names

    def open_spider(self, spider):
        uri_slots = {}
        for item_name in self.item_names :
            up = self._get_uri_params(spider, item_name)
            uri = self.urifmt % up
            if uri not in self.slots: 
                storage = self._get_storage(uri)
                file = storage.open(spider)
                exporter = self._get_exporter(file)
                exporter.start_exporting()
                self.slots[uri] = SpiderSlot(file, exporter, storage, uri)
            self.item2uri[item_name] = uri

    def close_spider(self, spider):
        deferreds = []
        for uri in self.slots:
            slot = self.slots[uri]
            if not slot.itemcount and not self.store_empty:
                continue
            slot.exporter.finish_exporting()
            logfmt = "%%s %s feed (%d items) in: %s" % (self.format, \
                slot.itemcount, slot.uri)
            d = defer.maybeDeferred(slot.storage.store, slot.file)
            d.addCallback(lambda _,logfmt=logfmt: log.msg(logfmt % "Stored", spider=spider))
            d.addErrback(log.err, logfmt % "Error storing", spider=spider)
            deferreds.append(d)
        
        if deferreds:
            return defer.DeferredList(deferreds)


    def item_scraped(self, item, spider):
        item_name = type(item).__name__
        slot = self.slots[self.item2uri[item_name]]
        slot.exporter.export_item(item)
        slot.itemcount += 1
        return item        

    def _get_uri_params(self, spider, item_name):
        params = {}
        for k in dir(spider):
            params[k] = getattr(spider, k)
        ts = datetime.utcnow().replace(microsecond=0).isoformat().replace(':', '-')
        params['time'] = ts
        params['item_name'] = item_name
        self._uripar(params, spider)
        return params
