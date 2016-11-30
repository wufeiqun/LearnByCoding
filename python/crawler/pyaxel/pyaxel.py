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
import traceback
import threading
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
        # Where to save the partial files temporary
        if "download" not in os.listdir("/tmp"):
            os.mkdir("/tmp/download")
        self.tmp_dir    = "/tmp/download"
        self.filesize   = self.get_filesize()
        self.alloc      = self.filesize // self.thread_num

    def get_filesize(self):
        """Get content-length from headers"""
        try:
            resp = requests.head(self.url)
            filesize = resp.headers["Content-Length"]
            return int(filesize)
        except Exception as e:
            printf(traceback.format_exc(e))

    def download(self, start, end):
        """Download file separately"""
        headers = {"Range":"bytes={0:d}-{1:d}".format(start, end)}
        resp = requests.get(self.url, headers=headers, stream=True)
        # Use the thread id as the partial filename, deleted after merged.
        filename = threading.current_thread().name.split("-")[1]
        with open(os.path.join(self.tmp_dir, filename), "wb") as f:
            for chunk in resp.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    progressbar(f.tell(), self.alloc, prefix = "Thread{0}".format(filename), suffix = 'Complete', decimals = 1, barLength = 100)

    def merge(self):
        """Merge all the files orderly"""
        # if filename exists,add suffix ".new"
        if os.path.exists(os.path.join(self.put_dir, self.filename)):
            self.filename = self.filename + ".new"
        new_file = open(os.path.join(self.put_dir, self.filename), "wb")
        # Order by thread id
        sorted_flist = sorted(os.listdir(self.tmp_dir), key=lambda x: int(x))
        for partial in sorted_flist:
            with open(os.path.join(self.tmp_dir, partial), "br") as f:
                r = f.read(1024)
                while r:
                    new_file.write(r)
                    r = f.read(1024)
        new_file.close()
        for dirty_file in glob.glob("/tmp/download/*"):
            os.remove(dirty_file)

    def md5(self, filename):
        hash_md5 = hashlib.md5()
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

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
    main()

