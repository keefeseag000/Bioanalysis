import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot_3by1(biorx_list, clms_list, df, **kwargs):
    """
###INPUTS###
biorx_list:
    list of bioreactor IDs to be plotted. Must match values in column "Sample ID"

clms_list:
    list of 3 columns to plot in descending order, 1 plot per column name.

    list of relevant columns to plot:

    clms_list = ['VCD', 'Viability', 'Titer', 'O2 Saturation', 'PCO2', 'Gluc', 'Lac', 'pH','NH4+','Gln', 'Glu',
            'Na+', 'K+', 'Ca++', "Osm", 'Qp']

df:
    dataframe must contain columns: "Sample ID", "Runtime", at least 3 from clms_list

**kwargs:

legend = dict of {"Sample ID": "legend str"}
    example: {"R0014":"Fed-batch, control"}

xmax = int or float
    maximum value of the x-axis (days)

    """

    #### plot specifications ###

    # pulling variable from **kwargs
    vari = kwargs.get("legend", None)
    x = kwargs.get("xmax", None)

    # filter data from input list
    df = df[df["Sample ID"].isin(biorx_list)]

    # filter data Runtime by xmax parameter if kwarg exists

    if type(x) == (int or float):
        df = df[df["Runtime"] < x + 0.5]
    else:
        pass


    # y axis labels for each column name
    ylabels = {'VCD': "10E6 Cells/mL", 'Viability': "% Viable", 'Titer': "g/L", 'O2 Saturation': "% Air Saturation",
               'PCO2': "mmHg", 'Gluc': "g/L", 'Lac': "g/L", 'pH': "pH", 'NH4+': "mmol/L", 'Gln': "mmol/L",
               'Glu': "mmol/L", 'Na+': "mmol/L", 'K+': "mmol/L", 'Ca++': "mmol/L", "Qp": "pg/cell day",
               "Osm": "mOsm/kg"}

    # y axis minimum
    dict_ymin = {'VCD': 0, 'Viability': 40, 'Titer': 0, 'O2 Saturation': 0, 'PCO2': 0, "Osm": 250,
                 'Gluc': 0, 'Lac': 0, 'pH': 6.4, 'NH4+': 0, 'Gln': 0, 'Glu': 0, 'Na+': 0, 'K+': 0, 'Ca++': 0, "Qp": 0}

    # x axis parameters
    xmin = -0.5

    if type(x) == (int or float):
        xmax = x + 0.5
    else:
        xmax = 14.5

    #### FIGURE ####

    fig = plt.figure(figsize=(14, 10))

    num = 1
    for i in clms_list:
        # creating a column of 3 subplots
        ax = fig.add_subplot(3, 1, num)
        num += 1

        # iterating over grouped reactor ID
        for key, grp in df.groupby(['Sample ID']):
            ax.scatter(grp['Runtime'], grp[i], label='_nolegend_')  # Point plots
            mask = np.isfinite(grp[i])

            # legend based on **kwarg dict presence
            if type(vari) == dict:
                ax.plot(grp['Runtime'][mask], grp[i][mask], label=(key + " " + vari[key]))  # line plots

            else:
                ax.plot(grp['Runtime'][mask], grp[i][mask], label=(key))

        ax.set_xlim(left=xmin, right=xmax)  # forcing a zero lower x limit (titer)
        ax.tick_params(axis='both', which='major', labelsize=15)  # tick labels size
        ax.set_ylabel(ylabels[i], fontsize=15)  # y-axis label

        ax.yaxis.grid(color='gray', linestyle='dashed')
        ax.xaxis.grid(color='gray', linestyle='dashed')

        ax.set_title(i, fontsize=23)

        ymin, ymax = ax.get_ylim()  # get the min and max of respective axes
        ax.set_ylim(bottom=dict_ymin[i], top=ymax * 1.05)  # bottom defined by dict per each param, top = max*1.05

        # adding x-axis on the last subplot
        if num == 4:
            ax.set_xlabel("Time (Days)", fontsize=22, fontweight="bold")  # x-axis label
        else:
            pass

    handles, labels = ax.get_legend_handles_labels()

    fig.legend(handles, labels, bbox_to_anchor=(0.7, .644), loc="upper left", fontsize=14)
    fig.tight_layout()
    fig.subplots_adjust(right=0.7)

    plt.savefig((str(clms_list) + ".png"), dpi=500)


def plot_2by2(biorx_list, clms_list, df, **kwargs):
    """
    ###INPUTS###
    biorx_list:
        list of bioreactor IDs to be plotted. Must match values in column "Sample ID"

    clms_list:
        list of 3 columns to plot in descending order, 1 plot per column name.

        list of relevant columns to plot:

        clms_list = ['VCD', 'Viability', 'Titer', 'O2 Saturation', 'PCO2', 'Gluc', 'Lac', 'pH','NH4+','Gln', 'Glu',
                'Na+', 'K+', 'Ca++', "Osm", 'Qp']

    df:
        dataframe must contain columns: "Sample ID", "Runtime", at least 3 from clms_list

    **kwargs:

    legend = dict of {"Sample ID": "legend str"}
        example: {"R0014":"Fed-batch, control"}

    xmax = int or float
        maximum value of the x-axis (days)

    """

    #### plot specifications ###

    # pulling variable from **kwargs
    vari = kwargs.get("legend", None)
    x = kwargs.get("xmax", None)

    # filter data from input list
    df = df[df["Sample ID"].isin(biorx_list)]

    # filter data Runtime by xmax parameter if kwarg exists
    if type(x) == (int or float):
        df = df[df["Runtime"] < x + 0.5]
    else:
        pass

    # y axis labels for each column name
    ylabels = {'VCD': "10E6 Cells/mL", 'Viability': "% Viable", 'Titer': "g/L", 'O2 Saturation': "% Air Saturation",
               'PCO2': "mmHg", 'Gluc': "g/L", 'Lac': "g/L", 'pH': "pH", 'NH4+': "mmol/L", 'Gln': "mmol/L",
               'Glu': "mmol/L", 'Na+': "mmol/L", 'K+': "mmol/L", 'Ca++': "mmol/L", "Qp": "pg/cell day",
               "Osm": "mOsm/kg"}

    # y axis minimum
    dict_ymin = {'VCD': 0, 'Viability': 40, 'Titer': 0, 'O2 Saturation': 0, 'PCO2': 0, "Osm": 250,
                 'Gluc': 0, 'Lac': 0, 'pH': 6.4, 'NH4+': 0, 'Gln': 0, 'Glu': 0, 'Na+': 0, 'K+': 0, 'Ca++': 0, "Qp": 0}

    # x axis parameters
    xmin = -0.5

    if type(x) == (int or float):
        xmax = x + 0.5
    else:
        xmax = 14.5

    #### FIGURE ####

    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(20, 10))

    for i, ax in enumerate(fig.axes):

        for key, grp in df.groupby(['Sample ID']):
            clm = clms_list[i]  # column name from list, called by enumerated for loop

            ax.scatter(grp['Runtime'], grp[clm], label='_nolegend_')  # Point plots
            mask = np.isfinite(grp[clm])  # masking over NaN data (lines dont connect)

            # legend based on **kwarg legend dict presence
            if type(vari) == dict:
                ax.plot(grp['Runtime'][mask], grp[clm][mask], label=(key + " " + vari[key]))  # line plots
            else:
                ax.plot(grp['Runtime'][mask], grp[clm][mask], label=(key))

        ax.set_xlim(left=xmin, right=xmax)  # forcing a zero lower x limit (titer)

        ax.tick_params(axis='both', which='major', labelsize=19)  # tick labels size

        ax.set_ylabel(ylabels[clm], fontsize=19)  # y-axis label

        ax.yaxis.grid(color='gray', linestyle='dashed')
        ax.xaxis.grid(color='gray', linestyle='dashed')

        ax.set_title(clm, fontsize=23)
        ymin, ymax = ax.get_ylim()  # get the min and max of respective axes
        ax.set_ylim(bottom=dict_ymin[clm], top=ymax * 1.05)  # bottom defined by dict per each param, top = max*1.05

    axes[1, 0].set_xlabel("Time (Days)", fontsize=19, fontweight="bold")  # x-axis label manually adding to outer
    axes[1, 1].set_xlabel("Time (Days)", fontsize=19, fontweight="bold")  # x-axis label

    handles, labels = ax.get_legend_handles_labels()

    fig.legend(handles, labels, bbox_to_anchor=(0.795, .644), loc="upper left", fontsize=15)
    fig.tight_layout()
    fig.subplots_adjust(right=0.8, wspace=0.15)

    plt.savefig((str(clms_list) + ".png"), dpi=500)