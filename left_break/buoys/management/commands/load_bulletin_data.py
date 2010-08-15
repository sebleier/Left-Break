import datetime
from ftplib import FTP, error_perm
from django.core.management.base import NoArgsCommand
from left_break.buoys.models import Buoy
import left_break.buoys
import sys
import os
from multiprocessing import Process, Queue


class LineStorage(object):
    """
    Helper class for the FTP library.  Stores lines when used as a callback for
    certain ftp methods.
    """
    _lines = []
    def __call__(self, line):
        self._lines.append(line)

    def parse(self, line):
        raise NotImplementError("Subclasses must implement this method")

    @property
    def lines(self):
        return filter(lambda x: x is not None, map(self.parse, self._lines))

class DirStorage(LineStorage):
    def parse(self, line):
        now = datetime.datetime.now()
        folder = line.split(" ")[-1]
        if folder.startswith(now.strftime("%Y%m%d")):
            return folder
dirs = DirStorage()

class FileNameStorage(LineStorage):
    def parse(self, line):
        return line.split(" ")[-1]
filenames = FileNameStorage()


q = Queue()
def retreive_files():
    # Worker function that consumes the queue until empty
    ftp = FTP("polar.ncep.noaa.gov")
    ftp.login()
    BASE_DIR = '/pub/waves'
    ftp.cwd(BASE_DIR)
    while q.qsize():
        dirname, filename = q.get()
        try:
            os.mkdir(dirname)
        except OSError:
            pass
        pwd = ftp.pwd()
        if pwd != os.path.join(BASE_DIR, dirname):
            try:
                if len(pwd.split("/")) == 3:
                    path = os.path.join(BASE_DIR, dirname)
                else:
                    path = os.path.join("..", dirname)
                ftp.cwd(path)
            except error_perm:
                print "Cannot change directory to %s" % os.path.join(BASE_DIR, dirname, filename)
                continue
        try:
            sys.stdout.write("Retreiving %s..." % filename)
            ftp.retrbinary('RETR %s' % filename, open(os.path.join(dirname, filename), 'wb').write)
        except error_perm, e:
            sys.stdout.write("Error: %s\n" % str(e))
        else:
            sys.stdout.write("Done\n")

class Command(NoArgsCommand):
    help = "Download spectral data for the buoys"

    def handle(self, **options):
        buoys = []
        PATH = os.path.join(os.path.dirname(left_break.buoys.__file__), "data", "ftp")
        os.chdir(PATH)
        ftp = FTP("polar.ncep.noaa.gov")
        ftp.login()
        ftp.cwd('pub/waves/')
        ftp.dir(dirs)
        for folder in dirs.lines:
            ftp.cwd(folder)
            ftp.dir(filenames)
            ftp.cwd("..")
            for filename in filenames.lines:
                if filename.split(".")[-1] == "bull":
                    try:
                        buoy = Buoy.objects.get(name=filename.split(".")[-2])
                    except Buoy.DoesNotExist:
                        continue
                    q.put((folder, filename))
        processes = []
        NUM_PROCESSES = 8
        for i in range(NUM_PROCESSES):
            p = Process(target=retreive_files)
            processes.append(p)
            p.start()
        # Join the processes
        for i in range(NUM_PROCESSES):
            processes[i].join()
