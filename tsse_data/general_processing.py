import numpy as np
import xarray


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
