#!/usr/bin/env python3

#
# DirDigger
# ---------
# Coded by: Riccardo Mollo (riccardomollo84@gmail.com)
#

import argparse
import getopt
import os
import re
import requests
import signal
import socket
import subprocess
import sys
import time
import urllib3
import validators
from fake_useragent import UserAgent
from termcolor import colored

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
requests.packages.urllib3.contrib.pyopenssl.extract_from_urllib3()
urllib3.disable_warnings()

def logo():
    print(colored('   ___  _     ___  _                  ', 'cyan'))
    print(colored('  / _ \(_)___/ _ \(_)__ ____ ____ ____', 'cyan'))
    print(colored(' / // / / __/ // / / _ `/ _ `/ -_) __/', 'cyan'))
    print(colored('/____/_/_/ /____/_/\_, /\_, /\__/_/   ', 'cyan'))
    print(colored('                  /___//___/          ', 'cyan'))
    print(colored('              Coded by: Riccardo Mollo', 'cyan'))
    print()

def usage():
    print('Usage: dirdigger.py [-h] | -u <url> -w <wordlist_file> [-i <status_codes>] [-t <timeout>]');
    print()

def help():
    usage()
    print('Options:')
    print(' -h                  Show this help message and exit')
    print(' -u <url>, --url=<url>')
    print('                     The base URL to start the scan from')
    print(' -w <wordlist_file>, --wordlist=<wordlist_file>')
    print('                     The file containing the wordlist')
    print(' -i <status_codes>, --ignore=<status_codes>')
    print('                     HTTP statuses to be ignored (eg: 404,302)')
    print(' -t <timeout>, --timeout=<timeout>')
    print('                     Request timeout in seconds (default: 5)')
    print()

def test(url, ua, timeout):
    try:
        r = requests.head(url, headers={'User-Agent': ua}, verify=False, timeout=(timeout, timeout))
        ret = r.status_code
    except requests.ReadTimeout:
        ret = 408
    except requests.exceptions.RequestException:
        ret = 0

    return ret

def show(status, url, ignored_statuses):
    if (ignored_statuses is not None) and (str(status) in ignored_statuses):
        pass
    else:
        str_status = str(status)

        if (status == 0):
            status = colored('ERR', 'red', attrs=['reverse', 'bold'])
        elif (status == 200):
            status = colored(str_status, 'green')
        elif ((status == 301) or (status == 302)):
            status = colored(str_status, 'yellow')
        elif ((status == 400) or (status == 401) or (status == 403) or (status == 404) or (status == 405)):
            status = colored(str_status, 'red')
        elif (status == 408):
            status = colored(str_status, 'magenta')
        elif ((status == 500) or (status == 501) or (status == 502) or (status == 503) or (status == 504) or (status == 550)):
            status = colored(str_status, 'red')
        else:
            status = str_status

        print('[+] ' + status + ' - ' + url)

def line_count(file):
    return int(subprocess.check_output('wc -l {}'.format(file), shell=True).split()[0])

def signal_handler(s, frame):
    if (s == 2):
        print('You pressed Ctrl+C!')
        print('Goodbye!')
        sys.exit()

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help = 'The base URL to start the scan from', required = True)
    parser.add_argument('-w', '--wordlist', help = 'The file containing the wordlist', required = True)
    parser.add_argument('-i', '--ignore-statuses', help = 'HTTP statuses to be ignored (eg: 404,302)', required = False, default = None)
    parser.add_argument('-t', '--timeout', help = 'Request timeout in seconds (default: 5)', type = int, required = False, default = 5)
    args = parser.parse_args()

    base_url = args.url

    if not validators.url(base_url):
        print(colored('ERROR!', 'red', attrs=['reverse', 'bold']) + ' Invalid URL: ' + colored(base_url, 'red'))
        print()
        sys.exit(1)

    wordlist_file = args.wordlist

    if not os.path.isfile(wordlist_file):
        print(colored('ERROR!', 'red', attrs=['reverse', 'bold']) + ' Wordlist file not found or not readable: ' + colored(wordlist_file, 'red'))
        print()
        sys.exit(1)

    ignored_statuses = args.ignore_statuses

    if ignored_statuses is not None:
        ignored_statuses = ignored_statuses.split(',')

    timeout = int(args.timeout)

    if (base_url[-1] != '/'):
        base_url += '/'

    start = time.time()

    logo()

    ua = UserAgent(cache=False, fallback='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36').random
    hostname = base_url.split("://")[1].split("/")[0]

    try:
        hostip =  socket.gethostbyname(hostname)
    except socket.gaierror:
        hostip = ''

    print('[+] Base URL:            ' + colored(base_url, 'white', attrs=['bold']))
    print('[+] Hostname:            ' + hostname)
    print('[+] Host IP:             ' + hostip)
    print('[+] Wordlist:            ' + wordlist_file)
    print('[+] Words count:         ' + str(line_count(wordlist_file)))
    print('[+] Random user agent:   ' + ua)
    if ignored_statuses is not None:
        print('[+] Ignored HTTP codes:  ' + ', '.join(map(str, ignored_statuses)))
#    print('[+] Mode: DIRECTORY (adding trailing \'/\' when needed)')
    print('[+] Timeout:             ' + str(timeout) + ' seconds')
    print('[+]')

    t = test(base_url, ua, timeout)
    show(t, base_url, ignored_statuses)

    if (t != 0):
        with open(wordlist_file, 'r') as wordlist:
            for word in wordlist:
                url = base_url + word.strip() + '/'
                t = test(url, ua, timeout)
                show(t, url, ignored_statuses)

    print('Elapsed time: ' + str(int(time.time() - start)) + ' seconds')
    print('Goodbye!')
    sys.exit()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main(sys.argv[1:])

#### TODO:
#### - output file
#### - handle dirs or files