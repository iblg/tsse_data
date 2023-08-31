def check_spreadsheet(df, filepath, dims, common_dims):
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
            if key in idx:
                pass
            else:
                idx.append(key)

    else:
        print('\n \n \ncommon_dims was passed but was format {}'.format(type(common_dims)))
        print('common_dims must be a dict. \n \n \n ')

    return idx


def check_dims(dims, common_dims):
    if isinstance(dims, list):
        pass
    else:
        print('\n \n \ndims was passed but was format {}'.format(type(dims)))
        print('dims must be a list of strings. \n \n \n ')

    if common_dims is None:
        pass
    elif isinstance(common_dims, dict):
        pass
    else:
        print('\n \n \ncommon_dims was passed but was format {}'.format(type(common_dims)))
        print('common_dims must be a dict. \n \n \n ')

    return


def write_common_dims_to_sheet(df, common_dims):
    for key, val in common_dims.items():
        df[key] = val
    return df


def write_variable_attrs(ds):
    cols = ['w_s', 'dw_s', 'w_a', 'dw_a', 'w_w', 'dw_w']
    long_names = ['Weight fraction salt',
                  'Uncertainty, weight fraction salt',
                  'Weight fraction amine',
                  'Uncertainty, weight fraction amine',
                  'Weight fraction water',
                  'Uncertainty, weight fraction water',
                  ]

    for col, ln in zip(cols, long_names):
        ds[col].attrs['units'] = 'g/g solution'
        ds[col].attrs['long_name'] = ln

    
    return ds