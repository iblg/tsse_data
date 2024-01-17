import pandas as pd
import numpy as np
from tsse_data.check_spreadsheet import check_spreadsheet, get_idx
from tsse_data.general_processing import check_willingness


def create_kf_spreadsheet(filepath: str, dims: tuple, ep1: bool = False, titer: bool = False):
    """
    filepath : str
    The filepath to the KF spreadsheet you wish to create.

    dims : list or array
    The list of column names that you wish to pass. These should be the same as the dims of your overall experiment.

    tic : bool, default False.
    If true, does put in columns for recording total inorganic carbon. If false, omits these columns.

    spot : bool, default False
    If True, puts in a column for you to indicate the spot on the machine. If false, omits this column.
    """
    if check_willingness('create_kf_spreadsheet', filepath):
        if isinstance(dims, tuple):
            pass
        else:
            print('\ndims must be a tuple. A {} was passed.'.format(type(dims)))
            print('\nCreating spreadsheet aborted.')
            return
        cols = list(dims)

        std_cols = ['wt_percent_water', 'm_sample', 'EP1', 'titer']

        if ep1:
            std_cols.append('EP1')

        if titer:
            std_cols.append('titer')

        [cols.append(col_name) for col_name in std_cols]

        df = pd.DataFrame(columns=cols)
        df.to_excel(filepath, index=False)
    return


def read_kf_spreadsheet(filepath):
    return pd.read_excel(filepath)


def process_kf_spreadsheet(filepath, dims, common_dims=None, print_raw_df=False):
    df = read_kf_spreadsheet(filepath)

    if print_raw_df:
        print(df)

    idx = get_idx(df, dims, common_dims)
    df = df.set_index(idx)
    ds = df.to_xarray()
    ds = find_ww(ds)

    for i in idx:
        ds = ds.drop_duplicates(dim=i)

    return ds


def find_ww(ds):
    """
    ds : xarray.Dataset

    This function should put out
    """
    x = ds['wt_percent_water'] / 100.

    ds['w_w'] = x.mean(dim='replicate')
    ds['dw_w'] = x.std(dim='replicate')

    return ds


def main():
    dims = ['sample', 'replicate']
    fp = './kf_sheet.xlsx'
    # create_kf_spreadsheet(fp, dims)
    # fp = '/Users/ianbillinge/dev/tsse_data/tsse_data/tests/merge_tests/kf.xlsx'
    df = read_kf_spreadsheet(fp)
    ds = process_kf_spreadsheet(fp, dims, common_dims={'phase': 'org'})
    print(ds)

    return


if __name__ == '__main__':
    main()
