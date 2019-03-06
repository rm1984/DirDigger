#!/usr/bin/env python3

#
# DirDigger
# ---------
# Coded by: Riccardo Mollo (riccardomollo84@gmail.com)
#

import getopt
import re
import requests
import signal
import subprocess
import sys
import time
import urllib3
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

def help():
    print('Usage: dirdigger.py [-h] | -u <url> -w <wordlist_file> [-i <status_codes>] [-t <timeout>]');
    print()
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

def show(status, url):
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
    if (len(argv) < 1):
        usage()
        sys.exit(1)

    try:
        opts, args = getopt.getopt(argv, 'hu:w:i:t:', ['url=', 'wordlist=', 'ignore=', 'timeout='])
    except getopt.GetoptError:
        usage()
        sys.exit(1)

    for opt, arg in opts:
        if opt == '-h':
            help()
            sys.exit()
        elif opt in ('-u', '--url'):
            base_url = arg
        elif opt in ('-w', '--wordlist'):
            wordlist_file = arg

    optsdict = dict(opts)

    if ('--ignore' in optsdict):
        ignore_status = optsdict['--ignore'].split(',')
    elif ('-i' in optsdict):
        ignore_status = optsdict['-i'].split(',')
    else:
        ignore_status = None

    if ('--timeout' in optsdict):
        timeout = int(optsdict['--timeout'])
    elif ('-t' in optsdict):
        timeout = int(optsdict['-t'])
    else:
        timeout = 5

    if (base_url[-1] != '/'):
        base_url += '/'

    start = time.time()

    logo()

    ua = UserAgent(cache=False, fallback='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36').random

    print('[+] Base URL: ' + base_url)
    print('[+] Wordlist: ' + wordlist_file)
    print('[+] Words count: ' + str(line_count(wordlist_file)))
    print('[+] Random user agent: ' + ua)
    if ignore_status is not None:
        print('[+] Ignored HTTP codes: ' + ', '.join(map(str, ignore_status)))
#    print('[+] Mode: DIRECTORY (adding trailing \'/\' when needed)')
    print('[+] Timeout: ' + str(timeout) + ' seconds')
    print('[+]')

    t = test(base_url, ua, timeout)
    show(t, base_url)

    if (t != 0):
        with open(wordlist_file, 'r') as wordlist:
            for word in wordlist:
                url = base_url + word.strip() + '/'
                t = test(url, ua, timeout)
                show(t, url)

    print('Elapsed time: ' + str(int(time.time() - start)) + ' seconds')
    print('Goodbye!')
    sys.exit()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main(sys.argv[1:])

#### TODO:
#### - output file
#### - handle dirs or files
