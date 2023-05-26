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


def check_willingness(func_name, filepath):
    print('Running ' + func_name + ' will overwrite any current spreadsheet in the location ' + filepath + '.')
    decision = input('Do you want to continue? Enter \'y\' to continue. Hit any other key to abort.')
    if decision == 'y':
        return True
    else:
        print('create_aq_ion_spreadsheet aborted.')
        return False
