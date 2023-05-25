import pandas as pd
import numpy as np
from tsse_data.check_spreadsheet import check_spreadsheet

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
    cols = dims
    if spot:
        cols.append('spot')

    if dish_label:
        cols.append('dish_label')

    std_cols = ['m_dish', 'm_with_sample', 'm_with_salt', 'm_with_DI water']

    if second_dil:
        cols.append('m_sol_to_ic')
        cols.append('m_DI_to_IC')

    [cols.append(col_name) for col_name in std_cols]

    [cols.append('A_' + ion) for ion in ions]

    df = pd.DataFrame(columns=dims)
    df.to_excel(filepath, index=False)
    return


def process_org_ic_spreadsheet(filepath, dims, ions, common_dims=None, print_raw_data=False):
    df = pd.read_excel(filepath)

    if print_raw_data:
        print(df)

    idx = check_spreadsheet(df, filepath, dims, common_dims)

    df = df.set_index(idx)

    ds = df.to_xarray()
    ds['m_sample'] = ds['m_with_sample'] - ds['m_dish']
    ds['m_salt'] = ds['m_with_salt'] - ds['m_dish']
    ds['m_solution'] = ds['m_with_DI water'] - ds['m_dish']

    for i, func in ions.items():
        k = 'A_' + i
        ds['log_' + k] = np.log10(ds[k])
        ds['log_w_' + i] = func(ds['log_' + k])
        ds['w_' + i + '_to_ic'] = 10 ** (ds['log_w_' + i])
        ds['w_' + i + '_rep'] = ds['w_' + i + '_to_ic'] * (ds['m_solution'] / ds['m_sample'])

        ds['w_' + i] = ds['w_' + i + '_rep'].mean(dim='replicate')
        ds['dw_' + i] = ds['w_' + i + '_rep'].std(dim='replicate')/np.sqrt(2)


    return ds


def main():
    fp = './org_ic_spread.xlsx'

    dims = ['amine', 'temperature', 'ion', 'phase', 'replicate']
    ions = ['cl']

    create_org_ic_spreadsheet(fp, dims, ions, spot=True, dish_label=True, second_dil=False)

    return


if __name__ == '__main__':
    main()
