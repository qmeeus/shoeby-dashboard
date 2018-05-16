import pandas as pd
import numpy as np


def filter_data(data, filter_many=None, filters=None, month_slider=None):
    data = data.copy()

    if month_slider is not None:
        min, max = month_slider
        mask = pd.Series(data.index, index=data.index)
        data = data.loc[(mask.dt.month >= min) & (mask.dt.month <= max)]

    if filter_many is not None:
        for column, values in filter_many.items():
            data = data.loc[data[column].isin(values)]

    if filters is not None:
        for key, value in filters.items():
            if key in data.columns and value is not None:
                data = data.loc[data[key] == value]

    return data
