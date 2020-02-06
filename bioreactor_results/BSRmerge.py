import pandas as pd
from os import listdir
import datetime
import re
import numpy as np


def vicell_convert_xlsx():
    """
    Converts all .xlsx files in present working directory

    Return: Dictionary. Keys = filename.xlsx, values = Dataframe
    """

    #### Listing all files in directory ####
    files_list = listdir()  # list of all files in pwd
    L_xlsx = [i for i in files_list if i[-4:] == "xlsx"]  # isolating files that end in "xlsx"
    print("####   ViCell Import Report ####")
    print("\n")
    print("Total number of .xlsx files in dir: " + str(len(L_xlsx)))
    print("List of .xlsx files: " + str(L_xlsx))
    print("\n")

    #### importing all xlsx files into a list of dataframes and Running ViCell file verification ####

    # importing all .xlsx files into dataframes
    print("Converting excel files into DataFrames: ")
    D_df = {}
    for i in L_xlsx:
        try:
            df = pd.read_excel(i)
            D_df[i] = df
            print(i + ": " + "CONVERTED")
        except:
            print("Failed to convert the following file into pandas dataframe: " + str(i))

    return D_df

def vicell_check_format(D_df):
    """
    Checking for ViCell data format consitency

    Input: Dictionary of dataframes.
    out: print statements
    """
    print("\n")
    print("#### ViCell Format Report ####")
    print("\n")
    print("Total files to verify: " + str(list(D_df.keys())))
    for key, df in D_df.items():

        if (
                df.columns[0][0:7] == "Vi-CELL" and  # first 7 characters of column 0 are "Vi-CELL
                df.iloc[2, 0] == "Bioprocess:" and  # column 0, row 2 is "Bioproces"
                df.iloc[3, 1] == "File name" and  # column 1, row 3 is "File name"
                df.iloc[3, 2] == "Cell type" and  # column2, row 3 is "Cell tppe"
                df.iloc[3, 4] == 'Sample date/time' and  # column 4 row 3 is "Sample date/time"
                df.iloc[3, 7] == 'Viability' and  # column 7 row 3 is "Viability"
                df.iloc[4, 7] == "(%)" and  # column 7 row 4 is "(%)
                df.iloc[3, 9] == 'Viable cells' and  # column 9 row 3 is "Viable cells"
                df.iloc[4, 9] == '/ml (x10^6)' and  # column 9 row 4 is '/ml (x10^6)'
                list(df.iloc[5, 0:10]) == [0, 1, 2, 10, 11, 12, 13, 14, 15, 16]
        # row 5 is just a series of number across all clms
        ):
            print(key + ": " + "CONFIRMED")
        else:
            print(key + ": " + "FAILED to confirm ViCell Format")

def vicell_clean(D_df):
    """
    Cleans up data from dataframe that is confirmed to have ViCell format from .xlsx file.


    Input: Dictionary of dataframes
    Return: Dictionary of dataframes
    """

    print("\n")
    print("#### ViCell Data Cleaning Report ####")
    print("\n")

    for key, df in D_df.items():

        # Getting list of strings from rows 3 and 4. These are the column headers that ViCell split into 2 rows.

        clms_list1 = []
        clms_list2 = []
        for i in df.loc[3, :]:
            clms_list1.append(i)
        for i in df.loc[4, :]:
            clms_list2.append(i)

        # Combining the strings from rows 3 and 4 to be the new column name

        combined = []
        for i, j in zip(clms_list1, clms_list2):
            if (type(i) == str) and (type(j) == str):
                combined.append(i + j)
            else:
                combined.append(i)

        df.columns = combined  # setting the columns to combined strings from rows 3 and 4/

        # dropping first 6 rows and resetting index

        df.drop(df.index[0:6], inplace=True)
        df.reset_index(inplace=True, drop=True)

        # dropping duplicates (just in case), becomes more important after mergin multiple vicell files

        # Shortening column data into the first 4 characters: Sample ID, File name
        df["Sample ID"] = df["Sample ID"].str.slice(0, 5)  # shortening Sample ID colum to first 4 characters
        df["File name"] = df["File name"].str.slice(0, 5)  # shortening "File name" column

        # verify that Sample ID column = File name column
        unequal_id = df["Sample ID"] != df["File name"]
        L_unequal = list(df[unequal_id].index)

        print(key + "-------- Data Cleaning Complete")

        if not L_unequal:
            print("All Sample ID's match File name")
        else:
            print("WARNING! Sample ID does not match File name for the following indeces: " + str(L_unequal))

        # verify that all "Cell type = "CHO"
        L_notCHO = list(df[df["Cell type"] != "CHO"].index)

        if not L_notCHO:
            print("All samples are of type: CHO")
        else:
            print("WARNING! Cell type is not CHO at the following index: " + str(L_notCHO))

    return D_df

def vicell_merge_convert(D_df):
    """
    Merging all dataframes in a dictionary, converting datatypes (datetime), and isolating essential columns

    Input: Dictionary of dataframes
    Return: dataframe with the following columns: 'Sample ID','Sample date/time','Viability(%)','Viable cells/ml (x10^6)'

    """

    print("\n")
    print("#### ViCell Data Merge Report ####")
    print("\n")

    df = pd.concat(D_df.values(), ignore_index=True)  # merge all datafrmes
    df.drop_duplicates(subset="Sample date/time", inplace=True)  # dropping duplicate rows

    # isolating columns of interest, converting datatpes
    df = df.loc[:, ['Sample ID', 'Sample date/time', 'Viability(%)', 'Viable cells/ml (x10^6)']].copy()
    df = df.apply(pd.to_numeric, errors="ignore")
    df['Sample date/time'] = pd.to_datetime(df['Sample date/time'])
    df.rename(columns={
        "Sample date/time": "Vicell date/time",
        "Sample ID":"Vicell Sample ID"
    }, inplace=True)

    # Sorting data by date/time
    df.sort_values(by="Vicell date/time", inplace=True)  # sorting chronologically
    df.reset_index(inplace=True, drop=True)

    # Samples Dates range:
    min = df["Vicell date/time"].min()
    max = df["Vicell date/time"].max()
    print("Sample date range: " + str(datetime.datetime.date(min)) + " - " + str(datetime.datetime.date(max)))

    # Unique samples
    print("Unique sample ID's: " + str(df["Vicell Sample ID"].unique()))

    # Number of rows
    print("Total number of samples: " + str(df.shape[0]))

    return df

def flex_convert_csv():
    """
    Converts all .csv files in present working directory

    Return: Dictionary. Keys = filename.csv, values = Dataframe
    """

    #### Listing all files in directory ####
    files_list = listdir()  # list of all files in pwd
    L_csv = [i for i in files_list if i[-3:] == "csv"]  # isolating files that end in "xlsx"
    print("####   FlEX Import Report ####")
    print("\n")
    print("Total number of .csv files in dir: " + str(len(L_csv)))
    print("List of .csv files: " + str(L_csv))
    print("\n")

    #### importing all xlsx files into a list of dataframes and Running ViCell file verification ####

    # importing all .xlsx files into dataframes
    print("Converting .csv files into DataFrames: ")
    D_df = {}
    for i in L_csv:
        try:
            df = pd.read_csv(i)
            D_df[i] = df
            print(i + ": " + "CONVERTED")
        except:
            print("Failed to convert the following file into pandas dataframe: " + str(i))

    return D_df

def flex_check_format(D_df):
    """
    Checking for flex data format consitency, and removing non-bioreactor data points.

    Input: Dictionary of dataframes
    out: Dictionary of dataframes (bioreactor data), print statements
    """
    print("\n")
    print("#### FLEX Format Report ####")
    print("\n")
    print("Total files to verify: " + str(list(D_df.keys())))
    print("\n")

    # Selecting wanted and unwanted columns
    flex_columns = ['Sample ID', 'Date & Time', 'Gln', 'Glu', 'Gluc', 'Lac', 'NH4+', 'Na+', 'K+', 'Ca++', 'pH', 'PO2',
                    'PCO2', 'O2 Saturation', 'Osm', 'Vessel Temperature (°C)', 'Chemistry Dilution Ratio', 'HCO3']

    for key, df in D_df.items():
        clms_lst = list(df.columns)  # extracting df columns as list
        test_list = [x for x in flex_columns if x in set(clms_lst)]  # test list: every item if it exists as a column

        if test_list == flex_columns:
            df = df[flex_columns].copy()  # trashing all columns except desired ones
            # Parsing wanted and unwanted samples
            a = re.compile(
                "[Rr][0-9][0-9]")  # expression to capture, letter r or R, followed by 2 numbers, followed by anything else

            df_reject = df[~df["Sample ID"].str.match(a)].copy()  # ~ is the opposite of, rejected sample IDs
            df = df[df["Sample ID"].str.match(a)].copy()  # accepted sample ID's

            D_df[key] = df.copy()
            print(str(key) + "----------" + "Converted Succesfully")  # printing accepted and rejected sample ID's
            print("Accpeted unique sample IDs: " + str(df["Sample ID"].unique()))
            print("Rejected unique sample IDs: " + str(df_reject["Sample ID"].unique()))
            print("\n")

        else:
            print(str(key) + "---------" + "FAILED to convert dataframe")
            print("Either missing a column of data or column name has been changed")

    return D_df

def flex_merge(D_df):
    """
    Merging all dataframes in a dictionary, converting datatypes (datetime)

    Input: Dictionary of dataframes
    Return: dataframe with the following columns:

    ['Sample ID', "Flex date/time", 'Gln', 'Glu', 'Gluc', 'Lac', 'NH4+', 'Na+', 'K+', 'Ca++', 'pH', 'PO2',
    'PCO2', 'O2 Saturation', 'Osm', 'Vessel Temperature (°C)','Chemistry Dilution Ratio','HCO3']

    https://stackoverflow.com/questions/58401694/merge-pandas-time-series-datasets-on-numerically-nearest-index-full-outer-join
    """
    print("\n")
    print("#### FLEX Data Merge Report ####")
    print("\n")

    df = pd.concat(D_df.values(), ignore_index=True)  # merge all datafrmes
    df.drop_duplicates(subset='Date & Time', inplace=True)  # dropping duplicate rows

    # Changing to datetime dtypes
    df['Date & Time'] = pd.to_datetime(df['Date & Time'])

    # Sorting data by date/time
    df.sort_values(by='Date & Time', inplace=True)  # sorting chronologically
    df.reset_index(inplace=True, drop=True)


    # Renaming columns to make FLEX specific columns
    df.rename(columns={
        'Date & Time': "Flex date/time",
        "Sample ID" : "Flex Sample ID"
    },
              inplace=True)

    # Samples Dates range:
    min_ = df["Flex date/time"].min()
    max_ = df["Flex date/time"].max()
    print("Sample date range: " + str(datetime.datetime.date(min_)) + " - " + str(datetime.datetime.date(max_)))

    # Unique samples
    print("Unique sample ID's: " + str(df["Flex Sample ID"].unique()))

    # Number of rows
    print("Total number of samples: " + str(df.shape[0]))

    return df

def rename_flex_sample_id(dict_change, df):
    """
    Allows user to rename mislabled sample IDs.
    Changing lists of mislabaled sample IDs to correct value (dictionary key)

    INPUTS:
    dict_change -  dictionary. key = "R0012" (correct value), value = ["R00120", "R012", "R00112"]
    df - dataframe containing column "Sample ID". Values in this column will be changed.
    """
    for key, value in dict_change.items():
        id_match = df["Flex Sample ID"].isin(dict_change[key])
        index = df[id_match].index
        df.loc[index, "Flex Sample ID"] = key

    return df

def merge_vcl_flx(df_vcl, df_flx):
    """
    Joining vicell and flex dataframes. 2 merges are performed: merge_asof, followed by outer merge.
    The data is grouped by Sample ID, then joined by nearest timestamp.


    INPUT: df_vcl, dataframe must contain columns: Vicell Sample ID, Vicell date/time
           df_flx, dataframe must contain columns: Flex Sample ID, Flex date/time

    Output: merged dataframe
    """

    df_flx["Vicell Sample ID"] = df_flx["Flex Sample ID"].str.slice(0,
                                                                    5)  # adding column to match Vicell file by (shortened flex Sample ID)
    df_flx['Rank'] = df_flx['Flex date/time'].rank()  # dummy column for outer join

    # left join on Vicell dataframe. merge_asof allows merging by closest values. will need outer join to get remainng right df data.

    merged = pd.merge_asof(df_vcl, df_flx,
                           left_on="Vicell date/time",
                           right_on="Flex date/time",
                           direction="nearest",
                           by="Vicell Sample ID",
                           tolerance=pd.Timedelta("30 minutes"))

    # trmming down to only viCell columns from first merge, will use rank to do an outer merge with flex data
    columns_to_keep = ['Vicell Sample ID', 'Vicell date/time', 'Viability(%)', 'Viable cells/ml (x10^6)', 'Rank']
    merged = merged[columns_to_keep].copy()
    df_flx.drop('Vicell Sample ID', axis=1, inplace=True)  # dropping scafflold column
    merged = merged.merge(df_flx, on="Rank", how="outer").copy()

    # filling in Sample ID and date/time
    merged = merged.assign(Sample_ID=lambda x: x.filter(like="Sample ID").bfill(1).iloc[:, 0])
    merged = merged.assign(datetime=lambda x: x.filter(like="date/time").bfill(1).iloc[:, 0])

    # shortening Sample_ID to 5 characters
    merged["Sample_ID"] = merged["Sample_ID"].str.slice(0, 5)

    #Renaming Sample_ID back to Sample ID, (couldnt have spaces in assign)
    merged.rename(columns={"Sample_ID":"Sample ID"}, inplace=True)

    print("#### Merge Report ####")
    print("\n")
    print("Unique sample IDs: " + str(merged["Sample ID"].unique()))
    print("Total number of rows: " + str(merged.shape[0]))

    return merged

def calc_runtime(df):
    """
    Calculating runtime that is grouped by sample ID. Creates a new column in a dataframe: Runtime.
    dataframe must contain the following columns: Sample ID, datetime

    :param df:
    :return:
    """
    # Sorting dataframe chronologically
    df.sort_values(by="datetime", inplace=True)

    #### Adding Flex Runtime Column (limiting sample ID to first 5 characters: R####) ####
    df["Runtime"] = 0  # empty column with zeros
    for key, grp in df.groupby(["Sample ID"]):
        time_delta = grp["datetime"].diff()  # time difference
        time_delta = time_delta.dt.total_seconds() / (24 * 60 * 60)  # converting to float
        added_time = time_delta.cumsum()  # added time
        added_time.iloc[0] = 0  # setting the first value to zero instead of Nan

        ind = added_time.index

        df.loc[ind, "Runtime"] = added_time

    df["Titer"] = np.nan
    ordered_clms = ['Vicell Sample ID', 'Flex Sample ID',
                    'Vicell date/time', 'Flex date/time',

                    'Sample ID', 'datetime', "Runtime",

                    'Viable cells/ml (x10^6)', 'Viability(%)', "Titer",
                    'Gln', 'Glu', 'Gluc', 'Lac', 'NH4+', 'Na+', 'K+',
                    'Ca++', 'pH', 'PO2', 'PCO2', 'O2 Saturation', 'Osm',
                    'Vessel Temperature (°C)', 'Chemistry Dilution Ratio', 'HCO3', ]

    df = df[ordered_clms].copy()
    df.sort_values(by=["datetime"], inplace=True)
    df.reset_index(inplace=True, drop=True)

    df.rename(columns={
        'Viable cells/ml (x10^6)':"VCD",
        'Viability(%)': 'Viability'
    }, inplace=True)


    return df

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
