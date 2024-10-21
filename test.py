# https://www.marcusfolkesson.se/blog/capture-a-picture-with-v4l2/

from v4l2 import ctl, constants, raw, utils

device_path = '/dev/video0'

cap = ctl.get_camera_capabilities(device_path)
print(cap)

if not ((cap['capabilities'] & constants.V4L2_CAP_VIDEO_CAPTURE) and (cap['capabilities'] & constants.V4L2_CAP_STREAMING)):
    exit(0)

cam_format = raw.v4l2_format()

cam_format.type = constants.V4L2_BUF_TYPE_VIDEO_CAPTURE
cam_format.fmt.pixelformat = utils.pixelformat_to_fourcc('MJPG')
cam_format.fmt.pix.width = 1920
cam_format.fmt.pix.height = 1080
cam_format.fmt.pix.field = constants.V4L2_FIELD_NONE

def test():
    import os
    fmt = raw.v4l2_format()
    fd = os.open(device_path, os.O_RDWR)
    utils.ioctl_safe(fd, raw.VIDIOC_S_FMT, fmt)
    os.close(fd)
    print(fmt.fmt.pix.width, fmt.fmt.pix.height)

test()
res = ctl.set_format(device_path, cam_format)
test()

print(res)
