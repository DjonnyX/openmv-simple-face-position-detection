# FacePositionDetection
#
# author: Eugene Grebennikov

import sensor, time, image, pyb, math

# Reset sensor
sensor.reset()

# setup sensor's
sensor.reset()
sensor.set_framesize(sensor.HQQVGA)
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_gainceiling(2)
sensor.set_contrast(3)
sensor.skip_frames()

# initialization usb/uart
usb = pyb.USB_VCP()

MAX_OFFSET = 30
RESET_TRACKING_TIMEOUT = 60
SKIP_FRAMES = 2

elapsed_to_reset = RESET_TRACKING_TIMEOUT
s_frames = SKIP_FRAMES

# HQQVGA half size
hw = 120 * 0.5
hh = 80 * 0.5

isReseted = True
epos = [0.0, 0.0]
lpos = [0.0, 0.0]
poss = [[0.0, 0.0]]

# send coordinates
def send(pos):
    f = b"%f:%f\n" % (pos[0], pos[1])
    usb.send(f)

def addPosition(x, y):
    sx = 0
    sy = 0
    l = len(poss)
    for p in poss:
      sx += p[0]
      sy += p[1]

    # img.draw_cross(int(sx), int(sy), 0xffffff, 4)

    nx = (sx/l-hw)/hw
    ny = (sy/l-hh)/hh

    send([nx, ny])

# initialize haar
face_cascade = image.HaarCascade("frontalface", stages=20)

while (True):
    elapsed_to_reset -= 1
    s_frames -= 1

    if elapsed_to_reset < 0:
        isReseted = True
        elapsed_to_reset = RESET_TRACKING_TIMEOUT

    # capture image
    img = sensor.snapshot()

    # face detection
    objects = img.find_features(face_cascade, threshold=0.81, scale_factor=1.35)

    # determination and sending to uart position coordinates
    for r in objects:
        x = r[0] + r[2] * 0.5
        y = r[1] + r[3] * 0.5

        dx = math.fabs(lpos[0] - x)
        dy = math.fabs(lpos[1] - y)

        if isReseted == False and (dx > MAX_OFFSET or dy > MAX_OFFSET):
            continue

        poss.pop(0)
        poss.append([x, y])

        if s_frames > 0:
            s_frames = SKIP_FRAMES
        addPosition(x, y)

        lpos[0] = x
        lpos[1] = y
        isReseted = False
        break
