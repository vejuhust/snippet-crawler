#!/usr/bin/env python3
"""Database accessors for snippet crawler"""

from config import *
from contextlib import closing
from datetime import datetime
from pymongo import MongoClient, ASCENDING


class DatabaseAccessor():
    """Database Accessor for connecting MongoDB"""
    def __init__(self):
        self._client = MongoClient(host=config_db_addr, port=config_db_port)
        self._db = self._client[config_db_name]
        if not self._db.authenticate(config_db_user, config_db_pass):
            raise RuntimeError("Failed to authenticate for {}@{}".format(config_db_user, config_db_addr))
        self._validate_collections()


    def close(self):
        self._client.close()


    def _validate_collections(self):
        names = self._db.collection_names()
        collections = [config_db_snippet, config_queue_crawl, config_queue_page]
        for collection in collections:
            if collection not in names:
                try:
                    self._db.create_collection(collection)
                    self._db[collection].create_index([('url', ASCENDING)], background=True)
                    self._db[collection].create_index([('status', ASCENDING)], background=True)
                    self._db[collection].create_index([('url', ASCENDING), ('status', ASCENDING)], background=True)
                    self._db[collection].create_index([('date', ASCENDING)], background=True)
                except Exception as e:
                    pass


    def _job_create(self, queue_name, content):
        content['status'] = "new"
        content['date'] = datetime.utcnow()
        return None == self._db[queue_name].find_and_modify(
            query={ 'url': content['url'] },
            update={ '$setOnInsert': content },
            upsert=True)


    def _job_count(self, queue_name, filter={}):
        return self._db[queue_name].find(filter).count()


    def _job_read(self, queue_name, filter={}):
        return self._db[queue_name].find(filter)


    def _job_update(self, queue_name, status_old=None, status_new=None, url=None, data=None):
        query = {}
        if url != None:
            query['url'] = url
        else:
            query['url'] = { '$exists': True, '$ne': None }
        if status_old != None:
            query['status'] = status_old
        set_new = { 'status': status_new }
        if data != None:
            set_new['data'] = data
        return self._db[queue_name].find_and_modify(
            query=query,
            update={ '$set': set_new })


    def _job_delete(self, queue_name, filter={}):
        return self._db[queue_name].remove(filter).get('ok', 0) == 1



    def queue_crawl_create(self, url):
        return self._job_create(config_queue_crawl, { 'url': url })


    def queue_crawl_take(self):
        return self._job_update(config_queue_crawl, "new", "process")


    def queue_crawl_done(self, url):
        return None != self._job_update(config_queue_crawl, "process", "done", url)


    def queue_crawl_fail(self, url):
        return None != self._job_update(config_queue_crawl, "process", "fail", url)


    def queue_crawl_renew(self, url):
        return None != self._job_update(config_queue_crawl, None, "new", url)


    def queue_crawl_retry(self):
        return None != self._job_update(config_queue_crawl, "fail", "new")


    def queue_crawl_clear(self):
        return self._job_delete(config_queue_crawl)


    def queue_crawl_count(self, status=None):
        filter = {}
        if status != None:
            filter['status'] = status
        return self._job_count(config_queue_crawl, filter)



    def queue_page_create(self, url, text):
        return self._job_create(config_queue_page, { 'url': url, 'text': text })


    def queue_page_take_raw(self):
        return self._job_update(config_queue_page, "new", "process_raw")


    def queue_page_take_data(self):
        return self._job_update(config_queue_page, "data", "process_data")


    def queue_page_done_raw(self, url, data):
        return None != self._job_update(config_queue_page, "process_raw", "data", url, data)


    def queue_page_done_data(self, url):
        return None != self._job_update(config_queue_page, "process_data", "done", url)


    def queue_page_fail_raw(self, url):
        return None != self._job_update(config_queue_page, "process_raw", "fail", url)


    def queue_page_renew(self, url):
        return None != self._job_update(config_queue_page, None, "new", url)


    def queue_page_count(self, status=None):
        filter = {}
        if status != None:
            filter['status'] = status
        return self._job_count(config_queue_page, filter)


    def queue_page_clear(self):
        return self._job_delete(config_queue_page)



"""
    def snippet_create(self, snippet):
        return self._job_create(config_db_snippet, snippet)


    def snippet_clear(self):
        return self._job_delete(config_db_snippet)


    def snippet_read(self, *fields):
        filter = {}
        for field in fields:
            filter[field] = { '$exists': True }
        data_raw = self._job_read(config_db_snippet, filter)
        fields_remove = ['_id', 'date', 'status']
        data = []
        for item in data_raw:
            for field in fields_remove:
                item.pop(field, None)
            data.append(item)
        return data


    def snippet_count(self, *fields):
        filter = {}
        for field in fields:
            filter[field] = { '$exists': True }
        return self._job_count(config_db_snippet, filter)
"""

def main():
    pass


if __name__ == '__main__':
    main()
