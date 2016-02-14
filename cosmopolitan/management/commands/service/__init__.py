def _super_log(message):
    print("-" * 18)
    print(message)
    print("-" * 18 + "\n")


def _format_ogr2ogr(path='', file_name=''):
    return "ogr2ogr -f 'Polygon' %(path)s.Polygon %(path)s/%(file_name)s.shp" % \
        {'path': path, 'file_name': file_name}
