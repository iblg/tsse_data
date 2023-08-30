import xarray as xr
import pandas as pd


def incorporate_toc_kf(toc, kf):
    toc_res = toc[['w_a', 'dw_a']]
    kf_res = toc[['w_w', 'dw_w']]

    return


def main():
    df1 = pd.DataFrame([[1, 'first'], [2, 'second']], columns=['x1', 'desc']).set_index(['desc'])
    df2 = pd.DataFrame([[3, 'third'], [4, 'fourth']], columns=['x1', 'desc']).set_index(['desc'])

    ds1 = df1.to_xarray()
    ds2 = df2.to_xarray()
    ds3 = xr.concat([ds1, ds2], dim='desc')
    print(ds3)
    # ds3, ds4 = xr.align(ds1, ds2, join = 'outer')
    # print(ds3, ds4)
    # ds5 = xr.concat([ds3, ds4], dim = )
    return


if __name__ == '__main__':
    main()
