import pandas as pd
import numpy as np
from tsse_data.check_spreadsheet import check_spreadsheet
from tsse_data.calibs import na_calib, cl_calib
from tsse_data.general_processing import adjust_for_molecular_weight, df_to_ds, check_willingness


def create_aq_ic_spreadsheet(filepath, dims, ions: str, spot: bool = False, second_dilution: bool = False):
    """
    filepath : str
    The filepath to the TOC spreadsheet you wish to create.

    dims : list or array of str
    The list of column names that you wish to pass. These should be the same as the dims of your overall experiment.

    ions : list of str
    The list of ions that are being measured.

    spot : bool, default False
    If True, puts in a column for you to indicate the spot on the machine. If false, omits this column.

    second_dil :
    """
    # print('Running create_aq_ic_spreadsheet will overwrite any current spreadsheet in the location ' + filepath + '.')
    # decision = input('Do you want to continue? Enter \'y\' to continue. Hit any other key to abort.')
    # if decision == 'y':
    #     pass
    # else:
    #     print('create_aq_ion_spreadsheet aborted.')

    if check_willingness('create_aq_ic_spreadsheet', filepath):
        cols = dims
        if spot:
            cols.append('spot')

        std_cols = ['m_sample', 'm_DI']

        if second_dilution:
            std_cols += ['m_first_solution', 'm_DI_2']

        [cols.append(col_name) for col_name in std_cols]

        [cols.append('A_' + ion) for ion in ions]

        df = pd.DataFrame(columns=dims)
        df.to_excel(filepath, index=False)
    return


def process_aq_ic_spreadsheet(filepath, dims, ions,
                              salt=None,
                              common_dims: list = None,
                              print_raw_data: bool = False,
                              second_dilution: bool = False,
                              ):
    df = pd.read_excel(filepath)

    if print_raw_data:
        print(df)
    idx = check_spreadsheet(df, filepath, dims, common_dims)
    df = df.set_index(idx)

    # ds['m_sample'] = ds['m_with_sample'] - ds['m_dish']
    # ds['m_salt'] = ds['m_with_salt'] - ds['m_dish']
    df['m_solution'] = df['m_sample'] + df['m_DI']
    #
    for ion, calibration in ions.items():
        df['w_' + ion + '_to_ic'] = calibration(df['A_' + ion])

        # dilutions

        # first dilution
        dil1 = df['m_solution'] / df['m_sample']

        # if second dilution
        if second_dilution:
            try:
                dil2 = df['m_DI_2'] / df['m_first_solution']
            except KeyError:
                print('Second dilution key not found! The keys must be m_DI_2 and m_first_solution!')
        else:
            dil2 = 1.

        df['w_' + ion + '_rep'] = df['w_' + ion + '_to_ic'] * dil1 * dil2

    ds = df.to_xarray()

    # average over replicates
    for ion, calibration in ions.items():
        ds['w_' + ion] = ds['w_' + ion + '_rep'].mean(dim='replicate')
        ds['dw_' + ion] = ds['w_' + ion + '_rep'].std(dim='replicate') / np.sqrt(ds.sizes['replicate'])

    if salt is not None:
        ds = convert_ion_to_salt(ds, salt)

    return ds


def convert_ion_to_salt(ds, salt):
    if isinstance(salt, dict):
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

    i_name = salt['name_ion_measured']
    n_i = salt['n_ion']
    mw_i = salt['mw_ion']
    mw_s = salt['mw_salt']

    k = mw_s / (n_i * mw_i)

    ds['w_s'] = ds['w_' + i_name] * k
    ds['dw_s'] = ds['dw_' + i_name] * k

    return ds


def new_na_calib(a):
    # filter: perform any filtering needed to determine which calibration function is best
    # to be implemented
    # apply function
    loga = np.log10(a)
    m = 1
    b = 1
    logw = m * loga + b
    w = 10 ** logw
    return w


def main():
    dims = ['sample', 'replicate']
    addl_d = {'amine': 'dipa', 'cation': 'Na', 'anion': 'Cl'}
    ions = {
        # 'Na': na_calib,
        'Cl': cl_calib
    }
    fp = './aq_ic_sheet.xlsx'
    # create_aq_ic_spreadsheet(fp, dims, ions)

    ds = process_aq_ic_spreadsheet(fp, dims, ions, common_dims=addl_d,
                                   salt={'name_ion_measured': 'Cl', 'n_ion': 1, 'mw_ion': 35.45, 'mw_salt': 58.44})
    print(ds)

    return


if __name__ == '__main__':
    main()
