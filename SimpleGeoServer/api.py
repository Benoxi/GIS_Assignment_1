import flask
from flask import request, jsonify
from flask_cors import CORS
from PIL import Image
import numpy

app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app)

# http://164.8.252.95/geoserver/gis/wms?
# BBOX=346681.25,10081.25,633400,2114,>56.25&
# STYLES=&
# FORMAT=image/png&
# REQUEST=GetMap&
# VERSION=1.1.1&
# LAYERS=gis:P100004&
# WIDTH=800&
# HEIGHT=521&
# SRS=EPSG:2170

def getImageByLayer(layer):
    location = "rester/PK1000_"
    img = Image.open(location)
    imgArray = numpy.array(img)
    imgArray.shape
    img.show()
    return 0

def getCapabilities():
    return 0

def cutImage(bBox, style, format, width, height, image):

    return 0

@app.route('/geoserver/gis/wms', methods=['GET'])
def wmsRequest():

    # Request validation
    for reqArgs in request.args:
        if len(request.args[reqArgs]) <= 0:
            return jsonify(reqArgs + " parameter is required!"), 422

    boundingBox = request.args['BBOX']
    styles = request.args['STYLES']
    format = request.args['FORMAT']
    req = request.args['REQUEST'] # GetMap or GetCapabilities
    version = request.args['VERSION'] # Set for other GeoServer
    layers = request.args['LAYERS'] #! TODO: Test if multiple variables create array?
    width = request.args['WIDTH']
    height = request.args['HEIGHT']
    srs = request.args['SRS'] # Ignore

    if req != "GetMap" or req != "GetCapabilities":
            return jsonify("Request parameter is invalid, only ['GetMap', 'GetCapabilities'] are valid values"), 422
    elif req == "GetMap":
        if "RS" in layers or "RSI" in layers or "ZDR" in layers :
            image = getImageByLayer(layers)
            resposne = cutImage(boundingBox, styles, format, width, height, image)
        else: # Send request forward!
            response = "Not yet imeplemented!"
    else:
        getCapabilities()

    return "Good request!"

app.run()

#getImageByLayer("RS")

