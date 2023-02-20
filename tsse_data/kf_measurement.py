import pandas as pd
import numpy as np

def create_kf_spreadsheet(filepath, dims):
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
    cols = dims

    std_cols = ['wt_percent_water','m_sample', 'EP1', 'titer']
    [cols.append(col_name) for col_name in std_cols]

    df = pd.DataFrame(columns = cols)
    df.to_excel(filepath, index = False)
    return df

def read_kf_spreadsheet(filepath):
    return pd.read_excel(filepath)

def process_kf_spreadsheet(filepath, dims, common_dims = None):
    """
    filepath : str
    The filepath to the KF spreadsheet you wish to create.

    dims : list or array
    The list of column names that you wish to use as dims. These should be the same as the dims of your overall experiment.

    common_dims : dict, default None.
    additional dims that apply to all measurements in the spreadsheet. Keys become xarray dims; vals become xarray coords.
    """
    df = read_kf_spreadsheet(filepath)

    if isinstance(filepath, str):
        pass
    else:
        print('\n \n \nfilepath was passed but was format {}'.format(type(filepath)))
        print('filepath must be a string. \n \n \n ')

    if isinstance(dims, list):
        idx = dims
        pass
    else:
        print('\n \n \ndims was passed but was format {}'.format(type(dims)))
        print('dims must be a list of strings. \n \n \n ')

    if common_dims is None:
        pass
    elif isinstance(common_dims, dict):
        for key, val in common_dims.items():  # write one column per common_dim
            df[key] = val
        [idx.append(d) for d in common_dims]
    else:
        print('\n \n \ncommon_dims was passed but was format {}'.format(type(common_dims)))
        print('common_dims must be a dict. \n \n \n ')

    df = df.set_index(idx)
    ds = df.to_xarray()
    ds = find_ww(ds)

    for i in idx:
        ds = ds.drop_duplicates(dim = i)

    return ds

def find_ww(ds):
    """
    ds : xarray.Dataset

    This function should put out
    """
    x = ds['wt_percent_water']/100.

    ds['w_w'] = x.mean(dim = 'replicate')
    ds['dw_w'] = x.std(dim = 'replicate')/np.sqrt(2)

    return ds

def main():
    # dims = ['amine', 'sample', 'phase']
    # fp = './kf_sheet.xlsx'
    # create_kf_spreadsheet(fp, dims)
    fp = '/Users/ianbillinge/Documents/yiplab/projects/new_saxs/phase_diagram/pd_kf.xlsx'
    df = read_kf_spreadsheet(fp)
    dims = ['amine', 'temperature', 'sample', 'replicate']
    ds = process_kf_spreadsheet(fp, dims, common_dims = {'phase':'org'})
    print(ds)

    return

if __name__ == '__main__':
    main()
