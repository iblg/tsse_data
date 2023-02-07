import pandas as pd

def create_org_ic_spreadsheet(filepath, dims, ions, spot = False, dish_label = False, second_dil = False):
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
    if spot == True:
        cols.append('spot')

    if dish_label == True:
        cols.append('dish_label')

    std_cols = ['m_dish', 'm_with_water', 'm_with_salt', 'm_with_DI water']

    if second_dil == True:
        cols.append('m_sol_to_ic')
        cols.append('m_DI_to_IC')

    [cols.append(col_name) for col_name in std_cols]

    [cols.append('A_' + ion) for ion in ions]

    df = pd.DataFrame(columns=dims)
    df.to_excel(filepath, index=False)
    return

def main():
    fp = './org_ic_spread.xlsx'

    dims = ['amine', 'temperature', 'ion', 'phase', 'replicate']
    ions = ['cl']

    create_org_ic_spreadsheet(fp, dims, ions, spot = True, dish_label = True, second_dil = True)

    return

if __name__ == '__main__':
    main()