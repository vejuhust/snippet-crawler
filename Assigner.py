#!/usr/bin/env python3
"""Parsing raw pages into JSON data for snippet crawler"""

from BaseLogger import BaseLogger
from DatabaseAccessor import DatabaseAccessor
from config import config_assign_domain, config_assgin_process, config_idle_sleep
from contextlib import closing
from json import loads
from multiprocessing import Process
from platform import node
from time import sleep


class Assigner(BaseLogger):
    def __init__(self, log_level=None):
        BaseLogger.__init__(self, self.__class__.__name__, log_level)
        self._db_conn = DatabaseAccessor()
        self._log_info("assigner start @%s", node())


    def close(self):
        self._db_conn.close()
        self._log_info("assigner exit")
        self._close_logger()


    def process(self):
        url = None
        job = self._db_conn.queue_page_take_raw()
        if job != None:
            url = job['url']
            text = job.get('text', "")
            parse_result = self._parse_raw_page(url, text)
            if parse_result == None:
                self._log_warning("fail to parse '%s' as JSON in queue_page", url)
                if not self._db_conn.queue_page_fail_raw(url):
                    self._log_warning("fail to mark %s as 'fail' in queue_page", url)
            else:
                if parse_result[0] == None:
                    self._log_warning("'%s' in queue_page indicates no more new content", url)
                else:
                    self._log_info("%s indicates new crawling job: %s", url, parse_result[0])
                    if not self._db_conn.queue_crawl_create(parse_result[0]):
                        self._log_warning("fail to add %s as 'new' job in queue_crawl", parse_result[0])
                if parse_result[1] == None:
                    self._log_warning("'%s' in queue_page contains on content", url)
                else:
                    self._log_info("%s contains %d raw snippets", url, len(parse_result[1]))
                    if not self._db_conn.queue_page_done_raw(url, parse_result[1]):
                        self._log_warning("fail to append parsed data for %s in queue_crawl", url)
        else:
            self._log_warning("grab no jobs to assign")
            sleep(config_idle_sleep)
        return url


    def _parse_raw_page(self, url, text):
        try:
            page_content = loads(text)
            url_new, data_new = None, None
            if page_content["data"]["has_more"]:
                url_new = config_assign_domain + str(page_content["data"]["max_time"])
            if len(page_content["data"]["data"]) > 0:
                data_new = page_content["data"]["data"]
            result = (url_new, data_new)
            self._log_info(
                "%s data status - more: %s, min: %d, max: %d",
                url,
                page_content["data"]["has_more"],
                page_content["data"]["min_time"],
                page_content["data"]["max_time"])
        except Exception as e:
            result = None
        return result


def main(times=10):
    with closing(Assigner()) as assigner:
        if times:
            for _ in range(times):
                assigner.process()
        else:
            while True:
                assigner.process()


if __name__ == '__main__':
    for _ in range(config_parse_process):
        Process(target=main, args=(0,)).start()
