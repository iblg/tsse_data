import pandas as pd
import typing as T
from numpy import polyfit
import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial.polynomial import Polynomial

def poly_fit(df: pd.DataFrame, num_rows: int, xcol: str = 'logA', ycol: str = 'logC', plot: bool = False,
             degree: int = None):
    # Calculate the degree of the polynomial
    if degree is None:
        degree = int(num_rows / 5)
    else:
        pass

    # Import polynomial fitting function

    # Fit the data to a polynomial
    res = polyfit(df[xcol], df[ycol], degree, full=True)
    coeffs = res[0]
    ssr = res[1]
    mse = ssr / num_rows
    std_err = np.sqrt(ssr / (num_rows - 2))
    # Print the polynomial coefficients

    if plot:
        plot_fit_vs_data(df, res, xcol, ycol, coeffs)

    frac_err = 10 ** std_err - 1
    func = Polynomial(coeffs)

    return func, mse, frac_err


def plot_fit_vs_data(df, res, xcol, ycol, coeffs):
    plt.plot(df[xcol], df[ycol], 'o', label='actual data')
    x = np.linspace(df[xcol].min(), df[xcol].max(), 100)
    y = np.zeros_like(x)

    for idx, val in enumerate(np.flip(coeffs)):
        y += x ** idx * val

    plt.plot(x, y, label='fit')
    plt.xlabel(xcol)
    plt.ylabel(ycol)
    plt.legend()
    plt.show()

    return


def main():
    # url = 'https://docs.google.com/spreadsheets/d/1ANBH6KZRnw76JkvNzLz3xAWzvHC9VsrhTen93ql1PRQ/edit#gid=1340378251'
    # wsheet_name = '2023-08-29-Rb'
    # df, num_rows = read_sheet(url, wsheet_name)
    # df = pd.read_csv('rb_calib.csv').dropna(axis='columns', how='all')
    # num_rows = df.shape[0]
    # coeffs, mse, frac_err = poly_fit(df, num_rows, ycol='log(w_Rb)', xcol='log (A_Rb)', plot=True)
    df = pd.read_csv('cation_calib.csv')
    num_rows = df.shape[0]
    func, mse, frac_err = poly_fit(df, num_rows, ycol='log(w_Na)', xcol='log (A_Na)', plot=True)
    print('coeffs {}'.format(*coeffs))
    print('mse {}'.format(mse))
    print('frac_err {}'.format(frac_err))
    return


if __name__ == '__main__':
    main()
