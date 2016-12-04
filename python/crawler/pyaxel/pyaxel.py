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
import signal
import hashlib
import tempfile
import traceback
import threading
import contextlib
import urllib.request

from docopt import docopt


class Downloader:
    """Light command line download accelerator"""
    def __init__(self, url, thread_num):
        signal.signal(signal.SIGINT, self.handler)
        self.url        = self.get_url(url)
        self.thread_num = thread_num
        self.filename   = self.url.split("/")[-1]
        # Where to save the downloaded file, default is your current dir.
        self.put_dir    = "."
        # Place to save the  temporary partial files
        self.tmp_dir    = tempfile.TemporaryDirectory()
        self.filesize   = self.get_filesize()
        self.alloc      = self.filesize // self.thread_num

    def get_url(self, url):
        """Get real URL when status code is 301, 302, etc"""
        req = urllib.request.Request(url, method="HEAD")
        with contextlib.closing(urllib.request.urlopen(req)) as resp:
            real_url = resp.geturl()
            if url != real_url:
                return self.get_url(real_url)
            else:
                return url

    def get_filesize(self):
        """Get content-length from headers (byte)"""
        req = urllib.request.Request(self.url, method="HEAD")
        with contextlib.closing(urllib.request.urlopen(req)) as resp:
            # Check if the server support ranges(multithreading)
            if resp.headers.get("Accept-Ranges") == "bytes" and resp.headers.get("Content-Length"):
                filesize = int(resp.headers.get("Content-Length"))
                return filesize
            else:
                print("The server does not support multithread, start common download...")
                urllib.request.urlretrieve(self.url, os.path.join(self.put_dir, self.filename))


    def download(self, start, end):
        """Download file separately"""
        bs = 1024 * 8  # block size (byte)
        headers = {"Range": "bytes={0:d}-{1:d}".format(start, end)}
        # Use the thread id as the partial filename, deleted after merged.
        filename = threading.current_thread().name.split("-")[1]

        req = urllib.request.Request(self.url, headers=headers)

        try:
            with contextlib.closing(urllib.request.urlopen(req)) as resp:
                with open(os.path.join(self.tmp_dir.name, filename), "wb") as f:
                    while 1:
                        block = resp.read(bs)
                        if not block:
                            break
                        f.write(block)
        except KeyboardInterrupt:
            print("Catch KeyboardInterrupt, thread {0} will exit".format(filename))
            sys.exit(1)

    def merge(self):
        """Merge all the files orderly and checksum the data"""
        # if filename exists then append suffix with nums like "filename.0", "filename.1" etc.
        if os.path.exists(os.path.join(self.put_dir, self.filename)):
            num_files = glob.glob(os.path.join(self.put_dir, self.filename + ".*"))
            if num_files:
                max_num = max([int(num_file.split(".")[-1]) for num_file in num_files])
                self.filename = self.filename + "." + str(max_num + 1)
            else:
                self.filename = self.filename + ".1"

        merged_file = open(os.path.join(self.put_dir, self.filename), "wb")

        # Order partial file by thread id
        sorted_flist = sorted(os.listdir(self.tmp_dir.name), key=lambda x: int(x))
        # Merged the partial file
        for partial in sorted_flist:
            with open(os.path.join(self.tmp_dir.name, partial), "br") as f:
                while 1:
                    block = f.read(1024*8)
                    if not block:
                        break
                    merged_file.write(block)
        merged_file.close()
        # Clean the tmpdir
        self.tmp_dir.cleanup()
        # Check the filesize
        retrive_size = os.stat(os.path.join(self.put_dir, self.filename)).st_size
        if retrive_size < self.filesize:
            raise ContentTooShortError(
                    "retrieval incomplete: got only {0:d} out of {1:d} bytes"
                    .format(retrive_size, self.filesize), (self.filename,)
                    )

    def handler(self, signum, frame):
        print("Received {0}".format(signum))
        sys.exit(0)

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

