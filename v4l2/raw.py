#!/usr/bin/python3

import ctypes

from . import ioctl_macros

from . import constants

class v4l2_capability(ctypes.Structure):
    _fields_ = [
        ("driver", ctypes.c_char * 16),
        ("card", ctypes.c_char * 32),
        ("bus_info", ctypes.c_char * 32),
        ("version", ctypes.c_uint32),
        ("capabilities", ctypes.c_uint32),
        ("device_caps", ctypes.c_uint32),
        ("reserved", ctypes.c_uint32 * 3)
    ]

class v4l2_fmtdesc(ctypes.Structure):
    _fields_ = [
        ("index", ctypes.c_uint32),
        ("type", ctypes.c_uint32),
        ("flags", ctypes.c_uint32),
        ("description", ctypes.c_char * 32),
        ("pixelformat", ctypes.c_uint32),
        ("mbus_code", ctypes.c_uint32),
        ("reserved", ctypes.c_uint32 * 3)
    ]

class v4l2_pix_format(ctypes.Structure):
    class EncodingUnion(ctypes.Union):
        _fields_ = [
            ("ycbcr_enc",   ctypes.c_uint32),
            ("hsv_enc",     ctypes.c_uint32)
        ]
    _fields_ = [
        ("width",           ctypes.c_uint32),
        ("height",          ctypes.c_uint32),
        ("pixelformat",     ctypes.c_uint32),
        ("field",           ctypes.c_uint32),
        ("bytesperline",    ctypes.c_uint32),
        ("sizeimage",       ctypes.c_uint32),
        ("colorspace",      ctypes.c_uint32),
        ("priv",            ctypes.c_uint32),
        ("flags",           ctypes.c_uint32),
        ("union",           EncodingUnion),
        ("quantization",    ctypes.c_uint32),
        ("xfer_func",       ctypes.c_uint32)
    ]

class v4l2_plane_pix_format(ctypes.Structure):
    _pack_ = True
    _fields_ = [
        ("sizeimage",       ctypes.c_uint32),
        ("bytesperline",    ctypes.c_uint32),
        ("reserved",        ctypes.c_uint16 * 6)
    ]

class v4l2_pix_format_mplane(ctypes.Structure):
    class EncodingUnion(ctypes.Union):
        _fields_ = [
            ("ycbcr_enc",   ctypes.c_uint32),
            ("hsv_enc",     ctypes.c_uint32)
        ]
    _pack_ = True
    _fields_ = [
        ("width",           ctypes.c_uint32),
        ("height",          ctypes.c_uint32),
        ("pixelformat",     ctypes.c_uint32),
        ("field",           ctypes.c_uint32),
        ("colorspace",      ctypes.c_uint32),
        ("plane_fmt",       v4l2_plane_pix_format),
        ("num_planes",      ctypes.c_uint8),
        ("flags",           ctypes.c_uint8),
        ("union",           EncodingUnion),
        ("quantization",    ctypes.c_uint8),
        ("xfer_func",       ctypes.c_uint8)
        ("reserved",        ctypes.c_uint8*7)
    ]

class v4l2_rect(ctypes.Structure):
    _fields_ = [
        ("left",    ctypes.c_int32),
        ("top",     ctypes.c_int32),
        ("width",   ctypes.c_uint32),
        ("height",  ctypes.c_uint32)
    ]

class v4l2_clip(ctypes.Structure):
    _fields_ = [
        ("c",       v4l2_rect),
        ("next",    ctypes.POINTER("v4l2_clip"))
    ]

class v4l2_window(ctypes.Structure):
    _fields_ = [
        ("w",               v4l2_rect),
        ("field",           ctypes.c_uint32),
        ("chromakey",       ctypes.c_uint32),
        ("clip",            ctypes.POINTER(v4l2_clip)),
        ("clipcount",       ctypes.c_uint32),
        ("bitmap",          ctypes.POINTER(None)),
        ("global_alpha",    ctypes.c_uint8)
    ]

class v4l2_vbi_format(ctypes.Structure):
    _fields_ = [
        ("sampling_rate",       ctypes.c_uint32),
        ("offset",              ctypes.c_uint32),
        ("samples_per_line",    ctypes.c_uint32),
        ("sample_format",       ctypes.c_uint32),
        ("start",               ctypes.c_int32*2),
        ("count",               ctypes.c_uint32*2),
        ("flags",               ctypes.c_uint32),
        ("reserved",            ctypes.c_uint32*2)
        
    ]

class v4l2_sliced_vbi_format(ctypes.Structure):
    _fields_ = [
        ("service_set", ctypes.c_uint16),
        ("service_lines", ctypes.c_uint16*2*24),
        ("io_size", ctypes.c_uint32),
        ("reserved", ctypes.c_uint32*2)
    ]

class v4l2_sdr_format(ctypes.Structure):
    _pack_ = True
    _fields_ = [
        ("pixelformat", ctypes.c_uint32),
        ("buffer_size", ctypes.c_uint32),
        ("reserved",    ctypes.c_uint8*24)
    ]

class v4l2_meta_format(ctypes.Structure):
    _pack_ = True
    _fields_ = [
        ("dataformat",      ctypes.c_uint32),
        ("buffersize",      ctypes.c_uint32),
        ("width",           ctypes.c_uint32),
        ("height",          ctypes.c_uint32),
        ("bytesperline",    ctypes.c_uint32)
    ]
 
class v4l2_format(ctypes.Structure):
    class FormatUnion(ctypes.Union):
        _fields_ = [
            ("pix",         v4l2_pix_format),
            ("pix_mp",      v4l2_pix_format_mplane),
            ("win",         v4l2_window),
            ("vbi",         v4l2_vbi_format),
            ("sliced",      v4l2_sliced_vbi_format),
            ("sdr",         v4l2_sdr_format),
            ("meta",        v4l2_meta_format),
            ("raw_data",    ctypes.c_uint8 * 200)
        ]
        _anonymous_ = ("raw_data",)
    _fields_ = [
        ("type",    ctypes.c_uint32),
        ("fmt",     FormatUnion)
    ]

class v4l2_control(ctypes.Structure):
    _fields_ = [
        ("id",      ctypes.c_uint32),
        ("value",   ctypes.c_int32)
    ]

class v4l2_queryctrl(ctypes.Structure):
    _fields_ = [
        ("id",              ctypes.c_uint32),
        ("type",            ctypes.c_uint32),
        ("name",            ctypes.c_char * 8),
        ("minimum",         ctypes.c_int32),
        ("maximum",         ctypes.c_int32),
        ("step",            ctypes.c_int32),
        ("default_value",   ctypes.c_int32),
        ("flags",           ctypes.c_uint32),
        ("reserved",        ctypes.c_uint32 * 2)
    ]

class v4l2_querymenu(ctypes.Structure):
    class UnionNameValue(ctypes.Union):
        _fields_ = [
            ("name",    ctypes.c_char * 32),
            ("value",   ctypes.c_int64)
        ]
    _pack_ = True
    _fields_ = [
        ("id",          ctypes.c_uint32),
        ("index",       ctypes.c_uint32),
        ("union",       UnionNameValue),
        ("reserved",    ctypes.c_uint32)
    ]
    _anonymous_ = ("union",)

class v4l2_ext_control(ctypes.Structure):
    _pack_ = True
    class ValueUnion(ctypes.Union):
        _fields_ = [
            ("value",   ctypes.c_int32),
            ("value64", ctypes.c_int64),
            ("string",  ctypes.POINTER(ctypes.c_char)),
            ("p_u8",    ctypes.POINTER(ctypes.c_uint8)),
            ("p_u16",   ctypes.POINTER(ctypes.c_uint16)),
            ("p_u32",   ctypes.POINTER(ctypes.c_uint32)),
            ("p_s32",   ctypes.POINTER(ctypes.c_int32)),
            ("p_s64",   ctypes.POINTER(ctypes.c_int64)),
            ("ptr",     ctypes.POINTER(None))
        ]

    _fields_ = [
        ("id",          ctypes.c_uint32),
        ("size",        ctypes.c_uint32),
        ("reserved2",   ctypes.c_uint32 * 1),
        ("union",       ValueUnion)
    ]
    _anonymous_ = ("union",)

class v4l2_ext_controls(ctypes.Structure):
    class UnionControls(ctypes.Union):
        _fields_ = [
            ("ctrl_class",  ctypes.c_uint32),
            ("which",       ctypes.c_uint32)
        ]

    _fields_ = [
        ("union",       UnionControls),
        ("count",       ctypes.c_uint32),
        ("error_idx",   ctypes.c_uint32),
        ("request_fd",  ctypes.c_int32),
        ("reserved",    ctypes.c_uint32 * 1),
        ("controls",    ctypes.POINTER(v4l2_ext_control) )
    ]
    _anonymous_ = ("union",)

class v4l2_frmsize_discrete(ctypes.Structure):
    _fields_ = [
        ("width",   ctypes.c_uint32),
        ("height",  ctypes.c_uint32)
    ]

class v4l2_frmsize_stepwise(ctypes.Structure):
    _fields_ = [
        ("min_width",   ctypes.c_uint32),
        ("max_width",   ctypes.c_uint32),
        ("step_width",  ctypes.c_uint32),
        ("min_height",  ctypes.c_uint32),
        ("max_height",  ctypes.c_uint32),
        ("step_height",     ctypes.c_uint32)
    ]

class v4l2_frmsizeenum(ctypes.Structure):
    class FrmSize(ctypes.Union):
        _fields_ = [
            ("discrete", v4l2_frmsize_discrete),
            ("stepwise", v4l2_frmsize_stepwise)
        ]
    _fields_ = [
        ("index",           ctypes.c_uint32),
        ("pixel_format",    ctypes.c_uint32),
        ("type",            ctypes.c_uint32),
        ("union",           FrmSize),
        ("reserved",        ctypes.c_uint32 * 2)
    ]
    _anonymous_ = ("union",)

class v4l2_fract(ctypes.Structure):
    _fields_ = [
        ("numerator",   ctypes.c_uint32),
        ("denominator", ctypes.c_uint32)
    ]
class v4l2_frmival_stepwise(ctypes.Structure):
    _fields_ = [
        ("min",     v4l2_fract),
        ("max",     v4l2_fract),
        ("step",    v4l2_fract)
    ]

class v4l2_frmivalenum(ctypes.Structure):
    class FrmIval(ctypes.Union):
        _fields_ = [
            ("discrete", v4l2_fract),
            ("stepwise", v4l2_frmival_stepwise)
        ]
    _fields_ = [
        ("index",       ctypes.c_uint32),
        ("pixel_format",ctypes.c_uint32),
        ("width",       ctypes.c_uint32),
        ("height",      ctypes.c_uint32),
        ("type",        ctypes.c_uint32),
        ("union",       FrmIval),
        ("reserved",    ctypes.c_uint32 * 2)
    ]
    _anonymous_ = ("union",)

class v4l2_query_ext_ctrl(ctypes.Structure):
    _fields_ = [
        ("id",              ctypes.c_uint32),
        ("type",            ctypes.c_uint32),
        ("name",            ctypes.c_char * 32),
        ("minimum",         ctypes.c_int64),
        ("maximum",         ctypes.c_int64),
        ("step",            ctypes.c_uint64),
        ("default_value",   ctypes.c_int64),
        ("flags",           ctypes.c_uint32),
        ("elem_size",       ctypes.c_uint32),
        ("elems",           ctypes.c_uint32),
        ("nr_of_dims",      ctypes.c_uint32),
        ("dim",             ctypes.c_uint32 * constants.V4L2_CTRL_MAX_DIMS),
        ("reserved",        ctypes.c_uint32 * 32)
    ]


VIDIOC_QUERYCAP                 = ioctl_macros.IOR(ord('V'), 0, v4l2_capability)
VIDIOC_ENUM_FMT                 = ioctl_macros.IOWR(ord('V'), 2, v4l2_fmtdesc)
VIDIOC_G_CTRL                   = ioctl_macros.IOWR(ord('V'), 27, v4l2_control)
VIDIOC_S_CTRL                   = ioctl_macros.IOWR(ord('V'), 28, v4l2_control)
VIDIOC_QUERYCTRL                = ioctl_macros.IOWR(ord('V'), 36, v4l2_queryctrl)
VIDIOC_QUERYMENU                = ioctl_macros.IOWR(ord('V'), 37, v4l2_querymenu)
VIDIOC_G_EXT_CTRLS              = ioctl_macros.IOWR(ord('V'), 71, v4l2_ext_controls)
VIDIOC_S_EXT_CTRLS              = ioctl_macros.IOWR(ord('V'), 72, v4l2_ext_controls)
VIDIOC_ENUM_FRAMESIZES          = ioctl_macros.IOWR(ord('V'), 74, v4l2_frmsizeenum)
VIDIOC_ENUM_FRAMEINTERVALS      = ioctl_macros.IOWR(ord('V'), 75, v4l2_frmivalenum)
VIDIOC_QUERY_EXT_CTRL           = ioctl_macros.IOWR(ord('V'), 103, v4l2_query_ext_ctrl)
