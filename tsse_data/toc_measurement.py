import pandas as pd
import numpy as np
from tsse_data.check_spreadsheet import check_spreadsheet
from tsse_data.general_processing import check_willingness


def create_toc_spreadsheet(filepath, dims, reporting='mean', meas_per_vial=2, h3po4=False, tic=False, spot=False):
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
    if check_willingness('create_toc_spreadsheet', filepath):
        cols = dims
        if spot:
            cols.append('spot')

        std_cols = ['m_sample', 'm_water']

        if h3po4:
            std_cols.append('m_h3po4')

        if reporting == 'mean':
            std_cols += ['toc_raw', 'dtoc_raw']
        elif reporting == 'replicates':
            repl_list = []
            [repl_list.append('TOC_{}_raw'.format(r)) for r in range(1, meas_per_vial + 1)]
            std_cols += repl_list
        else:
            print('No valid method of reporting provided to create_toc_spreadsheet().'
                  'Valid methods are \'mean\' or \'replicates\'.')

        [cols.append(col_name) for col_name in std_cols]

        if tic == True:
            tic_cols = ['TIC1', 'TIC2', 'TIC', 'dTIC']
            [cols.append(col_name) for col_name in tic_cols]

        toc_sheet = pd.DataFrame(columns=cols)

        toc_sheet.to_excel(filepath, index=False)

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
    df['w_toc_adj_dil'] = df['w_toc_calibrated'] * (1 + df['m_water'] / df['m_sample'])

    return df


def adjust_for_calibration(toc, calib):
    if calib is None:
        return toc
    toc = toc_calib(toc)
    return toc


def toc_calib(df: pd.DataFrame):
    ### a general format for a linear log w log a calibration. You can change the break conditions
    # and the slopes as needed
    # filter: perform any filtering needed to determine which calibration function is best
    # to be implemented
    # apply function
    toc = df['toc_raw']
    w_toc = df['w_toc_raw']
    breaks = [25000, 100000]  # set your breakpoints here

    log_w_toc = np.log10(w_toc)
    log_w_toc_calib = pd.Series(0, index=toc.index)

    for i, item in toc.items():
        ## set params
        if item < breaks[0]:
            m = 1.1019
            b = 0.12
        elif item < breaks[1]:
            m = 0.88
            b = -0.55
        else:
            print('TOC measurement is over range. Max value in this calibration curve is {}'.format(breaks[-1]))
            print('TOC was {}'.format(item))
            pass

        log_w_toc_calib[i] = b + m * log_w_toc[i]

    toc = 10 ** log_w_toc_calib

    return toc
#
#
# def low_calib(toc):
#     log_toc_meas = np.log10(toc)
#     log_toc_actual = log_toc_meas * 1.1019 + 0.12
#     print(log_toc_actual)
#
#     toc_actual = 10 ** log_toc_actual
#     return toc_actual
#
#
# def high_calib(toc):
#     log_toc_meas = np.log10(toc)
#     log_toc_actual = log_toc_meas * 0.88 - 0.55
#     toc_actual = 10 ** log_toc_actual
#     return toc_actual


def get_mean_toc(ds):
    """
    ds : xarray.Dataset
    ds is the TOC dataset under processing in process_toc_spreadsheet.

    This performs an unweighted mean and standard error of the TOC over replicates. note: replicates here mean the
    different vials put into the TOC machine. Future versions of this may include the option to do a weighted average
    of multiple TOC machine readouts to take into account the fact that the TOC machine itself reports uncertainty.
    """
    ds['dw_a'] = ds['w_a'].std(dim='replicate')
    ds['w_a'] = ds['w_a'].mean(dim='replicate')
    return ds


def convert_toc_w_amine(df, amine):
    nc = amine['nc']
    mw = amine['mw']

    if isinstance(nc, int):
        pass
    elif isinstance(nc, float):
        nc = int(nc)
        print('nc was passed as a float. Forcing to typecast as int.')
        print('nc is {}'.format(nc))
    else:
        print(
            'nc was not an int and could not be typecast as int. Please provide an integer nc to convert_toc_w_amine.')

    if isinstance(mw, float):
        pass
    else:
        print('mw was not a float. Please provide a float mw to convert_toc_w_amine.')

    df['w_a'] = df['w_toc_adj_dil'] * mw / (nc * 12.011)
    # df['dw_a'] = df['dw_toc_adj_dil'] * mw / (nc * 12.011) # temporarily, I have not worked in error propagation.
    return df


def process_toc_spreadsheet(filepath: str, dims: list, amine: dict, common_dims: dict = None, calib=None):
    """

    """
    df = read_toc_spreadsheet(filepath)


    idx = check_spreadsheet(df, filepath, dims, common_dims)
    df = df.set_index(idx)

    df['w_toc_raw'] = df['toc_raw'] / 10 ** 9
    df['dw_toc_raw'] = df['dtoc_raw'] / 10 ** 9

    df['w_toc_calibrated'] = adjust_for_calibration(df, toc_calib)
    df['dw_toc_calibrated'] = adjust_for_calibration(df, toc_calib)

    df = adjust_for_dilution(df)

    df = convert_toc_w_amine(df, amine)

    ds = df.to_xarray()

    ds = get_mean_toc(ds)

    return ds



def main():
    # """
    #
    # """
    d = ['sample', 'phase', 'temperature', 'replicate']
    addl_d = {'amine': 'dipa', 'salt': 'nacl'}
    # create_toc_spreadsheet('./toc_spreadsheet_1.xlsx', d, tic = False)
    #
    fp = './toc_spreadsheet_1.xlsx'
    dipa = {'nc': 6, 'mw': 101.19}
    ds = process_toc_spreadsheet(fp, d, amine=dipa, common_dims=addl_d,
                                 calib=toc_calib
                                 )

    ds = ds.sel({'amine': 'dipa', 'temperature': 25, 'phase': 'o', 'salt': 'nacl'})

    return


if __name__ == '__main__':
    main()
