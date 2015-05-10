#!/usr/bin/env python3
"""Configurations for snippet crawler"""

from multiprocessing import cpu_count
from time import strftime


config_db_addr  = "127.0.0.1"
config_db_port  = 27017
config_db_name  = "snippetcrawl"
config_db_user  = "YOUR_USERNAME"
config_db_pass  = "YOUR_PASSWORD"

config_db_snippet   = "snippet"
config_queue_crawl  = "queue_crawl"
config_queue_page   = "queue_page"

config_log_file     =  "sc_{}.log".format(strftime("%Y-%m-%d"))

config_crawl_process    = min(1, cpu_count())
config_crawl_retry      = 3
config_crawl_sleep      = 2
config_crawl_timeout    = 5
config_crawl_date_min   = 5
config_crawl_date_max   = 1431285365

config_idle_sleep       = 1

config_assign_process   = min(1, cpu_count())

config_parse_domain     = "http://neihanshequ.com/p"
config_parse_process    = min(1, cpu_count())
