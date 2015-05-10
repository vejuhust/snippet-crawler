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

config_crawl_process    = 4
config_crawl_retry      = 3
config_crawl_sleep      = 1
config_crawl_timeout    = 5

config_idle_sleep       = 1

config_assign_domain     = "http://neihanshequ.com/joke/?is_json=1&max_time="
config_assgin_process    = max(4, cpu_count())
