import flask
from flask import request, jsonify
from flask_cors import CORS
from PIL import Image
import requests
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

# Class to store and work with our card
class GeoImage:
  def __init__(self, tifImage, tfwData):
      self.tifImage = tifImage
      self.tfwData = tfwData

def getImageByLayer(layers):
    geoImages = []
    for layer in layers:
        FileName = layer.replace("gis:", "")
        tifLocation = "raster/" + FileName + ".TIF"
        tfwLocation = "raster/" + FileName + ".tfw"
        f = open(tfwLocation, 'r')
        tfwData = f.readlines()
        geoImages.append(GeoImage(Image.open(tifLocation), tfwData))

    return geoImages

def getCapabilities():
    return 0

def cutImage(bBox, image):
    # Set orientation and cut out bBox clip
    

    return 0

def prepareImages(bBox, style, format, width, height, images):
    for img in images:
        img = cutImage(bBox, img)

    return 0

@app.route('/geoserver/gis/wms', methods=['GET'])
def wmsRequest():

    # Request validation
    for reqArgs in request.args:
        if reqArgs != 'STYLES':
            if len(request.args[reqArgs]) <= 0:
                print("Missing: ", reqArgs)
                return jsonify(reqArgs + " parameter is required!"), 422

    boundingBox = request.args['BBOX'].split(',')
    styles = request.args['STYLES'] # Can be empty
    format = request.args['FORMAT']
    req = request.args['REQUEST'] # GetMap or GetCapabilities
    version = '1.1.1'
    layers = request.args['LAYERS'].split(',')
    width = request.args['WIDTH']
    height = request.args['HEIGHT']
    srs = 'EPSG:2170'

    if req != "GetMap" and req != "GetCapabilities":
            return jsonify("Request parameter is invalid, only ['GetMap', 'GetCapabilities'] are valid values"), 422
    elif req == "GetMap":
        if "gis:P100004" in layers or "gis:P100051" in layers or "gis:P100052" in layers: # TODO: If good and bad layers???
            images = getImageByLayer(layers)
            response = prepareImages(boundingBox, styles, format, width, height, images)
        else: # Send request forward!
            response = requests.get('https://ion.gemma.feri.um.si/ion/services/geoserver/demo1/', data = {
                'BBOX': request.args['BBOX'],
                'STYLES': request.args['STYLES'],
                'FORMAT': request.args['FORMAT'],
                'REQUEST': request.args['REQUEST'],
                'VERSION': version,
                'LAYERS': request.args['LAYERS'],
                'WIDTH': request.args['WIDTH'],
                'HEIGHT': request.args['HEIGHT'],
                'SRS': srs
            })

        return response
    else:
        getCapabilities()

    return "Good request!"

app.run()

#getImageByLayer("RS")

