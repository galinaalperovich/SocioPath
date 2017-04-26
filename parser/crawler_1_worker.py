# -*- coding: utf-8 -*-
import csv
from multiprocessing import Process, Queue

from selenium import webdriver

from parser.parser_utils import get_microformat_properties_by_type, get_event_features_and_write
from settings import path_to_phantomjs

CURRENT_URL = ''
TIME_OUT_LOAD = 20
TIME_OUT_FEATURE = 60

input = open('/Users/jetbrains/PycharmProjects/SocioPath/data/all_urls.csv', 'r')
output = open('/Users/jetbrains/PycharmProjects/SocioPath/data/data2.csv', 'a')
processed_urls = open('/Users/jetbrains/PycharmProjects/SocioPath/data/processed_urls.csv', 'a')

output_writer = csv.writer(output)
first_line = True

driver = webdriver.PhantomJS(executable_path=path_to_phantomjs)
i = 0


def start_with_timeout(process, timeout, msg):
    process.start()
    process.join(timeout)
    if process.is_alive():
        print("Timed out on {}".format(msg))
        process.terminate()
        process.join()


for line in input:
    if i < 1114:
        i += 1
        continue
    splited = line.split('\t')
    prop_type = splited[0]
    url = splited[1]
    CURRENT_URL = url
    print("Crawler works for: " + CURRENT_URL.strip())

    queue = Queue()
    p = Process(target=get_microformat_properties_by_type, args=(url, prop_type, queue))
    start_with_timeout(p, TIME_OUT_LOAD, "loading")

    event_properties = queue.get() if not queue.empty() else None
    if event_properties is not None:
        queue2 = Queue()
        p_write = Process(target=get_event_features_and_write, args=(event_properties, driver, output_writer, i))

        start_with_timeout(p_write, TIME_OUT_FEATURE, "feature extraction and writing")

    i += 1
    print(i)
    print("\n\n ")
    # if i == 100:
    #     break