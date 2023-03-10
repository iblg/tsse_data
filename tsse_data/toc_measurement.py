import pandas as pd
import numpy as np

def create_toc_spreadsheet(filepath, dims, tic = False, spot = False):
    """
    filepath : str
    The filepath to the TOC spreadsheet you wish to create.

    dims : list or array
    The list of column names that you wish to use as dims. These should be the same as the dims of your overall experiment.

    common_dims : dict, default None.
    additional dims that apply to all measurements in the spreadsheet. Keys become xarray dims; vals become xarray coords.

    tic : bool, default False.
    If true, does put in columns for recording total inorganic carbon. If false, omits these columns.

    spot : bool, default False
    If True, puts in a column for you to indicate the spot on the machine. If false, omits this column.
    """
    cols = dims
    if spot == True:
        cols.append('spot')

    std_cols = ['m_sample', 'm_water', 'TOC1_raw', 'TOC2_raw', 'TOC_raw', 'dTOC_raw']
    [cols.append(col_name) for col_name in std_cols]


    if tic == True:
        tic_cols = ['TIC1', 'TIC2', 'TIC', 'dTIC']
        [cols.append(col_name) for col_name in tic_cols]

    toc_sheet = pd.DataFrame(columns = cols)
    toc_sheet.to_excel(filepath, index = False)
    return

def read_toc_spreadsheet(filepath):
    """
    filepath : str
    The filepath to the TOC spreadsheet to be read. The TOC spreadsheet should be in the format previously generated by create_toc_spreadsheet.
    """
    df = pd.read_excel(filepath)
    return df

def adjust_for_dilution(df):
    """
    df : pandas.DataFrame
    The DataFrame containing the TOC data you are processing.
    """
    df['TOC_unavg'] = df['TOC_raw'] * (df['m_water'] + df['m_sample'])/df['m_sample']
    df['dTOC_unavg'] = df['dTOC_raw'] * (df['m_water'] + df['m_sample'])/df['m_sample']
    return df

def get_mean_toc(ds):
    """
    ds : xarray.Dataset
    ds is the TOC dataset under processing in process_toc_spreadsheet.

    This performs an unweighted mean and standard of the TOC over replicates. note: replicates here mean the different vials stuck
    into the TOC machine. Future versions of this may include the option to do a weighted average of multiple TOC machine
    readouts to take into account the fact that the TOC machine itself reports uncertainty.
    """
    ds['toc'] = ds['TOC_unavg'].mean(dim = 'replicate')
    ds['dtoc'] = ds['TOC_unavg'].std(dim = 'replicate')/np.sqrt(2)
    return ds

# def convert_toc_w_amine(df, nc, mw):
#     """
#     df : pandas.DataFrame
#     The DataFrame containing the TOC data you are processing.
#     nc : int
#     The number of carbon atoms your amine molecule contains.
#     mw : float
#     The molecular weight of your amine molecule.
#     """
#
#     if isinstance(nc, int):
#         pass
#     elif isinstance(nc, float):
#         nc = int(nc)
#         print('nc was passed as a float. Forcing to typecast as int.')
#     else:
#         print('nc was not an int. Please provide an integer nc to convert_toc_w_amine.')
#
#     if isinstance(mw, float):
#         pass
#     elif isinstance(nc, int):
#         pass
#     else:
#         print('mw was not a float. Please provide a float mw to convert_toc_w_amine.')
#
#
#     df['w_a'] = df['TOC'] * 10**(-9) * mw / (nc * 12.011)
#     df['dw_a'] = df['dTOC'] * 10**(-9) * mw / (nc * 12.011)
#     return df

def process_toc_spreadsheet(filepath, dims, common_dims = None):
    """
    filepath : str
    The filepath to the TOC spreadsheet you wish to create.

    dims : list or array
    The list of column names that you wish to use as dims. These should be the same as the dims of your overall experiment.

    common_dims : dict, default None.
    additional dims that apply to all measurements in the spreadsheet. Keys become xarray dims; vals become xarray coords.
    """
    df = read_toc_spreadsheet(filepath)

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
    df = adjust_for_dilution(df)

    ds = df.to_xarray()
    ds = get_mean_toc(ds)

    for i in idx:
        ds = ds.drop_duplicates(dim = i)
    # df = convert_toc_w_amine(df, nc, mw)
    return ds



def main():
    # """
    #
    # """
    d = ['sample', 'phase', 'temperature', 'replicate']
    addl_d = {'amine':'dipa', 'salt':'nacl'}
    # create_toc_spreadsheet('./toc_spreadsheet_1.xlsx', d, tic = False)
    #
    fp = './toc_spreadsheet_1.xlsx'
    ds = process_toc_spreadsheet(fp, d, common_dims = addl_d)
    print(ds)
    # ds = get_mean_toc(ds)
    # print(ds)
    #
    # print(x)
    # pass
    return

if __name__ == '__main__':
    main()