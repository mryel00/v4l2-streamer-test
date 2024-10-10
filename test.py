from v4l2 import ctl, constants

cap = ctl.get_camera_capabilities('/dev/video0')
print(cap)

if not ((cap['capabilities'] & constants.V4L2_CAP_VIDEO_CAPTURE) and (cap['capabilities'] & constants.V4L2_CAP_STREAMING)):
