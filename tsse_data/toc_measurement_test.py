import toc_measurement as toc
import xarray as xr

def main():
    fp = './test_spread.xlsx'
    # dims = ['sample', 'amine']
    # toc.create_toc_spreadsheet(fp, dims)



    df = toc.process_toc_spreadsheet(fp)
    print(df)
    return

if __name__ == '__main__':
    main()