import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot_3by1(biorx_list, clms_list, df, **kwargs):
    """
###INPUTS###

biorx_list:
    list of bioreactor IDs to be plotted. Must match values in column "Sample ID"

clms_list:
    list of 3 columns to plot in descending order, 1 plot per column name

    list of relevant columns to plot:

    clms_list = ['VCD', 'Viability', 'Titer', 'O2 Saturation', 'PCO2', 'Gluc', 'Lac', 'pH','NH4+','Gln', 'Glu',
            'Na+', 'K+', 'Ca++', 'Qp']

df:
    dataframe containing list of columns above. Must contain "Sample ID", "Runtime" column which is used to group bioreactor IDs

    """

    #### plot specifications ###

    # pulling variable from
    vari = kwargs.get("legend", None)

    # filter data from input list
    data = df[df["Sample ID"].isin(biorx_list)]

    # y axis labels for each column name
    ylabels = {'VCD': "10E6 Cells/mL", 'Viability': "% Viable", 'Titer': "g/L", 'O2 Saturation': "% Air Saturation",
               'PCO2': "mmHg", 'Gluc': "g/L", 'Lac': "g/L", 'pH': "pH", 'NH4+': "mmol/L", 'Gln': "mmol/L",
               'Glu': "mmol/L",
               'Na+': "mmol/L", 'K+': "mmol/L", 'Ca++': "mmol/L", "Qp": "pg/cell day"}

    # x axis labels
    xmin = -0.5
    xmax = 14.

    # y axis minimum
    dict_ymin = {'VCD': 0, 'Viability': 40, 'Titer': 0, 'O2 Saturation': 0, 'PCO2': 0,
                 'Gluc': 0, 'Lac': 0, 'pH': 6.4, 'NH4+': 0, 'Gln': 0, 'Glu': 0, 'Na+': 0, 'K+': 0, 'Ca++': 0, "Qp": 0}

    #### FIGURE ####

    fig = plt.figure(figsize=(14, 10))

    num = 1
    for i in clms_list:
        # creating a column of 3 subplots
        ax = fig.add_subplot(3, 1, num)
        num += 1

        # iterating over grouped reactor ID
        for key, grp in data.groupby(['Sample ID']):
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

    plt.savefig("Figure_3by1.png", dpi=500)

