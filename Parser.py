#!/usr/bin/env python3
"""JSON data parser for snippet crawler"""

from BaseLogger import BaseLogger
from DatabaseAccessor import DatabaseAccessor
from bs4 import BeautifulSoup
from config import config_queue_page, config_idle_sleep, config_parse_domain, config_parse_process
from contextlib import closing
from multiprocessing import Process
from platform import node
from time import sleep
from datetime import datetime


class Parser(BaseLogger):
    def __init__(self, log_level=None):
        BaseLogger.__init__(self, self.__class__.__name__, log_level)
        self._db_conn = DatabaseAccessor()
        self._log_info("parser start @%s", node())


    def close(self):
        self._db_conn.close()
        self._log_info("parser exit")
        self._close_logger()


    def process(self):
        result_count = None
        job = self._db_conn.queue_page_take_data()
        if job != None:
            url = job['url']
            data_list = job.get('data', [])
            self._log_info("parse json data from %s, items count %d", url, len(data_list))
            result_count = 0
            for data_index, data_item in enumerate(data_list):
                snippet = self._extract_snippet_record(data_item)
                if snippet == None:
                    self._log_warning("fail to extract #%d record of '%s' json data in queue_page", data_index, url)
                else:
                    if not self._db_conn.snippet_create(snippet):
                        self._log_warning("fail to add new snippet %s", snippet["url"])
                    else:
                        result_count += 1
            self._log_info("extract %d valid snippets from %s json data", result_count, url)
            if not self._db_conn.queue_page_done_data(url):
                self._log_warning("fail to mark %s as 'done' in queue_crawl", url)
        else:
            self._log_warning("grab no json data to parse")
            sleep(config_idle_sleep)
        return result_count


    def _extract_snippet_record(self, data):
        try:
            snippet = {
                "url": config_parse_domain + str(data["group"]["group_id"]),
                "date": datetime.fromtimestamp(data["group"]["create_time"]),
                "content": data["group"]["content"],
            }
            if len(data["comments"]) > 0:
                snippet["comment"] = data["comments"][0]["text"]
        except Exception as e:
            snippet = None
        return snippet;


def main(times=10):
    with closing(Parser()) as parser:
        if times:
            for _ in range(times):
                parser.process()
        else:
            while True:
                parser.process()


if __name__ == '__main__':
    for _ in range(config_parse_process):
        Process(target=main, args=(0,)).start()
