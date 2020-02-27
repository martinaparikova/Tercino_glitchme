# encoding=utf8

import pandas as pd
import datetime as dt
import column_list
import csv
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def create_csv(filename, targetpath, type):
    delimiter = '|'
    sheet = 0
    skip_rows = 1

    date_cols = []
    money_cols = []
    column_names = []
    drop_rows = []
    str_cols = []

    source_file_path = filename
    target_file_path = targetpath

    if type == 'zadatele':
        list_of_cols = column_list.zadatele_mhmp
    else:
        list_of_cols = column_list.zadatele_mhmp

    for col in list_of_cols:
        column_names.append(col[1])
        if col[3] == "money":
            money_cols.append(col[1])
        if col[3] == "date":
            date_cols.append(col[1])
        if col[3] == "str":
            str_cols.append(col[1])

    file_data = pd.read_excel(source_file_path, skiprows=skip_rows, names=column_names, sheet_name=sheet,
                              encoding='utf-8', keep_default_na=False)

    # cleaning data
    for column in file_data:
        # return numeric type for selected columns
        if column in money_cols:
            for rowindex, row in file_data.iterrows():
                pd.to_numeric(file_data.loc[rowindex, column])
        # delete rows with invalid date in selected columns (specific for airbnb data)
        if column in date_cols:
            for rowindex, row in file_data.iterrows():
                if str(file_data.loc[rowindex, column]).startswith('6') \
                        or file_data.loc[rowindex, column] > dt.datetime.now():
                    drop_rows.append(rowindex)
            file_data = file_data.drop(index=file_data.index[drop_rows])
        if column in str_cols:
            for rowindex, row in file_data.iterrows():
                file_data.loc[rowindex, column] = str(file_data.loc[rowindex, column].strip())
                # remove line endings inside fields
                file_data.loc[rowindex, column] = str(file_data.loc[rowindex, column]).replace('\n', '')

    # create csv
    file_data.to_csv(target_file_path, sep=delimiter, header=column_names, index=False,
                         quoting=csv.QUOTE_NONNUMERIC, encoding='utf-8-sig')
