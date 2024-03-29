import numpy as np
import xarray
from pathlib import Path


def adjust_for_molecular_weight(ds: xarray.Dataset,
                                ion_tuple: dict):
    """
    ds: xarray.Dataset
    The dataset containing data that you wish to adjust for molecular weight.

    ion_tuple: dict
    A dictionary containing information about the salt and its component ions.

    Key: is ion name. e.g. 'Na' or 'CO3'.
    val[0] is total weight of ions of this species in formula unit, g/mol formula unit.
    e.g, for Na in NaCl, val[0] = 22.999. For Na in Na2CO3, val[0] = 45.998
    val[1] is weight of formula unit of the salt, in g/mol.
    val[2] is name of overall salt.
    """
    for ion, val in ion_tuple.items():
        salt = val[2]
        ds['w_' + salt] = ds['w_' + ion] * val[1] / val[0]
        ds['dw_' + salt] = ds['dw_' + ion] * val[1] / val[0]
    return ds


def df_to_ds(df):
    return df.to_xarray()


def check_willingness(func_name, filepath):
    print('Running ' + func_name + ' will overwrite any current spreadsheet in the location ' + filepath + '.')
    decision = input('Do you want to continue? Enter \'y\' to continue. Hit any other key to abort.')
    if decision == 'y':
        return True
    else:
        print('create_aq_ion_spreadsheet aborted.')
        return False


def convert_ion_to_salt(ds, salt_conversion):
    if isinstance(salt_conversion, dict):
        pass
    else:
        print('In convert_ion_to_salt')
        print('salt must be type dict. A non-dict was passed.')

    # if salt.keys() == ['name_ion_measured', 'n_ion', 'mw_ion', 'mw_salt']:
    #     pass
    # else:
    #     print('In convert_ion_to_salt')
    #     print('salt.keys() must be [\'name_ion_measured\', \'n_ion\', \'mw_ion\', \'mw_salt\']')
    #     print('Keys of salt were:')
    #     print(salt.keys())
    #     return

    i_name = salt_conversion['name_ion_measured']
    n_i = salt_conversion['n_ion']
    mw_i = salt_conversion['mw_ion']
    mw_s = salt_conversion['mw_salt']

    k = mw_s / (n_i * mw_i)

    ds['w_s'] = ds['w_' + i_name] * k
    ds['dw_s'] = ds['dw_' + i_name] * k

    return ds


def create_measurement_folder(filepath=None, dir_name='measurements'):
    if filepath:
        p = Path(filepath).resolve()
    else:
        p = Path.cwd().resolve()
    p = p / dir_name

    try:
        p.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        print("Folder {} is already there".format(dir_name))
    else:
        print("Folder {} was created".format(dir_name))

    return p


def average_over_replicates(ds, ions, salt_conversion):
    for ion, calibration in ions.items():
        # average over replicates
        ds['w_' + ion] = ds['w_' + ion + '_rep'].mean(dim='replicate')
        ds['dw_' + ion] = ds['w_' + ion + '_rep'].std(dim='replicate')

        if salt_conversion is not None:
            ds = convert_ion_to_salt(ds, salt_conversion)

    return ds

    return
