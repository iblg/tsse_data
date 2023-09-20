import numpy as np
import pandas as pd


def linewise_calib(a: pd.Series):
    ### a general format for a linear log w log a calibration. You can change the break conditions
    # and the slopes as needed
    # filter: perform any filtering needed to determine which calibration function is best
    # to be implemented
    # apply function
    breaks = [10] # set your breakpoints here

    loga = np.log10(a)
    logw = pd.Series(0, index=a.index)

    for i, item in a.items():
        ## set params
        if item < breaks[0]:  # 0 is used as a condition here,
            m = 0.9367
            b = -5.128
        # elif item < breaks[1]:
        #     m = 1.010164931 #un-comment and modify values if needed
        #     b = -1.010164931 # you can add more calibration breakpoints if needed.
            pass
        else: #un-comment and modify values if needed
            m = 0.9367
            b = -5.128
            pass

        logw[i] = b + m * loga[i]

    w = 10 ** logw

    return w


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
