import pandas as pd

def create_kf_spreadsheet(filepath, dims):
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

    std_cols = ['wt_percent_water','m_sample', 'EP1', 'titer']
    [cols.append(col_name) for col_name in std_cols]

    df = pd.DataFrame(columns = dims)
    df.to_excel(filepath, index = False)
    return

def read_kf_spreadsheet(filepath):
    return pd.read_excel(filepath)




def main():
    dims = ['amine', 'sample', 'phase']
    fp = './kf_sheet.xlsx'
    create_kf_spreadsheet(fp, dims)

    return

if __name__ == '__main__':
    main()
