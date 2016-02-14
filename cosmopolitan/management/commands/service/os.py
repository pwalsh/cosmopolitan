import os
import json
import zipfile

def _super_log(message):
    print("-" * 18)
    print(message)
    print("-" * 18 + "\n")


def _format_ogr2ogr(path='', file_name=''):
    os.system("ogr2ogr -f 'GeoJSON' %(path)s.geojson %(path)s/%(file_name)s.shp" % \
              {'path': path, 'file_name': file_name})


class Unzip(object):
    def __init__(self, file_name='', outpath=''):
        self.file_name = file_name
        self.outpath = outpath

    def run(self):
        _super_log("Unziping the file...")
        with open(self.file_name, "rb") as f:
            z = zipfile.ZipFile(f)
            for name in z.namelist():
                z.extract(name, self.outpath)


class LoadPolygon(object):
    def __init__(self, path):
        self.path = path

    def run(self):
        with open(self.path + ".geojson") as f:
            data = json.load(f)
        return data
