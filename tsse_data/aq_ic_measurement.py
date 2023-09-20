import pandas as pd
import numpy as np
from tsse_data.check_spreadsheet import check_spreadsheet
from tsse_data.calibs import na_calib, cl_calib
from tsse_data.general_processing import *


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
                              salt_conversion=None,
                              common_dims: list = None,
                              print_raw_data: bool = False,
                              second_dilution: bool = False,
                              ):
    df = pd.read_excel(filepath)

    if print_raw_data:
        print(df)
    idx = check_spreadsheet(df, filepath, dims, common_dims)
    df = df.set_index(idx)

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
                return
        else:
            dil2 = 1.

        df['w_' + ion + '_rep'] = df['w_' + ion + '_to_ic'] * dil1 * dil2

    ds = df.to_xarray()

    ds = average_over_replicates(ds, ions, salt_conversion)

    return ds


def main():
    dims = ['sample', 'replicate']
    addl_d = {'amine': 'dipa', 'cation': 'Na', 'anion': 'Cl'}
    ions = {
        # 'Na': na_calib,
        'Cl': cl_calib
    }
    fp = './aq_ic_sheet.xlsx'
    # create_aq_ic_spreadsheet(fp, dims, ions)

    ds = process_aq_ic_spreadsheet(fp, dims, ions,
                                   salt_conversion={'name_ion_measured': 'Cl', 'n_ion': 1, 'mw_ion': 35.45,
                                                    'mw_salt': 58.44}, common_dims=addl_d)
    ds = ds.sel(cation='Na', anion='Cl', amine='dipa')
    print(ds['w_s'].values)
    print(ds['dw_s'].values)

    return


if __name__ == '__main__':
    main()
