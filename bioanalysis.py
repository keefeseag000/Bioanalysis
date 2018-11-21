import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


def grouped_histograms(df_data, df_group):
    """
    arguments:
    df_data = dataframe containing columns of data to be plotted as a histogram.
    df_group = dataframe containing a single column of categorical data.
                must be same number of rows as df_data.

    return: no object returned, however hist.png is saved in local dir
    """

    # forcing to use the following colors in this order for hist
    colors_list = ["blue", "crimson", "green", "cyan", "violet", "orange", "lime", "gold"]

    groups = df_group["Cond"].unique()  # array of unique groups
    n = 0  # counting subplots

    # logic for # of subplot rows for (# rows) x 4 subplot grid
    if len(df_data.columns) % 4 > 0:
        plt_rows = (int(len(df_data.columns)) + 1)
    else:
        plt_rows = int(len(df_data.columns) / 4)

    fig = plt.figure(figsize=(30, 20))

    # for every column, create a subplot.
    for i in df_data.columns:

        bin_count = int(
            (len(df[i])) ** (1 / 2))  # (# of bins) = sqaure root of number of data points, i.e., column length
        bin_edges = np.histogram(df_data[i].dropna(), bins=bin_count)[
            1]  # getting bin edges for all the data (all groups)

        n += 1
        ax = fig.add_subplot(plt_rows, 4, n)
        ax.set_title(i, fontsize=20, fontweight="bold")
        ax.tick_params(axis='both', which='major', labelsize=16)

        # for every group, draw a hist
        for p, color in zip(groups, colors_list):
            # index by group,
            ax.hist(df_data[df_group.iloc[:, 0] == p][i].dropna(), bins=bin_edges, alpha=0.7, label=p, color=color)
        plt.legend(fontsize=16)

    plt.tight_layout
    plt.savefig("hist.png", bbox_inches="tight", dpi=200)
    return
