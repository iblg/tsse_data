import pandas as pd

def create_toc_spreadsheet(filepath, dims, tic = False, spot = False):
    """
    filepath : str
    The filepath to the TOC spreadsheet you wish to create.

    dims : list or array
    The list of column names that you wish to pass. These should be the same as the dims of your overall experiment.

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
    df['TOC'] = df['TOC_raw'] * (df['m_water'] + df['m_sample'])/df['m_sample']
    df['dTOC'] = df['dTOC_raw'] * (df['m_water'] + df['m_sample'])/df['m_sample']
    return df

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

def process_toc_spreadsheet(filepath):
    df = read_toc_spreadsheet(filepath)
    df = adjust_for_dilution(df)
    # df = convert_toc_w_amine(df, nc, mw)
    return df

def import_toc_measurement():
    """

    """
    pass

    return


# def main():
#     """
#
#     """
#     d = ['sample', 'phase', 'date', 'temperature']
#     # create_toc_spreadsheet('./toc_spreadsheet_1.xlsx', d, tic = False)
#
#     fp = './toc_spreadsheet_1.xlsx'
#     nc = 7
#     mw = 101.19
#     x = process_raw_toc_spreadsheet(fp, nc, mw)
#     print(x)
#
#     return
#
# if __name__ == '__main__':
#     main()