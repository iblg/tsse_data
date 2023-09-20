import pandas as pd
import numpy as np
from tsse_data.check_spreadsheet import check_spreadsheet
from tsse_data.general_processing import check_willingness
from tsse_data.calibs import na_calib, cl_calib, linewise_calib
from tsse_data.general_processing import adjust_for_molecular_weight, convert_ion_to_salt


def create_org_ic_spreadsheet(filepath, dims, ions, spot=False, dish_label=False, second_dil=False):
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
    if check_willingness('create_org_ic_spreadsheet', filepath):
        cols = dims
        if spot:
            cols.append('spot')

        if dish_label:
            cols.append('dish_label')

        std_cols = ['m_dish', 'm_with_sample', 'm_with_salt', 'm_with_DI water']

        if second_dil:
            cols.append('m_solution_to_ic')
            cols.append('m_di_to_ic')

        [cols.append(col_name) for col_name in std_cols]

        [cols.append('A_' + ion) for ion in ions]

        df = pd.DataFrame(columns=dims)
        df.to_excel(filepath, index=False)

    return


def process_org_ic_spreadsheet(filepath, dims, ions, common_dims=None, print_raw_data=False, second_dilution=False,
                               salt_conversion=None):
    df = pd.read_excel(filepath)

    if print_raw_data:
        print(df)

    idx = check_spreadsheet(df, filepath, dims, common_dims)

    df = df.set_index(idx)

    df['m_sample'] = df['m_with_sample'] - df['m_dish']
    df['m_salt'] = df['m_with_salt'] - df['m_dish']
    df['m_solution'] = df['m_with_DI water'] - df['m_dish']

    for ion, calibration in ions.items():

        # transform to log
        # ds['log_' + 'A_' + ion] = np.log10(ds['A_' + ion])
        df['w_' + ion + '_to_ic'] = calibration(df['A_' + ion])
        # ds['log_w_' + ion] = calibration(ds['log_A_' + ion]) # use the calibration function passed
        # ds['w_' + ion + '_to_ic'] = 10 ** (ds['log_w_' + ion])  # re-transform from log units to normal

        # dilutions
        dil1 = df['m_solution'] / df['m_sample']

        if second_dilution:  # if you did a second dilution:
            dil2 = (df['m_solution_to_ic'] + df['m_di_to_ic']) / df['m_di_to_ic']
        else:
            dil2 = 1

        df['w_' + ion + '_rep'] = df['w_' + ion + '_to_ic'] * dil1 * dil2

    ds = df.to_xarray()
    for ion, calibration in ions.items():
        # average over replicates
        ds['w_' + ion] = ds['w_' + ion + '_rep'].mean(dim='replicate')
        ds['dw_' + ion] = ds['w_' + ion + '_rep'].std(dim='replicate') / np.sqrt(ds.sizes['replicate'])

        if salt_conversion is not None:
            ds = convert_ion_to_salt(ds, salt_conversion)

    return ds



def main():
    fp = './org_ic_spread.xlsx'

    dims = ['sample', 'temperature', 'ion', 'phase', 'replicate']
    ions = {'Cl': linewise_calib}

    # create_org_ic_spreadsheet(fp, dims, ions, spot=True, dish_label=True, second_dil=False)
    ds = process_org_ic_spreadsheet(fp, dims, ions)
    ds = ds.sel({'temperature': 25.0}, method='nearest').sel({'phase': 'o', 'ion': 'Cl'})
    # print(ds)
    ds = adjust_for_molecular_weight(ds, {'Cl': (35.45, 58.44, 'NaCl')})
    print(ds['dw_NaCl'])
    return


if __name__ == '__main__':
    main()
