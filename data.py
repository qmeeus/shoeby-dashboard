import os
import warnings
import pandas as pd
import datetime as dt
from pandas.api.types import CategoricalDtype

from config import *

# ----------------------------------------------------------------------------------------
#                            EXTRACT - TRANSFORM - LOAD
# ----------------------------------------------------------------------------------------


def build_sales():
    """
    Extract and transform sales dataset
    Operations:
        - Remove sending & payment fees
        - Groupby smallest granularity to aggregate the data
        - Aggregation by sum for Quantities & Returns
        - Filter the sizes to keep only letters (S, M, L, etc.)
    :return: sales dataframe
    """
    filename = join_path(RAW_SALES)
    exclude = ['Kosten verzending', 'AFTERPAY (WEB) Nerderland']

    def load_column_selection():
        with open(join_path(SALES_COLUMNS_SELECTION)) as f:
            return list(map(lambda t: t[1], [tuple(col.strip().split(', ')) for col in f.readlines()]))

    usecols = load_column_selection()
    sales = read_csv(filename, sep=",", encoding="latin-1", usecols=usecols)

    concat_date = lambda row: dt.datetime.combine(row['order_date'], row['order_time'])

    return (

        sales
        .dropna(how='all', axis=1)
        # .loc[:, usecols]
        .assign(
            order_date=pd.to_datetime(sales['Order Date']).dt.date,
            order_time=pd.to_datetime(sales['Order Time']).dt.time)
        .pipe(lambda df: df.assign(order_date=df.apply(concat_date, axis=1)))
        .drop(["Order Date", "Order Time", "order_time"], axis=1)
        .dropna(how='all', axis=1)
        .pipe(lambda df: df.where(~df.Description.isin(exclude)).dropna())
        .set_index("order_date")
        .groupby([pd.Grouper(freq=SAMPLING), "Horizontal Component Code"] + list(map(lambda x: x[0], FILTERS)))
        .aggregate({"Quantity": 'sum', "Quantity Returned": 'sum'})
        .reset_index()
        .set_index("order_date")
        .rename(columns={"Horizontal Component Code": "Size"})
        .pipe(filter_sizes)

    )


def build_inventory():
    # TODO: include original data tranformation
    # TODO: link to filters & config --> see how build_sales uses the values defined in config
    """
    Extract and transform inventory dataset
    Operations:
        - Remove unrelevant size --> Although this is done anyway at the end = to remove
        - Add the brand and collection using table items (left join) --> make sure in doc that default = left
        - Clean column items.ACACollection, merge product * merchandise code
        - Calculate the NetQuantity (without the sales = real stock delta)
        -  Filter the sizes to keep only letters (S, M, L, etc.)
    :return: inventory dataframe
    """
    final_column_selection = [
        'Opening Inventory',
        'Closing Inventory',
        'Quantity',
        'Sales',
        'NetQuantity'
    ]

    data = read_csv(join_path(RAW_INVENTORY), sep=",", encoding="latin-1")
    items = load_items()

    data = (
        data
            .where(~data["Size"].isin(('1', '1MT')))
            .dropna()
            .join(items, on="Item No_")
    )

    def convert_collection(s):
        try:
            return s.split("-")[0]
        except:
            return s

    return (

        data
        .assign(
            posting_date=pd.to_datetime(data["Posting Date"]),
            Season=data["ACACollection"].map(convert_collection),
            product_code=data["Merchandise Code"].combine_first(data["Product Group Code"]),
            Size=data["Size"].str.replace("3XL", "XXXL"),
            NetQuantity=data["Quantity"] + data["Sales"])
        .where(lambda df: df["NetQuantity"] != 0)
        .dropna()
        .drop(["Posting Date", "ACACollection", "Merchandise Code", "Product Group Code"], axis=1)
        .rename(columns={"product_code": "Merchandise Code", "ACABrand": "Brand"})
        .groupby(["posting_date", "Brand", "Item No_", "Size", "Color"])
        .agg({
            column: 'max' for column in final_column_selection})
        .reset_index()
        .set_index("posting_date")
        .pipe(filter_sizes)

    )


def load_items():
    selection = ['Item No_', 'Product Group Code', 'ACACollection', 'ACABrand']
    items = read_csv(join_path(RAW_ITEMS), sep=",", encoding="latin-1")
    return (

        items[selection]
            .drop_duplicates(subset=selection[:2])
            .loc[~(items["ACACollection"].str.endswith('M', na=False))]
            .set_index('Item No_')

    )


def load_sales():
    filename = "sales.csv"
    path = join_path(filename)
    if not os.path.exists(path):
        sales = build_sales()
        sales.to_csv(path)
        return sales
    return (
        pd.read_csv(path)
        .assign(order_date=lambda df: pd.to_datetime(df["order_date"]))
        .set_index("order_date")
    )


def load_inventory():
    filename = INVENTORY
    path = join_path(filename)
    if not os.path.exists(path):
        sales = build_inventory()
        sales.to_csv(path)
        return sales
    return (
        pd.read_csv(path)
        .assign(posting_date=lambda df: pd.to_datetime(df["posting_date"]))
        .set_index("posting_date")
    )

# ----------------------------------------------------------------------------------------
#                                      FILTERS
# ----------------------------------------------------------------------------------------


def filter_sizes(data):
    # Select relevant sizes
    sizes = ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL']
    column_name = "Size"
    categorical_size_type = CategoricalDtype(categories=sizes, ordered=True)
    data = data[data[column_name].isin(sizes)].copy()
    data[column_name] = data[column_name].astype(categorical_size_type)
    return data


def prepare_data(data, **kwargs):
    assert isinstance(data, pd.DataFrame)
    data = data.copy()

    start_date = kwargs.get("start_date", START_DATE)
    end_date = kwargs.get("end_date", END_DATE)

    filters = [

        ("Web Shop Code", kwargs.get("retailer")),
        ("Brand", kwargs.get("brand")),
        ("Season", kwargs.get("season")),
        ("Merchandise Code", kwargs.get("product_code"))

    ]

    simple_filter = lambda data, column, value: data[data[column] == value].copy()

    def filter_date(data, start_date=None, end_date=None):
        # Filter start date and end date
        data = data.copy()
        convert_date = lambda date: dt.datetime(date.year, date.month, date.day)
        if start_date:
            data = data[data.index >= convert_date(start_date)]
        if end_date:
            data = data[data.index <= convert_date(end_date)]
        return data

    # Filter out unwanted values
    # data = filter_date(data, start_date, end_date)
    #     data = filter_sizes(data)

    # for name, value in filters:
    #     if value is not None:
    #         data = simple_filter(data, name, value)

    return filter_data(data, **kwargs)


def filter_data(data, **kwargs):
    data = data.copy()
    for key, value in kwargs.items():
        if key in data.columns:
            data = data.loc[data[key] == value]

    return data


def prepare_size_dist(sales, inventory, **kwargs):
    output = []
    for i, df in enumerate([sales, inventory]):
        y_column = "Quantity" if not i else "NetQuantity"
        df = prepare_data(df, **kwargs)
        df = df[["Size", y_column]]
        grouped = df.groupby("Size").sum()
        output.append(grouped.index)
        output.append(grouped[y_column])

    return output


def prepare_sales_history(sales, **kwargs):
    data = prepare_data(sales, **kwargs)
    frequency = kwargs.get("frequency", SAMPLING)
    y_data = kwargs.get("y_data")
    if y_data:
        columns = FILTERS[list(map(lambda x: x[1], FILTERS)).index(y_data)][0]
        data = data.reset_index().pivot_table(index="order_date", columns=columns, values="Quantity", aggfunc="sum")
    else:
        data = data["Quantity"]
    data = data.resample(frequency).sum()
    return data.index, data.values

def prepare_inventory(data, **kwargs):
    data = filter_data(data, **kwargs)
    data = data[["Size", "NetQuantity"]]
    grouped = data.groupby("Size").sum()
    x_data = grouped.index
    y_data = grouped["NetQuantity"]

    return x_data, y_data

# ----------------------------------------------------------------------------------------
#                                       UTILS
# ----------------------------------------------------------------------------------------


def read_csv(filename, nrows=None, **csv_params):
    if nrows is not None:
        csv_params["nrows"] = nrows
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        return pd.read_csv(filename, **csv_params)


def join_path(filename):
    return os.path.join(DATA_DIR, filename)


# DEBUG
if __name__ == '__main__':
    inventory = load_inventory()
    # sales = load_sales()
    # x_sales, y_sales, x_inventory, y_inventory = prepare_size_dist(sales, inventory)
    # print(inventory.columns)
