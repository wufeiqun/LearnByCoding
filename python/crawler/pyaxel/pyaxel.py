#!/usr/bin/env python3
"""
Usage:
    pyaxel.py <url>
    pyaxel.py [--thread=<num>] <url>

Options:
    -h --help        Show this screen.
    -V --version     Show version.
    --thread=<num>    Thread number [default: 10].

"""
import os
import sys
import glob
import time
import hashlib
import tempfile
import traceback
import threading
import contextlib
import urllib.request

import requests
from docopt import docopt

def progressbar(cursor, total, prefix = '', suffix = '', decimals = 1, barLength = 100):
    """
    Call in a loop to create terminal progress bar
    @params:
        cursor   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        barLength   - Optional  : character length of bar (Int)
    """
    formatStr = "{0:." + str(decimals) + "f}"
    percent = formatStr.format(100 * (cursor / float(total)))
    filledLength = int(round(barLength * cursor / float(total)))
    bar = '█' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)),
    if cursor == total:
        sys.stdout.write('\n')
    sys.stdout.flush()


class Downloader:
    """Light command line download accelerator"""
    def __init__(self, url, thread_num):
        self.url        = url
        self.thread_num = thread_num
        self.filename   = self.url.split("/")[-1]
        # Where to save the downloaded file, default is your current dir.
        self.put_dir    = "."
        # Place to save the  temporary partial files
        self.tmp_dir    = tempfile.TemporaryDirectory()
        self.filesize   = self.get_filesize()
        self.alloc      = self.filesize // self.thread_num

    def get_filesize(self):
        """Get content-length from headers (byte)"""
        req = urllib.request.Request(self.url, method="HEAD")
        with contextlib.closing(urllib.request.urlopen(req)) as resp:
            filesize = resp.length
            if not filesize:
                raise KeyError("Content-Length not found from headers")
        return filesize

    def download(self, start, end):
        """Download file separately"""
        bs = 1024 * 8  # block size (byte)
        headers = {"Range": "bytes={0:d}-{1:d}".format(start, end)}
        # Use the thread id as the partial filename, deleted after merged.
        filename = threading.current_thread().name.split("-")[1]

        req = urllib.request.Request(self.url, headers=headers)

        with contextlib.closing(urllib.request.urlopen(req)) as resp:
            with open(os.path.join(self.tmp_dir, filename), "wb") as f:
                while 1:
                    block = resp.read(bs)
                    if not block:
                        break
                    f.write(block)

    def merge(self):
        """Merge all the files orderly and checksum the data"""
        # if filename exists then append suffix with nums like "filename.0", "filename.1" etc.
        if os.path.exists(os.path.join(self.put_dir, self.filename)):
            num_files = glob.glob(os.path.join(self.put_dir, self.filename + ".*"))
            if num_files:
                max_num = max([int(num_file.split(".")[-1]) for num_file in num_files])
                self.filename = self.filename + str(max_num + 1)
            else:
                self.filename = self.filename + ".1"

        merged_file = open(os.path.join(self.put_dir, self.filename), "wb")

        # Order partial file by thread id
        sorted_flist = sorted(os.listdir(self.tmp_dir), key=lambda x: int(x))
        # Merged the partial file
        for partial in sorted_flist:
            with open(os.path.join(self.tmp_dir, partial), "br") as f:
                while 1:
                    block = f.read(1024*8)
                    if not block:
                        break
                    merged_file.write(block)
        merged_file.close()
        # Clean the tmpdir
        self.tmp_dir.cleanup()

    def md5(self, filename):
        hash_md5 = hashlib.md5()
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def info(self):
        """
        1. real URL
        2. filesize
        3. filename
        4. file MD5
        5. time consumtion
        """

    def run(self):
        threads = []
        for n in range(self.thread_num-1):
            thread = threading.Thread(target=self.download, args=(n*self.alloc, n*self.alloc + self.alloc - 1))
            thread.start()
            threads.append(thread)
        # Last thread download all the rest
        last_thread = threading.Thread(target=self.download, name="Thread-{0}".format(self.thread_num), args=((self.thread_num-1)*self.alloc, self.filesize))
        last_thread.start()
        threads.append(last_thread)
        for thread in threads:
            thread.join()
        # Merge the partial file,then delete the source partial file.
        self.merge()
        # Checksum the md5 of the merged file
        md5 = self.md5(self.filename)
        print("Filename: {0} ---> MD5: {1}".format(self.filename, md5))



def main():
    start = time.time()
    args = docopt(__doc__, version="0.1")
    d = Downloader(args["<url>"], int(args["--thread"]))
    d.run()
    end = time.time()
    print("Download finished with {0:.2f}s.".format(end-start))



if __name__ == "__main__":
    #d = Downloader("http://hellorfimg.zcool.cn/preview/425783590.jpg", 5)
    #print(d.get_filesize())
    main()

