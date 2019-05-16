from multiprocessing import Process
import os
import time
import logging
import threading
from faker import Faker
import csv

from datetime import datetime


dir_path = os.path.dirname(os.path.realpath(__file__))

# set up logging to file - see previous section for more details
log_file_name = datetime.now().strftime('multi_threading_processing_%d_%m_%Y_%H_%M.log')
logging.basicConfig(level=logging.DEBUG,
                    format='%(relativeCreated)6d %(threadName)s %(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=os.path.join(dir_path, "logs", log_file_name),
                    filemode='a')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(relativeCreated)6d %(threadName)s %(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)


def generate_csv(input_data):
    """
    Generate csv reports form list of dict
    :param input_data:
    :return: None
    """

    report_name = os.path.join(dir_path, "reports", datetime.now().strftime('report_%d_%m_%Y_%H_%M.csv'))

    with open(report_name, 'wb') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=["node", "name", "address", "log"])
        dict_writer.writeheader()
        for data in input_data:
            dict_writer.writerow(data)

    logging.info("Report is generated at {}".format(report_name))
    print "Report is generated at {}".format(report_name)


def find_in_log_file(search_text, log_file):
    """
    Searches text in log file
    :param search_text:
    :param log_file:
    :return: Boolean
    """
    try:
        logging.info("Reading log file")
        with open(log_file) as _file:
            contents = _file.read()
            if search_text in contents:
                return True
            else:
                return False
    except Exception as e:
        print e
        logging.error("Error in reading log file".format(e))
        raise
    finally:
        pass


def logs_scanner(node):
    """

    :param node:
    :return:
    """
    report_list = []
    try:
        logging.info("OS process id: {}".format(os.getpid()))
        log_file_path = os.path.join(dir_path, "mylog.log")
        fk = Faker("en_US")
        result = {
            "name": fk.name(),
            "node": node,
            "address": fk.address(),
            # "log": "log"
            "log": "Found" if find_in_log_file("network SCRIPTENTRY", log_file_path) else "Not Found"
        }
        report_list.append(result)
        generate_csv(report_list)
    except Exception as e:
        logging.error("Exception {}".format(e))
        raise


def thread_handler():
    """
    Thread Handler
    :return:
    """

    logging.info("Multi Threading section started")
    start_time = int(time.time())
    node_details = ["172.10.152." + str(x) for x in range(10, 100)]
    local_threads = []

    for node_detail in node_details:
        _thread = threading.Thread(
            target=logs_scanner,
            args=(node_detail,)
        )
        local_threads.append(_thread)

    for _thread in local_threads:
        _thread.start()

    for _thread in local_threads:
        _thread.join()

    # generate_csv(report_list)
    end_time = int(time.time())
    total_time = end_time - start_time
    logging.info("Threading Total Time Taken {}".format(total_time))


def multi_processing_handler():
    """

    :return:
    """
    logging.info("Multi Processing section started")
    start_time = int(time.time())
    node_details = ["172.10.152." + str(x) for x in range(10, 100)]
    local_threads = []

    for node_detail in node_details:
        _thread = Process(
            target=logs_scanner,
            args=(node_detail,)
        )
        local_threads.append(_thread)

    for _thread in local_threads:
        _thread.start()

    for _thread in local_threads:
        _thread.join()

    # generate_csv(report_list)
    end_time = int(time.time())
    total_time = end_time - start_time
    logging.info("Multi Processing Total Time Taken {}".format(total_time))


if __name__ == "__main__":

    thread_handler()
    multi_processing_handler()
