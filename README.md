# DirDigger

**DirDigger** is a simple Python script that tries to do something like DIRB or DirBuster.

**Usage:**
```
usage: dirdigger.py [-h] -u URL -w WORDLIST [-m MODE] [-e FILE_EXTENSIONS]
                    [-i IGNORE_STATUSES] [-t TIMEOUT]

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     The base URL to start the scan from
  -w WORDLIST, --wordlist WORDLIST
                        The file containing the wordlist
  -m MODE, --mode MODE  Scan mode is "dir" or "file" (default: "dir")
  -e FILE_EXTENSIONS, --file-extensions FILE_EXTENSIONS
                        File extensions when mode is "file" (eg: php,aspx)
  -i IGNORE_STATUSES, --ignore-statuses IGNORE_STATUSES
                        HTTP statuses to be ignored (eg: 404,302)
  -t TIMEOUT, --timeout TIMEOUT
                        Request timeout in seconds (default: 5)
```

**Preview:**

<a href="https://ibb.co/pyKYDKz"><img src="https://i.ibb.co/pyKYDKz/Screenshot-from-2019-04-09-12-21-24.png" alt="DirDigger" border="0" /></a>
