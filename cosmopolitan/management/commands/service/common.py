import os

import cosmopolitan.management.commands.service.web as sweb
import cosmopolitan.management.commands.service.os as sos

HOST = "http://naciscdn.org"
HTTP_PATH = "/naturalearth/10m/cultural/"
FOLDER = "data/"


def prepare_data(file_data={}):
    # handle *.geojson file
    file_full_path = FOLDER + file_data["file_name_without_extension"]

    if not os.path.isfile(file_full_path+".geojson"):
        print("Processing GeoJSON")

        file_name = FOLDER + file_data["file_name"]

        sweb.Webfile(url=HOST + HTTP_PATH + file_data["file_name"],
                     file_name=file_name).download()

        if not os.path.exists(file_name):
            sos._super_log("Can't proceed, file %s not found" % file_name)
            return 1

        # unzip zip file
        outpath = FOLDER + file_data["file_name_without_extension"] + "/"
        sos.Unzip(file_name=file_name, outpath=outpath).run()

        # call org2org on unzipped stuff
        sos._format_ogr2ogr(path=FOLDER + file_data["file_name_without_extension"],
                            file_name=file_data["file_name_without_extension"])

    return sos.LoadPolygon(file_full_path).run()
