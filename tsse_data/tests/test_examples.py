import xarray as xr
import pandas as pd
def test_one_plus_one_is_two():
    "Check that one and one are indeed two."
    assert 1 + 1 == 2

def test_merge(ds1, ds2):
    df1 = pd.Dataframe([1,2], columns = ['x1'])
    df2 = pd.Dataframe([3,4], columns = ['x2'])

    ds1 = df1.to_xarray()
    ds2 = df2.to_xarray()

    assert