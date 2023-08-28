import xarray as xr
import numpy as np
import xarray


def check_dims(aq_ic, toc, org_ic, kf):
    samples = aq_ic.dims['sample']

    cond = toc.dims['sample'] == samples

    return


def merge_measurements(aq_ic: xarray.Dataset,
                       toc: xarray.Dataset,
                       org_ic: xarray.Dataset,
                       kf: xarray.Dataset):
    """
    """

    check_dims(aq_ic, toc, org_ic, kf)

    return


def merge_org_phase(org_ic: xarray.Dataset, kf: xarray.Dataset):
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

    org = org_ic
    org['w_w'], org['dw_w'] = kf['w_w'], kf['dw_w']
    org['w_s'], org['w_s'] = org_ic['w_s'], org_ic['dw_s']

    org['w_a'], org['dw_a'] = find_third_component(x1=org['w_s'], x2=org['w_w'], dx1=org['dw_s'], dx2=org['dw_w'])

    return org


def merge_aq_phase(aq_ic, toc):
    if aq_ic.dims == toc.dims:
        pass
    else:
        print('merge_aq_phase cannot merge two datasets with different dims.')
        print('Dims of aq_ic are: \n {} \n'.format(aq_ic.dims))
        print('Dims of toc are: \n {} \n'.format(toc.dims))

    aq = aq_ic
    aq['w_a'], aq['dw_a'] = toc['w_a'], toc['dw_a']
    aq['w_s'], aq['w_s'] = aq_ic['w_s'], aq_ic['dw_s']
    aq['w_a'], aq['dw_a'] = find_third_component(x1=aq['w_s'], x2=aq['w_a'], dx1=aq['dw_s'], dx2=aq['dw_a'])

    return aq


def find_third_component(x1, x2, dx1=None, dx2=None):

    x3 = 1 - x1 - x2

    if (dx1 is not None) and (dx2 is not None):
        dx3 = np.sqrt(dx1 ** 2 + dx2 ** 2)
    elif dx1 is not None:
        dx3 = dx1
    elif dx2 is not None:
        dx3 = dx2
    else:
        return x3

    return x3, dx3


def main():
    org_ic = xr.DataArray(np.random.randn(2, 3, 2), dims=("phase", "sample", "temp"), coords={"temp": [10, 20]})
    org_ic_ds = xr.Dataset()
    org_ic_ds['w_s'] = org_ic
    org_ic_ds['dw_s'] = org_ic * 0.1
    kf = xr.DataArray(np.random.randn(2, 3, 2), dims=("phase", "sample", "temp"), coords={"temp": [10, 20]})
    kf_ds = xr.Dataset()
    kf_ds['w_w'] = kf
    kf_ds['dw_w'] = kf * 0.1

    org = merge_org_phase(org_ic_ds, kf_ds)
    aq = merge_aq_phase(org_ic_ds, kf_ds)
    print(org)
    return


if __name__ == '__main__':
    main()
