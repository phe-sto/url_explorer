#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# For argument like CSV an regex
import argparse
# To produce a CSV if desired
import csv
import urllib.request
from http.client import InvalidURL, RemoteDisconnected
from threading import Thread, active_count
from time import sleep, perf_counter
from urllib.error import URLError

import exrex
import pip

pip.main(['install', 'exrex', '--quiet'])
MESSAGE = """\nWARNING #1 dot '.' is a regular expression symbol. Don't forgot to escape it if it is not
    \nmeant to be a regular expression. For instance to search for google.com sudomain https://www\...\.google\.com .
    \nFirst and third dot are escaped but not the second.
    \nWARNING #2 Depend on exrex python package to generate all the URL(s) based on a regex. Therefore a pip install is
    \nperformance at the beginning of the script. This pip command might force you to sudo or log as administrator,
    \nroot, etc. Enter a regex pattern URL to check for exstance: """

MAX_THREAD = 1000


class UrlCheckerException(Exception):
    """Specific exception raised by the UrlChecker class"""
    pass


class UrlChecker(Thread):
    """Class UrlChecker that check for existance of url"""
    url_exist = []

    def __init__(self, url_to_check):
        """
        Contructor of the UrlChecker class
        """
        # Initialize threading
        Thread.__init__(self)

        if isinstance(url, str) is False:
            raise TypeError("First argument url_regex must  be a string type")
        self.url = url_to_check

    def __repr__(self):
        """Representation of the UrlChecker class instance"""
        return "UrlChecker for pattern {0}".format(self.url)

    def __del__(self):
        """Initialize the Thread"""
        if self.is_alive() is True:
            raise UrlCheckerException(
                'Thread still alive, wait for it to finish wish join() method')

    def run(self):
        """Starting the internal methods of a Thread to check if url exist"""
        try:
            urllib.request.urlopen(self.url, timeout=5)
            UrlChecker.url_exist.append(self.url)
        except URLError:
            pass
        except ValueError:
            pass
        except InvalidURL:
            pass
        except RemoteDisconnected:
            pass


if __name__ == '__main__':
    # Main procedure
    parser = argparse.ArgumentParser(
        description="Regular expression to search for URL(s) and optionnal ouput CSV file")
    parser.add_argument('-of', '--output_file', type=str, help='Write an output CSV file with results',
                        required=False)
    parser.add_argument('-re', '--regular_expression', type=str, help='Regex pattern to search for URL(s)',
                        required=False)
    # input arguments
    args = parser.parse_args()
    output_file = args.output_file
    url_pattern = args.regular_expression
    if url_pattern is None:
        # Input message explaining the script and input
        url_pattern = input(MESSAGE)
    # Generate a list of possible URL, unduplicated with set()
    url_list = list(set(exrex.generate(url_pattern)))
    # Start counter
    t0 = perf_counter()
    # Initialize all threads
    for url in url_list:
        globals()['thread_{0}'.format(url)] = UrlChecker(url)
    # Start all threads with sleep in case of max thread reached
    for url in url_list:
        while True:
            # Max reached
            if active_count() == MAX_THREAD:
                # Wait for some threads to end
                sleep(0.1)
            else:
                globals()['thread_{0}'.format(url)].start()
                break
    for url in url_list:
        globals()['thread_{0}'.format(url)].join()
    # End time
    t1 = perf_counter()
    if output_file is not None:
        with open(output_file, 'w', newline='') as csvfile:
            result_writer = csv.writer(csvfile, delimiter=' ')
            for url in UrlChecker.url_exist:
                result_writer.writerow([url])
    else:
        print("""\nNumber of URL(s) tested is {0} in {1:.2f} seconds.
        \nNumber of valid URL(s) found is {2} :
        \n{3}""".format(len(url_list), float(t1 - t0), len(UrlChecker.url_exist), UrlChecker.url_exist))
