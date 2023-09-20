import xarray as xr
import pandas as pd
from tsse_data.check_spreadsheet import check_spreadsheet, check_dims, write_common_dims_to_sheet, \
    write_variable_attrs


def check_dataset_dims(datasets, common_dims):
    for ds in datasets:
        if ds.dims == common_dims:
            pass
        else:
            print('One dataset contains dims that do not match the common dims.')
            print('The dims of this dataset are ')
        return

    return


def check_dataset_data():
    return


def set_attributes(ds, attributes):
    for key, val in attributes.items():
        ds.attrs[key] = val
    return ds


def merge_spreadsheets(filepaths, unique_dims, common_dims, attributes: dict = None, print_raw_data: bool = False):
    """
    Should take an iterable of filepaths. Should read in the spreadsheets as DataFrames, recognize dims,
    assign common_dims, check that data is in the form of weight fractions,
    Then attempt to merge them by coords.

    """
    check_dims(unique_dims, common_dims)
    ds_list = []
    first = True
    for fp in filepaths:
        df = pd.read_excel(fp)
        df = write_common_dims_to_sheet(df, common_dims)

        if print_raw_data:
            print('\nData from {}.'.format(fp))
            print(df)

        if first:
            idx = check_spreadsheet(df, fp, unique_dims, common_dims)
            first = False

        df = df.set_index(idx)
        ds = df.to_xarray()

        if attributes is not None:
            ds = set_attributes(ds, attributes) #this might not work if it applies attributes to all parts of the dataset
            # might have to be coords instead, as in experimenters' data

        ds_list.append(ds)

    ds = xr.combine_by_coords(ds_list)
    ds = write_variable_attrs(ds)

    return ds
