import numpy as np



def na_calib(a):
    # filter: perform any filtering needed to determine which calibration function is best
    # to be implemented
    # apply function
    loga = np.log10(a)
    m = 1.010164931
    b = -5.434729452
    logw = m * loga + b
    w = 10 ** logw
    return w


def cl_calib(a):
    # filter: perform any filtering needed to determine which calibration function is best
    # to be implemented
    # apply function
    loga = np.log10(a)
    m = 0.9367262838
    b = -5.128
    logw = m * loga + b
    w = 10 ** logw
    return w
