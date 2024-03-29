import pandas as pd
import numpy as np


def filter_data(data, filter_many=None, filters=None, month_slider=None, categories=None):
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


def make_matenboog(inventory, sizes, brands, month_slider, groups):
    inventory = filter_data(inventory, filter_many={"Brand": brands}, month_slider=month_slider)
    stocks = inventory[(inventory["Sales"] == 0) & (inventory["NetQuantity"] > 0)]
    sales = inventory[inventory["Sales"] != 0]

    grouped_stocks = (
        stocks
        .reset_index()
        .loc[:, groups + ["NetQuantity"]]
        .groupby(groups)
        .sum()
        .apply(lambda x: x / x.sum())
        .rename(columns={"NetQuantity": "Inventory"})
    )

    grouped_sales = (
        sales
        .reset_index()
        .loc[:, groups + ["Sales"]]
        .groupby(groups)
        .sum()
        .apply(lambda x: x / x.sum())
    )

    matenboog = pd.concat([grouped_stocks, grouped_sales], axis=1, join='outer').fillna(0)

    return matenboog