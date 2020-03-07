import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

#http://164.8.252.95/geoserver/gis/wms?
#BBOX=346681.25,10081.25,633400,2114,>56.25&
#STYLES=&
#FORMAT=image/png&
#REQUEST=GetMap&
#VERSION=1.1.1&
#LAYERS=gis:P100004&
#WIDTH=800&
#HEIGHT=521&
#SRS=EPSG:2170

@app.route('/geoserver/gis/wms', methods=['GET'])
def wmsRequest():
    boundingBox = NULL
    styles = NULL
    format = NULL
    request = NULL
    version = NULL
    layers = NULL
    width = NULL
    height = NULL
    srs = NULL

    if 'BBOX' in request.args:
        boundingBox = request.args['BBOX']
    else:
        return "Bounding Box parameter is required!"

    if 'STYLES' in request.args:
        styles = request.args['STYLES']

    if 'FORMAT' in request.args:
        format = request.args['FORMAT']
    else:
        return "Format parameter is required!"

    if 'REQUEST' in request.args:
        request = request.args['REQUEST']
    else:
        return "Request parameter is required!"

    if 'VERSION' in request.args:
        version = request.args['VERSION']
    else:
        return "Version parameter is required!"

    if 'LAYERS' in request.args:
        layers = request.args['LAYERS']
    else:
        return "Layers parameter is required!"

    if 'WIDTH' in request.args:
        width = request.args['WIDTH']
    else:
        return "Width parameter is required!"

    if 'HEIGHT' in request.args:
        height = request.args['HEIGHT']
    else:
        return "Height parameter is required!"

    if 'SRS' in request.args:
        srs = request.args['SRS']
    else:
        return "SRS parameter is required!"

    print(request);

app.run()
