#!/usr/bin/env python3
"""Exporter of snippets for snippet crawler"""

from BaseLogger import BaseLogger
from DatabaseAccessor import DatabaseAccessor
from contextlib import closing
from csv import DictWriter
from json import dump
from os import remove
from platform import node
from time import strftime
from zipfile import ZipFile, ZIP_DEFLATED


class Exporter(BaseLogger):
    def __init__(self, log_level=None):
        BaseLogger.__init__(self, self.__class__.__name__, log_level)
        self._db_conn = DatabaseAccessor()
        self._log_info("exporter start @%s", node())
        self._source_set_joke = [
            "http://neihanshequ.com/joke/",
            "http://neihanshequ.com/bar/1/",
            "http://neihanshequ.com/bar/11/",
            "http://neihanshequ.com/bar/76/",
            "http://neihanshequ.com/bar/80/",
            "http://neihanshequ.com/bar/82/",
            "http://neihanshequ.com/bar/59/",
            "http://neihanshequ.com/bar/5/",
        ]
        self._source_set_art = [
            "http://neihanshequ.com/bar/25/",
            "http://neihanshequ.com/bar/26/",
            "http://neihanshequ.com/bar/3/",
            "http://neihanshequ.com/bar/53/",
            "http://neihanshequ.com/bar/46/",
            "http://neihanshequ.com/bar/49/",
            "http://neihanshequ.com/bar/69/",
            "http://neihanshequ.com/bar/51/",
            "http://neihanshequ.com/bar/60/",
        ]


    def process(self):
        filelist = []
        data = self._db_conn.snippet_read()
        self._log_info("load all snippet data from database")

        filelist.append(self._save_as_json(data))
        filelist.append(self._save_as_csv(data))

        data_joke = self._select_data_column(data, self._source_set_joke)
        filelist.append(self._save_as_csv(data_joke, "snippet_joke.csv"))

        data_art = self._select_data_column(data, self._source_set_art)
        filelist.append(self._save_as_csv(data_art, "snippet_art.csv"))

        self._archive_into_zipfile(filelist)


    def _select_data_column(self, data_raw, source_set):
        data_new = []
        for item_raw in data_raw:
            if item_raw["source"] not in source_set:
                continue
            for index in range(max(1, len(item_raw.get("comments", [])))):
                item_new = {
                    "count_digg": item_raw["count"]["digg"],
                    "count_bury": item_raw["count"]["bury"],
                    "count_favorite": item_raw["count"]["favorite"],
                    "count_comment": item_raw["count"]["comment"],
                    "count_diggcomm": None,
                    "text": item_raw["content"],
                    "text_comment": None,
                    "source": item_raw["source_name"],
                }
                if "comments" in item_raw:
                    item_new["text_comment"] = item_raw["comments"][index]
                    item_new["count_diggcomm"] = item_raw["count"]["commdigg"][index]
                data_new.append(item_new)
        return data_new


    def _save_as_json(self, data, filename="snippet.json"):
        with open(filename, 'w') as jsonfile:
            for item in data:
                dump(item, jsonfile, sort_keys=True)
                jsonfile.write("\n")
        self._log_info("save %d items as json file: %s", len(data), filename)
        return filename


    def _save_as_csv(self, data, filename="snippet.csv"):
        fields = set()
        for item in data:
            fields = fields.union(set(item.keys()))
        with open(filename, 'w', encoding='utf8', newline='') as csvfile:
            writer = DictWriter(csvfile, extrasaction='ignore', dialect='excel', fieldnames=sorted(fields, reverse=False))
            writer.writeheader()
            for item in data:
                writer.writerow(item)
        self._log_info("save %d items as csv file: %s", len(data), filename)
        return filename


    def _archive_into_zipfile(self, filelist):
        zipname = "snippet_{}.zip".format(strftime("%Y-%m-%d_%H-%M-%S"))
        with ZipFile(zipname, 'w', ZIP_DEFLATED) as zip:
            for filename in filelist:
                zip.write(filename)
                remove(filename)
        self._log_info("archive exported files into %s", zipname)


    def close(self):
        self._db_conn.close()
        self._log_info("exporter exit")
        self._close_logger()


def main():
    with closing(Exporter()) as exporter:
        exporter.process()


if __name__ == '__main__':
    main()
