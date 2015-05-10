#!/usr/bin/env python3
"""Usability verification tool for snippet crawler"""

from Assigner import Assigner
from Crawler import Crawler
from DatabaseAccessor import DatabaseAccessor
from Parser import Parser
from config import *
from contextlib import closing
from pprint import pprint
from time import sleep


urls = [
    "http://neihanshequ.com/joke/?is_json=1&max_time=",       # 首页

    "http://neihanshequ.com/bar/1/?is_json=1&max_time=",      # 内涵段子
    "http://neihanshequ.com/bar/11/?is_json=1&max_time=",     # 精辟语录
    "http://neihanshequ.com/bar/76/?is_json=1&max_time=",     # 友问友答
    "http://neihanshequ.com/bar/80/?is_json=1&max_time=",     # 来自世界的恶意
    "http://neihanshequ.com/bar/82/?is_json=1&max_time=",     # 机智如我
    "http://neihanshequ.com/bar/59/?is_json=1&max_time=",     # 突然觉得哪里不对
    "http://neihanshequ.com/bar/5/?is_json=1&max_time=",      # 我的xx是极品

    "http://neihanshequ.com/bar/25/?is_json=1&max_time=",     # 治愈系英文
    "http://neihanshequ.com/bar/26/?is_json=1&max_time=",     # 精选书摘
    "http://neihanshequ.com/bar/3/?is_json=1&max_time=",      # 早晚必读的话
    "http://neihanshequ.com/bar/53/?is_json=1&max_time=",     # 旅行家
    "http://neihanshequ.com/bar/46/?is_json=1&max_time=",     # 佛家禅语
    "http://neihanshequ.com/bar/49/?is_json=1&max_time=",     # 悸动歌词
    "http://neihanshequ.com/bar/69/?is_json=1&max_time=",     # 图写心情
    "http://neihanshequ.com/bar/51/?is_json=1&max_time=",     # 情感点滴
    "http://neihanshequ.com/bar/60/?is_json=1&max_time=",     # 耽美宅腐
]


class Launcher():
    def __init__(self):
        pass


    def close(self):
        pass


    def process(self, urls):
        # self.clear_queue_crawl_page_snippet()
        self.add_urls_to_queue_crawl(urls)
        times_idle = 1
        self.run_crawler(len(urls) + times_idle)
        self.run_assigner(len(urls) + times_idle)
        self.run_parser(len(urls) + times_idle)
        # self.read_all_profile()


    def add_urls_to_queue_crawl(self, urls):
        print("add_urls_to_queue_crawl with config_crawl_date_max =", config_crawl_date_max)
        with closing(DatabaseAccessor()) as dal:
            for url_prefix in urls:
                url = url_prefix + str(config_crawl_date_max)
                print("add {} - {}".format(url, dal.queue_crawl_create(url)))


    def clear_queue_crawl_page_snippet(self):
        print("clear_queue_crawl_page_snippet")
        with closing(DatabaseAccessor()) as dal:
            print("clear crawl - {}".format(dal.queue_crawl_clear()))
            print("clear page - {}".format(dal.queue_page_clear()))
            print("clear snippet - {}".format(dal.snippet_clear()))


    def run_crawler(self, times=5):
        with closing(Crawler()) as crawler:
            for _ in range(times):
                crawler.process()
                sleep(config_crawl_sleep)


    def run_assigner(self, times=5):
        with closing(Assigner()) as assigner:
            for _ in range(times):
                assigner.process()


    def run_parser(self, times=5):
        with closing(Parser()) as parser:
            for _ in range(times):
                parser.process()


"""
    def read_all_profile(self):
        with closing(DatabaseAccessor()) as dal:
            pprint(dal.profile_read())
"""

def main():
    with closing(Launcher()) as launcher:
        launcher.process(urls)


if __name__ == '__main__':
    main()
