# -*- coding: utf-8 -*-

# For argument like CSV an regex
import argparse
# To produce a CSV if desired
import csv
import socket
import urllib.request
from http.client import InvalidURL, RemoteDisconnected
from threading import Thread, active_count
from time import sleep, perf_counter
from urllib.error import URLError

try:
    import exrex
except ModuleNotFoundError:
    import pip
    pip.main(['install', 'exrex', '--quiet'])
    import exrex

MESSAGE = """
   ___             _____  _____ 
  / _ \__ _ _ __   \_   \/__   \\
 / /_)/ _` | '_ \   / /\/  / /\/      INFOGESTION & CONSEIL IT
/ ___/ (_| | |_) /\/ /_   / /   
\/    \__,_| .__/\____/   \/          christophe.brun@papit.fr 
           |_|                  

WARNING #1 Dot '.' is a regular expression symbol. Don't forgot to escape it if it is not
meant to be a regular expression. For instance to search for google.com subdomain https://www\...\.google\.com .
First and third dot are escaped but not the second.
WARNING #2 Depend on exrex python package to generate all the URL(s) based on a regex. Therefore a pip install is
performance at the beginning of the script. This pip command might force you to sudo or log as administrator,
root, etc. Enter a regex pattern URL to check for existence: """

DEFAULT_MAX_THREAD = 1000

# ======================================================================================================================
# Threading explorer object
# ======================================================================================================================


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

        if isinstance(url_to_check, str) is False:
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
        except socket.timeout:
            pass
        except ConnectionResetError:
            pass
        except URLError:
            pass
        except ValueError:
            pass
        except InvalidURL:
            pass
        except RemoteDisconnected:
            pass


# ======================================================================================================================
# Main procedure
# ======================================================================================================================
def main():
    # Argument definition
    parser = argparse.ArgumentParser(
        description="Regular expression to search for URL(s), optionnal ouput CSV file and max thread number")
    parser.add_argument('-re', '--regular_expression', type=str, help='Regex pattern to search for URL(s)',
                        required=False)
    parser.add_argument('-mt', '--max_thread', type=int, help='Maximum number of thread at a time',
                        required=False)
    parser.add_argument('-of', '--output_file', type=str, help='Output CSV file name',
                        required=False)
    # input arguments
    args = parser.parse_args()
    output_file = args.output_file
    url_pattern = args.regular_expression
    max_thread = args.max_thread
    # Input text if no argument
    if url_pattern is None:
        # Input message explaining the script and input
        url_pattern = input(MESSAGE)
    # Generate a list of possible URL, unduplicated with set()
    url_list = list(set(exrex.generate(url_pattern, limit=10000000)))
    # Start counter
    t0 = perf_counter()
    # Initialize all threads
    thread_list = []
    for url in url_list:
        thread_list.append(UrlChecker(url))
    # if no argument for maximum thread, default is 1000
    if max_thread is None:
        max_thread = DEFAULT_MAX_THREAD
    # Start all threads with sleep in case of max thread reached
    for t in thread_list:
        while True:
            # Max reached
            if active_count() == max_thread:
                # Wait for some threads to end
                sleep(0.1)
            else:
                t.start()
                break
    for t in thread_list:
        t.join()
    # End time
    t1 = perf_counter()
    # In case of output file argument write result to a CSV
    if output_file is not None and len(UrlChecker.url_exist) > 0:
        with open(output_file, 'w', newline='') as csvfile:
            result_writer = csv.writer(csvfile, delimiter=' ')
            for url in UrlChecker.url_exist:
                result_writer.writerow([url])
    # If no output file argument, a report is printed
    elif output_file is None:
        print("""\nNumber of URL(s) tested is {0} in {1:.2f} seconds.
        \nNumber of valid URL(s) found is {2} :
        \n{3}""".format(len(url_list), float(t1 - t0), len(UrlChecker.url_exist), UrlChecker.url_exist))


# ======================================================================================================================
# Command line started
# ======================================================================================================================
if __name__ == '__main__':
    main()
