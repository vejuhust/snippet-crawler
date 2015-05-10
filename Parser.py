#!/usr/bin/env python3
"""JSON data parser for snippet crawler"""

from BaseLogger import BaseLogger
from DatabaseAccessor import DatabaseAccessor
from bs4 import BeautifulSoup
from config import config_queue_page, config_idle_sleep, config_parse_domain, config_parse_process
from contextlib import closing
from datetime import datetime
from multiprocessing import Process
from platform import node
from time import sleep


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
        count_valid = None
        count_duplicate = None
        job = self._db_conn.queue_page_take_data()
        if job != None:
            url = job['url']
            data_list = job.get('data', [])
            self._log_info("parse json data from %s, items count %d", url, len(data_list))
            count_valid = 0
            count_duplicate = 0
            for data_index, data_item in enumerate(data_list):
                snippet = self._extract_snippet_record(url, data_item)
                if snippet == None:
                    self._log_warning("fail to extract #%d record of '%s' json data in queue_page", data_index, url)
                else:
                    if not self._db_conn.snippet_create(snippet):
                        count_duplicate += 1
                        # self._log_warning("fail to add new snippet %s", snippet["url"])
                    else:
                        count_valid += 1
            self._log_info("extract %d valid & %d duplicate snippets from %s json data", count_valid, count_duplicate, url)
            if not self._db_conn.queue_page_done_data(url):
                self._log_warning("fail to mark %s as 'done' in queue_crawl", url)
        else:
            self._log_warning("grab no json data to parse")
            sleep(config_idle_sleep)
        return (count_valid, count_duplicate)


    def _extract_snippet_record(self, url, data):
        try:
            snippet = {
                "url": config_parse_domain + str(data["group"]["group_id"]),
                "date": datetime.fromtimestamp(data["group"]["create_time"]),
                "content": data["group"]["content"],
                "archive": data,
                "source": url.split("?")[0],
                "source_name": data["group"]["category_name"],
            }
            snippet["count"] = {
                "digg": data["group"]["digg_count"],
                "bury": data["group"]["bury_count"],
                "favorite": data["group"]["favorite_count"],
                "comment": data["group"]["comment_count"],
            }
            if len(data["comments"]) > 0:
                comment_text = []
                comment_digg = []
                for comment in data["comments"]:
                    comment_text.append(comment["text"])
                    comment_digg.append(comment["digg_count"])
                snippet["comments"] = comment_text
                snippet["count"]["commdigg"] = comment_digg
            if len(snippet["content"].strip()) == 0:
                snippet = None
        except Exception as e:
            snippet = None
        return snippet


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
