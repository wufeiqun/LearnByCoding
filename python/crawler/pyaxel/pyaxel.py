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
import traceback
import threading

import requests
from docopt import docopt


class Downloader:
    """Light command line download accelerator"""
    def __init__(self, url, thread_num):
        self.url = url
        self.thread_num = thread_num
        self.filename = self.url.split("/")[-1]
        # Where to save the downloaded file, default is your current dir.
        self.put_dir = "."
        # Where to save the partial files temporary
        if "download" not in os.listdir("/tmp"):
            os.mkdir("/tmp/download")
        self.tmp_dir = "/tmp/download"
        self.filesize = self.get_filesize()
        self.alloc = self.filesize // self.thread_num

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

    def merge(self):
        """Merge all the files orderly"""
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

    def run(self):
        threads = []
        for n in range(self.thread_num-1):
            thread = threading.Thread(target=self.download, args=(n*self.alloc, n*self.alloc + self.alloc - 1))
            thread.start()
            threads.append(thread)
            print("{0} started.".format(thread.name))
        # Last thread download all the rest
        last_thread = threading.Thread(target=self.download, name="Thread-{0}".format(self.thread_num), args=((self.thread_num-1)*self.alloc, self.filesize))
        last_thread.start()
        threads.append(last_thread)
        print("{0} started.".format(last_thread.name))
        for thread in threads:
            thread.join()

        self.merge()


if __name__ == "__main__":
    args = docopt(__doc__, version="0.1")
    d = Downloader(args["<url>"], int(args["--thread"]))
    d.run()

