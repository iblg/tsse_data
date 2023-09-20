import xarray
import xarray as xr


def w_to_x(ds: xarray.Dataset):
    """
    """
    water = (ds['w_w'], ds['dw_w'], ds.coords['mw_w'])
    amine = (ds['w_a'], ds['dw_a'], ds.coords['mw_a'])
    salt = (ds['w_s'], ds['dw_s'], ds.coords['mw_s'])

    ds['x_w'], ds['dx_w'] = get_x_single_component(water, amine, salt)
    ds['x_a'], ds['dx_a'] = get_x_single_component(amine, salt, water)
    ds['x_s'], ds['dx_s'] = get_x_single_component(salt, water, amine)

    return ds


def get_x_single_component(tuple1, tuple2, tuple3):
    w1, dw1, mw1 = tuple1[0], tuple1[1], tuple1[2]
    w2, dw2, mw2 = tuple2[0], tuple2[1], tuple2[2]
    w3, dw3, mw3 = tuple3[0], tuple3[1], tuple3[2]

    denom = w1 / mw1 + w2 / mw2 + w3 / mw3
    x1 = w1 / mw1 / denom
    dx1 = - w1 / (mw1 * denom ** 2) * (dw2 / mw2 + dw3 / mw3) + dw1 * (w1 / (mw1 ** 2 * denom ** 2) + 1 / (mw1 * denom))

    # as-yet untested function for finding the mole frac + uncertainty on a single one.
    return x1, dx1


def main():
    ds = xr.Dataset()
    ds['w_w'], ds['dw_w'] = 0.5, 0.01
    ds['w_a'], ds['dw_a'] = 0.3, 0.05
    ds['w_s'], ds['dw_s'] = 0.2, 0.03

    # ds = ds.expand_dims(dim=['amine','salt'])
    ds = ds.assign_coords({'mw_a': 101.19, 'mw_s':58.44, 'mw_w': 18.015})
    ds = w_to_x(ds)
    print(ds)


    return


if __name__ == '__main__':
    main()
