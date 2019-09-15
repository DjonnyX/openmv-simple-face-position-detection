# FacePositionDetection
#
# author: Eugene Grebennikov

import sensor, time, image, pyb, math

# Reset sensor
sensor.reset()

# setup sensor's
sensor.set_framesize(sensor.HQQVGA)
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_gainceiling(2)
sensor.set_contrast(3)
sensor.skip_frames()

# HQQVGA half size
half_width = 120 * 0.5
half_height = 80 * 0.5

isReseted = True
positions = [[0.0, 0.0]]

# send coordinates
def send(pos):
    f = b"%f:%f\n" % (pos[0], pos[1])
    print(f)

def getLen(x, y):
  return math.fabs(x + y) * 0.5

def addPosition(x, y):
    sx = 0
    sy = 0
    length = len(positions)
    for p in positions:
      sx += p[0]
      sy += p[1]

    img.draw_cross(int(sx), int(sy), 0xffffff, 4)

    norm_x = (sx / length - half_width) / half_width
    norm_y = (sy / length - half_height) / half_height

    send([norm_x, norm_y])

# initialize haar
face_cascade = image.HaarCascade("frontalface", stages=20)

while (True):
    elapsed_to_reset -= 1
    s_frames -= 1

    # capture image
    img = sensor.snapshot()

    # face detection
    objects = img.find_features(face_cascade, threshold=0.81, scale_factor=1.35)

    # determination and sending to uart position coordinates
    for r in objects:
        x = r[0] + r[2] * 0.5
        y = r[1] + r[3] * 0.5

        positions.pop(0)
        positions.append([x, y])

        addPosition(x, y)
        break
