# -*- coding: utf-8 -*-
from pyquery import PyQuery as pq
from datetime import datetime
import requests
import csv

# 調べたい声優名一覧
ACTRESSES = [
    "竹達彩奈",
    "種田梨沙",
]

# 検索URL
URL_SEARCH = lambda k, c: "http://www.logsoku.com/search?q={}&sort=create&sr={}".format(k, c)

# フィルタ（これ以上を対象とする）
FILTER_IKIOI = 1
FILTER_RES_COUNT = 10


def get_threads(html):
    threads = []
    d = pq(html)
    for elem in d("#search_result_threads table tbody tr"):
        row = pq(elem)
        bbs = row("td.bbs").text()
        res_count = int(row("td.length").text())
        title = row("td.title").text().replace("[転載禁止]©2ch.net", "")
        date = datetime.strptime(row("td.date").text(), "%Y-%m-%d %H:%M")
        ikioi = int(row("td.ikioi").text())
        threads.append({
            "bbs": bbs,
            "res_count": res_count,
            "title": title,
            "date": date,
            "ikioi": ikioi
        })
    return threads


def get_keyword_threads(keyword):
    html = requests.get(URL_SEARCH(keyword, FILTER_RES_COUNT)).text
    return [t for t in get_threads(html) if t["ikioi"] >= FILTER_IKIOI and t["res_count"] >= FILTER_RES_COUNT]

if __name__ == "__main__":
    with open("count.csv", "w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        for keyword in ACTRESSES:
            writer.writerows([[keyword] + list(t.values()) for t in get_keyword_threads(keyword)])

