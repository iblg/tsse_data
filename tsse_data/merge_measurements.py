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

    return org


def main():
    org_ic = xr.DataArray(np.random.randn(2, 3, 2), dims=("phase", "sample", "temp"), coords={"temp": [10, 20]})
    org_ic_ds = xr.Dataset()
    org_ic_ds['w_w'] = org_ic
    kf = xr.DataArray(np.random.randn(2, 3, 2), dims=("phase", "sample", "temp"), coords={"temp": [10, 20]})
    kf_ds = xr.Dataset()
    kf_ds['w_w'] = kf
    kf_ds['dw_w'] = kf

    org = merge_org_phase(org_ic_ds, kf_ds)
    print(org)
    return


if __name__ == '__main__':
    main()
