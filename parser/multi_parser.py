import csv
import multiprocessing as mp
import os
import sys
from multiprocessing import Queue
from multiprocessing.context import Process

from selenium import webdriver

from parser.parser_utils import get_microformat_properties_by_type, get_event_features_and_write, now
# from parser_utils import get_microformat_properties_by_type, get_event_features_and_write, now

fn = 'temp.txt'

CWD = os.getcwd()

# PATH_FILES = '/Users/jetbrains/Yandex.Disk.localized/Diploma/data_output'
PATH_FILES = CWD + '/data_output'
path_to_phantomjs = CWD +'/phantomjs'
PATH_PARSED_FILES = '/Users/jetbrains/Yandex.Disk.localized/Diploma/data_parsed' #LOCAL
# PATH_PARSED_FILES = CWD + '/data_parsed' #METACENTRUM

FILES_LIST = list(filter(lambda x: 'csv' in x, os.listdir(PATH_FILES)))
TIME_OUT_LOAD = 20
TIME_OUT_FEATURE = 60


def start_with_timeout(process, timeout, msg, url, i):
    process.start()
    process.join(timeout)
    if process.is_alive():
        print("{}   {}  Process={}  {}  {}".format(now(), i, "Timed out on: ", msg, url))
        sys.stdout.flush()
        process.terminate()
        # process.join()


def process_file(file_path_input, file_path_output, i):
    if os.path.exists(file_path_output):
        return print('{}    {}  Already done'.format(now(), file_path_output))

    input_file = open(file_path_input, 'r')
    output_file = open(file_path_output, 'a')

    # every worker create separate file for a input file
    writer = csv.writer(output_file, delimiter='\t')

    # for every file we create seperate driver (100 URLs)
    driver = webdriver.PhantomJS(executable_path=path_to_phantomjs)

    for line in input_file:
        splited = line.split('\t')
        property_type = splited[0]
        url = splited[1]
        print('{}   Process={}  Current url: {}'.format(now(), i, url))

        # start process for getting microformat properties
        temp_queue = Queue()
        p = Process(target=get_microformat_properties_by_type, args=(url, property_type, temp_queue, i))
        start_with_timeout(p, TIME_OUT_LOAD, "loading", url, i)

        event_properties = temp_queue.get() if not temp_queue.empty() else None
        if p.is_alive():
            p.terminate()
        if event_properties is not None:
            print("{}   Process={}  Got properties for  {}".format(now(), i, url))

            # start process for feature extraction and writing to separate file
            p_event_features = Process(target=get_event_features_and_write,
                                       args=(event_properties, driver, writer, i, output_file))
            start_with_timeout(p_event_features, TIME_OUT_FEATURE, "feature extraction", url, i)
            if p_event_features.is_alive():
                p.terminate()

    return 'done'


def get_filepath(file_id, input=True):
    if input:
        return PATH_FILES + '/' + FILES_LIST[file_id]
    else:
        return PATH_PARSED_FILES + '/' + FILES_LIST[file_id].replace('output', 'parsed')


def worker(file_ids, i):
    for file_id in file_ids:
        file_path_input = get_filepath(file_id)
        file_path_output = get_filepath(file_id, input=False)
        try:
            print('{}   Process={}  Started to process file {}'.format(now(), i, file_path_input))
            process_file(file_path_input, file_path_output, i)
        except Exception as e:
            print('{}   Process={}  Bad file!    {}'.format(now(), i, e))
            continue


def get_files_for_worker(i, num_workers):
    num_files = len(FILES_LIST)
    all_files_idx = list(range(num_files))
    return chunkify(all_files_idx, num_workers)[i]


def chunkify(lst, n):
    return [lst[i::n] for i in range(n)]


def main():
    sys.stdout = open('log_print.txt', 'a')
    #num_workers = int(mp.cpu_count()/3
    num_workers = 1
    for i in range(num_workers):
        file_ids = get_files_for_worker(i, num_workers)
        process = Process(target=worker,
                          args=(file_ids, i))
        process.start()


if __name__ == "__main__":
    main()
