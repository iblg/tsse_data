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
        [idx.append(d) for d in common_dims]
    else:
        print('\n \n \ncommon_dims was passed but was format {}'.format(type(common_dims)))
        print('common_dims must be a dict. \n \n \n ')
    return idx