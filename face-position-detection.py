# FacePositionDetection
#
# author: Eugene Grebennikov

import sensor, time, image, pyb, math

# Reset sensor
sensor.reset()

# setup sensor's
sensor.set_contrast(0)
sensor.set_gainceiling(16)
sensor.set_framesize(sensor.HQQVGA)
sensor.set_pixformat(sensor.GRAYSCALE)

# initialize haar
face_cascade = image.HaarCascade("frontalface", stages=24)

while (True):
    # capture image
    img = sensor.snapshot()

    # face detection
    objects = img.find_features(face_cascade, threshold=0.81, scale_factor=1.35)

    # determination position coordinates
    for r in objects:
        x = r[0] + r[2] * 0.5
        y = r[1] + r[3] * 0.5
        break
