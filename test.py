# https://www.kernel.org/doc/html/v4.9/media/uapi/v4l/capture.c.html
# https://www.marcusfolkesson.se/blog/capture-a-picture-with-v4l2/

from v4l2 import ctl, constants, raw, utils
import os

device_path = '/dev/v4l/by-id/usb-SJ-180517-N_1080P_Webcam-video-index0'
device_path = '/dev/v4l/by-id/usb-3DO_3DO_NOZZLE_CAMERA_V2_3DO-video-index0'

# MARK: Query capabilities
cap = ctl.get_camera_capabilities(device_path)
print(cap)

if not ((cap['capabilities'] & constants.V4L2_CAP_VIDEO_CAPTURE) and (cap['capabilities'] & constants.V4L2_CAP_STREAMING)):
    exit(0)

# MARK: Set format
cam_format = raw.v4l2_format()

cam_format.type = constants.V4L2_BUF_TYPE_VIDEO_CAPTURE
cam_format.fmt.pixelformat = utils.pixelformat_to_fourcc('MJPG')
cam_format.fmt.pix.width = 640
cam_format.fmt.pix.height = 480
cam_format.fmt.pix.field = constants.V4L2_FIELD_INTERLACED

device_path = os.open(device_path, os.O_RDWR)

def test_get_format():
    fmt = raw.v4l2_format()
    fmt.type = constants.V4L2_BUF_TYPE_VIDEO_CAPTURE
    fd = device_path# os.open(device_path, os.O_RDWR)
    utils.ioctl_safe(fd, raw.VIDIOC_G_FMT, fmt)
    # os.close(fd)
    print(fmt.fmt.pix.width, fmt.fmt.pix.height)

test_get_format()
res = ctl.set_format(device_path, cam_format)
test_get_format()

# MARK: Request buffer
count = ctl.request_buffer(device_path, 3)

# MARK: Query and queue buffer
buffers = [None]*count
buffers_size = [None]*count
for i in range(count):
    buffers[i], buffers_size[i] = ctl.query_buffer(device_path, i)

for i in range(count):
    ctl.queue_buffer(device_path, i)

# MARK: Start streaming
ctl.start_streaming(device_path)

frames = []

with open("test.mp4", "wb") as vid:
    for i in range(300):
        # MARK: Dequeue buffer
        index = ctl.dequeue_buffer(device_path)
        # print(index)
        vid.write(buffers[index])
        ctl.queue_buffer(device_path, index)

# for i, frame in enumerate(frames):
#     with open(f"test/test{i}", "wb") as f:
#         f.write(frame)

ctl.stop_streaming(device_path)

os.close(device_path)
