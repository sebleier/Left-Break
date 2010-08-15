import datetime
from ftplib import FTP
from left_break.buoys.models import Buoy
from django.core.management.base import NoArgsCommand

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

class Command(NoArgsCommand):
    help = "Download spectral data for the buoys"

    def handle(self, **options):
        buoys = []
        ftp = FTP("polar.ncep.noaa.gov")
        ftp.login()
        ftp.cwd('pub/waves/')
        ftp.dir(dirs)
        for folder in dirs.lines:
            ftp.cwd(folder)
            ftp.dir(filenames)
            names = []
            for filename in filenames.lines:

                if len(filename.split(".")) < 2:
                    continue
                name = filename.split(".")[1]
                try:
                    buoy = Buoy.objects.get(name__icontains=name)
                except Buoy.DoesNotExist:
                    pass
                else:
                    buoys.append(buoy)
            ftp.cwd("..")
        print buoys

