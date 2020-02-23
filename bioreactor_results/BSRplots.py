import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math


import matplotlib.cm #color maps for plots


def global_color():
    """
    A function that creates global dictionary with color keys and rgba values to be used
    in plotting.
    """

    grey = matplotlib.cm.get_cmap("Greys")
    purple = matplotlib.cm.get_cmap("Purples")
    blue = matplotlib.cm.get_cmap("Blues")
    green = matplotlib.cm.get_cmap("Greens")
    orange = matplotlib.cm.get_cmap("Oranges")
    red = matplotlib.cm.get_cmap("Reds")

    cmap_dict = {"grey": grey,
                 "purple": purple,
                 "blue": blue,
                 "green": green,
                 "orange": orange,
                 "red": red}

    global global_dict

    global_dict = {}

    for key, value in cmap_dict.items():
        for i in list(range(1, 11)):
            global_dict[key + str(i)] = value(i / 10)
def manipulating_kwargs(**kwargs):
    """
    Processing kwargs for plot function: takes bioreactor list input and assigns values to plot color and legend
    based on used input in the plot function.

    return: dictionary with key = bioreactor ID, value = string with position 0 being color, position 1 is legend.

    """

    key_words = kwargs.get("kwargs", None)  # import all key words
    biorx_list = kwargs.get("biorx_list", None)  # importing list of bioreactor ID's

    color_dict = key_words.get("color", None)
    legend_dict = key_words.get("legend", None)

    #### Creating a dict with list of **kwargs. {key:[(rgbs color), legend]} ####

    # 1) setting bioreactor IDs as keys and values as list of None type
    kwargs_dict = {}
    for i in biorx_list:
        kwargs_dict[i] = [None, i]

    # 2) adding color value to first position in kwargs_dict list if kwarg exists

    global_color()  # running a function to create global color_dict rgb key

    if color_dict != None:
        color_dict = color_dict.copy()

        # converting color keys to rgb values
        for key, value in color_dict.items():
            if type(value) == float: #if Nan type value in color legend, simplistic and not robus solution
                color_dict[key] = None
            else:
                color_dict[key] = global_dict[value]  # pulling from global color_dict the rgb values

        # assinging rgb value to first item in kwargs_dict list value
        for key, value in kwargs_dict.items():
            value[0] = color_dict.get(key, value[0])

    # 3 adding legend value to the second position in kwargs_dict value
    if type(legend_dict) == dict:
        legend_dict = legend_dict.copy()

        for key, value in kwargs_dict.items():
            value[1] = legend_dict.get(key, value[1])

    if legend_dict == "no":
        for key, value in kwargs_dict.items():
            value[1] = None

    return kwargs_dict


ylabels = {'VCD': "10E6 Cells/mL", 'Viability': "% Viable", 'Titer': "g/L", 'O2 Saturation': "% Air Saturation",
               'PCO2': "mmHg", 'Gluc': "g/L", 'Lac': "g/L", 'pH': "pH", 'NH4+': "mmol/L", 'Gln': "mmol/L",
               'Glu': "mmol/L", 'Na+': "mmol/L", 'K+': "mmol/L", 'Ca++': "mmol/L", "Qp": "pg/cell day",
               "Osm": "mOsm/kg"}

    # y axis minimum
dict_ymin = {'VCD': 0, 'Viability': 40, 'Titer': 0, 'O2 Saturation': 0, 'PCO2': 0, "Osm": 250,
            'Gluc': 0, 'Lac': 0, 'pH': 6.4, 'NH4+': 0, 'Gln': 0, 'Glu': 0, 'Na+': 0, 'K+': 0, 'Ca++': 0, "Qp": 0}




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

color = dict of {"Sample ID": "color str"}
    color str must be in the following format, color# where # is number 01-10.
    color options are: "grey","purple","blue","green","orange","red"}

    example: {"R0010":"red5", "R0025":"blue5"}

    """

    #### plot specifications ###

    # pulling variable from **kwargs
    kwargs_dict = manipulating_kwargs(**locals())  # using seperate function to organize **kwargs

    # lgnd = kwargs.get("legend", None) #This needs to be updated to incorporate legend options
    x = kwargs.get("xmax", None)

    # filter data from input list
    df = df[df["Sample ID"].isin(biorx_list)]

    # filter data Runtime by xmax parameter if kwarg exists
    if (type(x) == int) or (type(x) == float):
        df = df[df["Runtime"] < x + 0.5]
    else:
        pass

    # x axis parameters
    xmin = -0.5

    if (type(x) == int) or (type(x) == float):
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
            ax.scatter(grp['Runtime'], grp[i], label='_nolegend_', color=kwargs_dict[key][0])  # Point plots

            mask = np.isfinite(grp[i])  # masking off missing data to avoid breaks in line plots
            ax.plot(grp['Runtime'][mask], grp[i][mask], label=kwargs_dict[key][1], color=kwargs_dict[key][0])

        ax.xaxis.set_ticks(np.arange(0, 30, 2))  # forcing ticks, every even value
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

    fig.legend(handles, labels, bbox_to_anchor=(0.7, .644), loc="upper left", fontsize=14, frameon=False)
    fig.tight_layout()
    fig.subplots_adjust(right=0.7)

    plt.savefig((str(clms_list) + ".png"), dpi=500)


#def plot_3by1(biorx_list, clms_list, df, **kwargs):
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
    """
    

    #### plot specifications ###

    # pulling variable from **kwargs
    vari = kwargs.get("legend", None)
    x = kwargs.get("xmax", None)

    # filter data from input list
    df = df[df["Sample ID"].isin(biorx_list)]

    # filter data Runtime by xmax parameter if kwarg exists

    if (type(x) == int) or (type(x) == float):
        df = df[df["Runtime"] < x + 0.5]
    else:
        pass


    # x axis parameters
    xmin = -0.5

    if (type(x) == int) or (type(x) == float):
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
            mask = np.isfinite(grp[i]) #plot lines are disconnected if Nan is present, boolean mask nans when plotting

            # legend based on **kwarg dict presence
            if type(vari) == dict:
                ax.plot(grp['Runtime'][mask], grp[i][mask], label=(key + " " + vari[key]))  # line plots

            else:
                ax.plot(grp['Runtime'][mask], grp[i][mask], label=(key))

        ax.xaxis.set_ticks(np.arange(0, 30, 2)) #forcing ticks, every even value
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
"""

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

    color = dict of {"Sample ID": "color str"}
        color str must be in the following format, color# where # is number 01-10.
        color options are: "grey","purple","blue","green","orange","red"}

    example: {"R0010":"red5", "R0025":"blue5"}

    xmax = int or float
        maximum value of the x-axis (days)

    """

    #### plot specifications ###

    # pulling variable from **kwargs
    kwargs_dict = manipulating_kwargs(**locals())  # using seperate function to organize **kwargs

    x = kwargs.get("xmax", None)

    # filter data from input list
    df = df[df["Sample ID"].isin(biorx_list)]

    # filter data Runtime by xmax parameter if kwarg exists
    if (type(x) == int) or (type(x) == float):
        df = df[df["Runtime"] < x + 0.5]
    else:
        pass

    # x axis parameters
    xmin = -0.5

    if (type(x) == int) or (type(x) == float):
        xmax = x + 0.5
    else:
        xmax = 14.5

    #### FIGURE ####

    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(21, 10))

    for i, ax in enumerate(fig.axes):

        for key, grp in df.groupby(['Sample ID']):
            clm = clms_list[i]  # column name from list, called by enumerated for loop

            ax.scatter(grp['Runtime'], grp[clm], label='_nolegend_', color=kwargs_dict[key][0])  # Point plots

            mask = np.isfinite(grp[clm])  # masking over NaN data (lines dont connect)
            ax.plot(grp['Runtime'][mask], grp[clm][mask], label=kwargs_dict[key][1], color=kwargs_dict[key][0])

        ax.xaxis.set_ticks(np.arange(0, 30, 2))
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

    fig.legend(handles, labels, bbox_to_anchor=(0.795, .644), loc="upper left", fontsize=15, frameon=False)
    fig.tight_layout()
    fig.subplots_adjust(right=0.79, wspace=0.15)

    plt.savefig((str(clms_list) + ".png"), dpi=500)

#def plot_2by2(biorx_list, clms_list, df, **kwargs):
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

    
    #### plot specifications ###

    # pulling variable from **kwargs
    vari = kwargs.get("legend", None)
    x = kwargs.get("xmax", None)

    # filter data from input list
    df = df[df["Sample ID"].isin(biorx_list)]

    # filter data Runtime by xmax parameter if kwarg exists
    if (type(x) == int) or (type(x) == float):
        df = df[df["Runtime"] < x + 0.5]
    else:
        pass


    # x axis parameters
    xmin = -0.5

    if (type(x) == int) or (type(x) == float):
        xmax = x + 0.5
    else:
        xmax = 14.5

    #### FIGURE ####

    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(21, 10))

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

        ax.xaxis.set_ticks(np.arange(0, 30, 2))
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
    fig.subplots_adjust(right=0.79, wspace=0.15)

    plt.savefig((str(clms_list) + ".png"), dpi=500)
    """

def plot_single(biorx_list, clm, df, **kwargs):
    """
    ###INPUTS###
    biorx_list:
        list of bioreactor IDs to be plotted. Must match values in column "Sample ID"

    clms:
        str. name of column to plot.

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
    kwargs_dict = manipulating_kwargs(**locals())  # using seperate function to organize **kwargs

    x = kwargs.get("xmax", None)

    # filter data from input list
    df = df[df["Sample ID"].isin(biorx_list)]

    # filter data Runtime by xmax parameter if kwarg exists
    if (type(x) == int) or (type(x) == float):
        df = df[df["Runtime"] < x + 0.5]
    else:
        pass

    # x axis parameters
    xmin = -0.5

    if (type(x) == int) or (type(x) == float):
        xmax = x + 0.5
    else:
        xmax = 14.5

    #### FIGURE ####

    fig, ax = plt.subplots(figsize=(15, 7.5))

    for key, grp in df.groupby(['Sample ID']):
        # clm = clms_list[i]  # column name from list, called by enumerated for loop

        ax.scatter(grp['Runtime'], grp[clm], label='_nolegend_', color=kwargs_dict[key][0])  # Point plots
        mask = np.isfinite(grp[clm])  # masking over NaN data (lines dont connect)

        # legend based on **kwarg legend dict presence
        ax.plot(grp['Runtime'][mask], grp[clm][mask], label=kwargs_dict[key][1], color=kwargs_dict[key][0])

    ax.xaxis.set_ticks(np.arange(0, 30, 2))
    ax.set_xlim(left=xmin, right=xmax)  # forcing a zero lower x limit (titer)

    ax.tick_params(axis='both', which='major', labelsize=24)  # tick labels size

    ax.set_ylabel(ylabels[clm], fontsize=24)  # y-axis label

    ax.yaxis.grid(color='gray', linestyle='dashed')
    ax.xaxis.grid(color='gray', linestyle='dashed')

    ax.set_title(clm, fontsize=25)
    ymin, ymax = ax.get_ylim()  # get the min and max of respective axes
    ax.set_ylim(bottom=dict_ymin[clm], top=ymax * 1.05)  # bottom defined by dict per each param, top = max*1.05

    ax.set_xlabel("Time (Days)", fontsize=24)  # x-axis label manually adding to outer

    handles, labels = ax.get_legend_handles_labels()

    fig.legend(handles, labels, bbox_to_anchor=(0.70, .644), loc="upper left", fontsize=20, frameon=False)
    fig.tight_layout()
    fig.subplots_adjust(right=0.70, wspace=0.15)

    plt.savefig((str(clm) + ".png"), dpi=500, bbox_inches='tight')




#def plot_single(biorx_list, clm, df, **kwargs):
    """
    ###INPUTS###
    biorx_list:
        list of bioreactor IDs to be plotted. Must match values in column "Sample ID"

    clms:
        str. name of column to plot.

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



    #### plot specifications ###

    # pulling variable from **kwargs
    vari = kwargs.get("legend", None)
    x = kwargs.get("xmax", None)

    # filter data from input list
    df = df[df["Sample ID"].isin(biorx_list)]

    # filter data Runtime by xmax parameter if kwarg exists
    if (type(x) == int) or (type(x) == float):
        df = df[df["Runtime"] < x + 0.5]
    else:
        pass


    # x axis parameters
    xmin = -0.5

    if (type(x) == int) or (type(x) == float):
        xmax = x + 0.5
    else:
        xmax = 14.5

    #### FIGURE ####

    fig, ax = plt.subplots(figsize=(15, 7.5))

    for key, grp in df.groupby(['Sample ID']):
        # clm = clms_list[i]  # column name from list, called by enumerated for loop

        ax.scatter(grp['Runtime'], grp[clm], label='_nolegend_')  # Point plots
        mask = np.isfinite(grp[clm])  # masking over NaN data (lines dont connect)

        # legend based on **kwarg legend dict presence
        if type(vari) == dict:
            ax.plot(grp['Runtime'][mask], grp[clm][mask], label=(key + " " + vari[key]))  # line plots
        else:
            ax.plot(grp['Runtime'][mask], grp[clm][mask], label=(key))

    ax.xaxis.set_ticks(np.arange(0, 30, 2))
    ax.set_xlim(left=xmin, right=xmax)  # forcing a zero lower x limit (titer)

    ax.tick_params(axis='both', which='major', labelsize=24)  # tick labels size

    ax.set_ylabel(ylabels[clm], fontsize=24)  # y-axis label

    ax.yaxis.grid(color='gray', linestyle='dashed')
    ax.xaxis.grid(color='gray', linestyle='dashed')

    ax.set_title(clm, fontsize=25)
    ymin, ymax = ax.get_ylim()  # get the min and max of respective axes
    ax.set_ylim(bottom=dict_ymin[clm], top=ymax * 1.05)  # bottom defined by dict per each param, top = max*1.05

    ax.set_xlabel("Time (Days)", fontsize=24)  # x-axis label manually adding to outer

    handles, labels = ax.get_legend_handles_labels()

    fig.legend(handles, labels, bbox_to_anchor=(0.70, .644), loc="upper left", fontsize=20)
    fig.tight_layout()
    fig.subplots_adjust(right=0.70, wspace=0.15)


    plt.savefig((str(clm) + ".png"), dpi=500, bbox_inches='tight')
    """

def calc_qp(df):
    """
    Calculates Cell Specific Productivity in units of pg/cell day and inserts result into a new column "Qp".
    Must contain columns: ["Runtime", "VCD", "Titer"]

    PARAMETERS

    df: datframe input


    RETURN

    df: original dataframe is returned with additional column, "Qp".


    """

    df["Qp"] = np.nan  # adding column to house data

    for key, grp in df.groupby(["Sample ID"]):
        temp = grp[grp["VCD"].notnull()]

        time_delta = temp["Runtime"].diff()  # getting time delta (x axis delta)
        VCD_shift = temp["VCD"].shift()  # shifting y column to do Yn + Y(n-1) for every row
        VCD_trapezoids = (temp["VCD"] + VCD_shift) * time_delta / 2  # area of each trapezoid
        IVCD = VCD_trapezoids.cumsum() * (10 ** 6)  # integrated area in units cells/mL * days
        titer_pg_ml = temp["Titer"] * (10 ** 9)  # converting titer to pg/ml

        qp = titer_pg_ml / IVCD  # the result
        ind = qp.index  # getting the index

        df.loc[ind, "Qp"] = qp  # index based assignment to original df

    return df







#Generic 3-pane and 4 pane plots to run plot functions in for loop
fig1 = ['VCD', 'Viability', 'Titer']
fig2 = ['VCD', 'Viability', 'Titer', "Qp"]
fig3 = ['Gluc', 'Lac',"Osm",'PCO2']
fig4 = ['Gln', 'Glu','pH','NH4+']
fig5 = ['Na+', 'K+', 'Ca++']

list_3pane = [fig1, fig5]
list_4pane = [fig2, fig3, fig4]


#legend dictionary: optional kwarg. Adds descriptive legend to plots
lgnd = {
    "R0007":"CFB, U144", "R0008":"CFB, U144",
        "R0009":"Fed-Batch", "R0010":"Fed-Batch",
        "R0011":"Perfusion, 0.2um", "R0012":"FB, control (-CB4)",
        "R0013": "FB, 5E10 inoc (-CB4)", "R0014": "FB, 5E10 inoc",
        "R0015": "CFB, C5", "R0016":"CFB, C5",
        "R0017":"Fed-Batch, control", "R0018":"Fed-Batch, 5E10 inoc",
        "R0019":"CFB, C5", "R0020":"CFB, C5", "R0021": "Perfsuion, 0.2um", "R0022":"Perfsuion, 0.2um",
        "R0023":"Perfsuion, 0.2um", "R0024":"CFB, C5", "R0025":"CFB, C5", "R0026": "CFB, C15"}



