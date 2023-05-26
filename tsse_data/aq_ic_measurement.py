import pandas as pd
import numpy as np
from tsse_data.check_spreadsheet import check_spreadsheet


def create_aq_ic_spreadsheet(filepath, dims, ions, spot=False):
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
    print('Running create_aq_ic_spreadsheet will overwrite any current spreadsheet in the location ' + filepath + '.')
    decision = input('Do you want to continue? Enter \'y\' to continue. Hit any other key to abort.')
    if decision == 'y':
        pass
    else:
        print('create_aq_ion_spreadsheet aborted.')

    cols = dims
    if spot:
        cols.append('spot')

    std_cols = ['m_sample', 'm_DI']

    [cols.append(col_name) for col_name in std_cols]

    [cols.append('A_' + ion) for ion in ions]

    df = pd.DataFrame(columns=dims)
    df.to_excel(filepath, index=False)
    return


def process_aq_ic_spreadsheet(filepath, dims, ions, common_dims=None, print_raw_data=False):
    df = pd.read_excel(filepath)

    if print_raw_data:
        print(df)

    idx = check_spreadsheet(df, filepath, dims, common_dims)

    df = df.set_index(idx)

    # ds['m_sample'] = ds['m_with_sample'] - ds['m_dish']
    # ds['m_salt'] = ds['m_with_salt'] - ds['m_dish']
    # ds['m_solution'] = ds['m_with_DI water'] - ds['m_dish']
    #
    # for i, func in ions.items():
    #     k = 'A_' + i
    #     ds['log_' + k] = np.log10(ds[k])
    #     ds['log_w_' + i] = func(ds['log_' + k])
    #     ds['w_' + i + '_to_ic'] = 10 ** (ds['log_w_' + i])
    #     ds['w_' + i + '_rep'] = ds['w_' + i + '_to_ic'] * (ds['m_solution'] / ds['m_sample'])
    #
    #     ds['w_' + i] = ds['w_' + i + '_rep'].mean(dim='replicate')
    #     ds['dw_' + i] = ds['w_' + i + '_rep'].std(dim='replicate')/np.sqrt(2)

    return df


def adjust_for_calibration(df, ions):
    for i, t in ions.items():

        df['w_' + i + '_to_ic'] = np.zeros(df.shape[0])

        df.loc[:, 'w_' + i + '_to_ic'] = t(df.loc[:, 'A_' + i]) # This currently applies the same fxn to all rows
        # any row-by-row treatment must be done in the calibration function.

    return df


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


def adjust_for_dilution(df, ions):
    for i, t in ions.items():
        df['w_' + i + '_replicate'] = df['w_' + i + '_to_ic'] * (1 + df['m_DI'] / df['m_sample'])
    return df

def adjust_for_molecular_weight(df, ion_tuple):
    """
    ion_tuple: dict
    Key is ion name.
    val[0] is total weight of ions of this species in formula unit, g/mol formula unit.
    val[1] is weight of formula unit, g/mol.
    val[2] is name of overall salt.
    """
    for key, val in ion_tuple.items():
        df['w_' + val[2] + '_replicate'] = df['w_' + key + '_replicate'] * val[1] / val[0]

    return df

def df_to_ds(df):
    return df.to_xarray()


def main():
    dims = ['sample', 'replicate']
    addl_d = {'amine': 'dipa', 'cation': 'Na', 'anion': 'Cl'}
    ions = {'Na': na_calib, 'Cl': cl_calib}
    fp = './aq_ic_sheet.xlsx'
    # create_aq_ic_spreadsheet(fp, dims, ions)
    df = process_aq_ic_spreadsheet(fp, dims, ions, common_dims=addl_d)
    df = adjust_for_calibration(df, ions)
    df = adjust_for_dilution(df, ions)
    df = adjust_for_molecular_weight(df, {'Cl': (35.45, 58.44, 'NaCl')})
    ds = df_to_ds(df)

    print(ds['w_NaCl_replicate'])

    return


if __name__ == '__main__':
    main()
