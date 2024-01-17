import xarray as xr
import numpy as np
import xarray


def merge_phases(org, aq):
    """

    """
    # check dims
    if org.dims == aq.dims:
        pass
    else:
        print('merge_phases cannot merge two datasets with different dims.')
        print('Dims of {} are: \n {} \n'.format(org.name, org.dims))
        print('Dims of {} are: \n {} \n'.format(aq.name, aq.dims))
        return

    merged = xr.concat([org, aq], dim='phase')
    return merged


def merge_org_phase(org_ic: xarray.Dataset, kf: xarray.Dataset, compatibility: str = 'override'):
    """
    Takes org_ic and kf, two xarray Datasets, and returns a single Dataset.
    To do this, merge_org_phase simply takes the org_ic dataset and adds variables for 'w_w' and 'dw_w'.

    org_ic: xarray.Dataset
    Data from organic IC measurement.

    kf: xarray.Dataset
    Data from KF measurement.
    """

    # check for same dims.
    if org_ic.dims == kf.dims:
        pass
    else:
        print('merge_org_phase cannot merge two datasets with different dims.')
        print('Dims of org_ic are: \n {} \n'.format(org_ic.dims))
        print('Dims of kf are: \n {} \n'.format(kf.dims))

    org = xr.combine_by_coords([org_ic, kf],
                               compat=compatibility  # currently, error message is being thrown on one column.
                               )
    # org = org_ic
    # org['w_w'], org['dw_w'] = kf['w_w'], kf['dw_w']
    # org['w_s'], org['w_s'] = org_ic['w_s'], org_ic['dw_s']

    org['w_a'], org['dw_a'] = find_third_component(x1=org['w_s'], x2=org['w_w'], dx1=org['dw_s'], dx2=org['dw_w'])

    return org


def merge_aq_phase(aq_ic, toc, compat: str = 'override'):
    if aq_ic.dims == toc.dims:
        pass
    else:
        print('merge_aq_phase cannot merge two datasets with different dims.')
        print('Dims of aq_ic are: \n {} \n'.format(aq_ic.dims))
        print('Dims of toc are: \n {} \n'.format(toc.dims))

    aq = xr.combine_by_coords([aq_ic, toc],
                              compat=compat  # currently, error message is being thrown on one column.
                              )

    aq['w_w'], aq['dw_w'] = find_third_component(x1=aq['w_s'], x2=aq['w_a'], dx2=aq['dw_a'])
    return aq


def find_third_component(x1, x2, dx1=None, dx2=None):
    # print('\n \n \nIn find_third_component')
    # print('x1: \n {}'.format(x1))
    # print('x2: \n {}'.format(x2))
    x3 = 1 - x1 - x2
    # print('Hello')
    if (dx1 is not None) and (dx2 is not None):
        dx3 = np.sqrt(dx1 ** 2 + dx2 ** 2)
    elif dx1 is not None:
        dx3 = dx1
    elif dx2 is not None:
        dx3 = dx2
    else:
        return x3

    return x3, dx3
