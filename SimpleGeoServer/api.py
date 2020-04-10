import flask
from flask import request, jsonify
from flask_cors import CORS
# from PIL import Image
import cv2
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
        # turn tfw strings to floats
        self.tfwData = list(map(float, tfwData))
        self.croppedImage = {}

    def cropImage(self, x1, y1, x2, y2):
        self.croppedImage = self.tifImage[y1:y2, x1:x2]


def validateBoundingBox(bBox, geoImage):
    # Check all sides, if the coincide with image coords

    # x1,y1 must be smaller then x2,y2
    if bBox[0] > bBox[2] or bBox[1] > bBox[3]:
        return False

    RIGHT = geoImage.tfwData[4] + (geoImage.tfwData[0] * geoImage.tifImage.shape[1])
    DOWN = geoImage.tfwData[5] + (geoImage.tfwData[3] * geoImage.tifImage.shape[0])
    LEFT = geoImage.tfwData[4]
    UP = geoImage.tfwData[5]

    if RIGHT < bBox[2] or DOWN > bBox[1] or LEFT > bBox[0] or UP < bBox[3]:
        return False

    return True

def checkLayers(layers):
    for layer in layers:
        if layer != "gis:P100004" and layer != "gis:P100051" and layer != "gis:P100052":
            return False
    return True

def getImageByLayer(layers):
    geoImages = []
    for layer in layers:
        FileName = layer.replace("gis:", "")
        tifLocation = "raster/" + FileName + ".TIF"
        tfwLocation = "raster/" + FileName + ".tfw"
        f = open(tfwLocation, 'r')
        tfwData = f.readlines()
        geoImages.append(GeoImage(cv2.imread(tifLocation), tfwData))

    return geoImages

def getCapabilities():
    return 0

def cutImage(bBox, image):
    # Set orientation and cut out bBox clip
    x1 = int((bBox[0] - image.tfwData[4]) / image.tfwData[0])
    x2 = int((bBox[2] - image.tfwData[4]) / image.tfwData[0])
    y1 = int((bBox[3] - image.tfwData[5]) / (image.tfwData[3]))
    y2 = int((bBox[1] - image.tfwData[5]) / (image.tfwData[3]))

    image.cropImage(x1, y1, x2, y2)

    return image

def formatImage(image, format, width, height):
    cv2.imshow("image", image)

    return 0

def prepareImage(bBox, format, width, height, images):
    i = 0
    for img in images:
        img = cutImage(bBox, img)
        if i > 0:
            layerdImage = cv2.addWeighted(layerdImage, 1, img.croppedImage, 1, 0)
        else:
            layerdImage = img.croppedImage

        i += 1

    responseImage = formatImage(layerdImage, format, width, height)

    return responseImage

@app.route('/geoserver/gis/wms', methods=['GET'])
def wmsRequest():

    # Request validation
    for reqArgs in request.args:
        if reqArgs != 'STYLES':
            if len(request.args[reqArgs]) <= 0:
                print("Missing: ", reqArgs)
                return jsonify(reqArgs + " parameter is required!"), 422

    boundingBox = list(map(float, request.args['BBOX'].split(',')))
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
        if checkLayers(layers): # TODO: If good and bad layers???
            images = getImageByLayer(layers)
            # Validate bBox params
            if validateBoundingBox(boundingBox, images[0]):
                response = prepareImage(boundingBox, format, width, height, images)
            else:
                # Create "bbox out of bounds error message"
                return 0
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