import os
import warnings
import pandas as pd
import datetime as dt
from pandas.api.types import CategoricalDtype
import plotly.graph_objs as go

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
        inventory = build_inventory()
        inventory.to_csv(path)
        return inventory
    return (
        pd.read_csv(path)
        .assign(posting_date=lambda df: pd.to_datetime(df["posting_date"]))
        .set_index("posting_date")
        .pipe(filter_sizes)
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
        if key in data.columns and value is not None:
            data = data.loc[data[key] == value]

    return data


def prepare_size_dist(inventory, **kwargs):
    inventory = filter_data(inventory, **kwargs)

    stocks = inventory[(inventory["Sales"] == 0) & (inventory["NetQuantity"] > 0)]
    sales = inventory[inventory["Sales"] != 0]
    matenboog_stock = (stocks
                       .reset_index()
                       [["Brand", "Size", "NetQuantity"]]
                       .groupby(["Brand", "Size"])
                       .sum()
                       .groupby("Brand")
                       .apply(lambda x: x / float(x.sum()))
                       .rename(columns={"NetQuantity": "Inventory"})
                       )

    matenboog_sales = (sales
                       .reset_index()
                       [["Brand", "Size", "Sales"]]
                       .groupby(["Brand", "Size"])
                       .sum()
                       .groupby("Brand")
                       .apply(lambda x: x / float(x.sum()))
                       )
    matenboog = pd.concat([matenboog_stock, matenboog_sales], axis=1, join="outer").fillna(0)
    if len(matenboog) == 0:
        return None, None
    gap_summary = matenboog.groupby(level=1).agg(lambda s: abs(s).sum())
    x_sales, y_sales = gap_summary.index, gap_summary["Sales"]
    x_inventory, y_inventory = gap_summary.index, gap_summary["Inventory"]
    return x_sales, y_sales, x_inventory, y_inventory


def size_dist_plot(brand, relative, inventory):
    x_sales, y_sales, x_inventory, y_inventory = prepare_size_dist(
        inventory,
        Brand=brand
    )
    barplot = dict(

        data=[
            go.Bar(
                x=x_sales,
                y=y_sales,
                text=y_sales,
                textposition='auto',
                name='Sales'

            ), go.Bar(
                x=x_inventory,
                y=y_inventory,
                text=y_inventory,
                textposition='auto',
                name='Stock levels',
                marker=dict(color='rgb(255, 125, 0)')
            )
        ],
        layout=go.Layout(
            xaxis={
                'title': brand,
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest',
        ),

    )
    return barplot


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


def prepare_gap_plot(inventory, **kwargs):
    inventory = filter_data(inventory, **kwargs)

    stocks = inventory[(inventory["Sales"] == 0) & (inventory["NetQuantity"] > 0)]
    sales = inventory[inventory["Sales"] != 0]
    matenboog_stock = (stocks
                       .reset_index()
                       [["Brand", "Size", "NetQuantity"]]
                       .groupby(["Brand", "Size"])
                       .sum()
                       .groupby("Brand")
                       .apply(lambda x: x / float(x.sum()))
                       .rename(columns={"NetQuantity": "Inventory"})
                       )

    matenboog_sales = (sales
                       .reset_index()
                       [["Brand", "Size", "Sales"]]
                       .groupby(["Brand", "Size"])
                       .sum()
                       .groupby("Brand")
                       .apply(lambda x: x / float(x.sum()))
                       )
    matenboog = pd.concat([matenboog_stock, matenboog_sales], axis=1, join="outer").fillna(0)
    if len(matenboog) == 0:
        return None, None
    matenboog["gap"] = matenboog["Inventory"] - matenboog["Sales"]
    gap_summary = matenboog.groupby(level=0).agg(lambda s: abs(s).sum())

    x_data, y_data = gap_summary.index, gap_summary["gap"]
    return x_data, y_data


def gap_plot(brand, relative, inventory):
    x_data, y_data = prepare_gap_plot(
        inventory,
        Brand=brand
    )

    barplot = dict(

        data=[
            go.Bar(
                x=x_data,
                y=y_data,
                text=y_data,
                textposition='auto',
                marker=dict(color='rgb(255, 125, 0)')
            )
        ],
        layout=go.Layout(
            xaxis={
                'title': brand,
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest',
        ),

    )
    return barplot


# Added by Wesley
def load_brand(brand):
    with open('./BrandBin/' + brand + '.txt') as f:
        return [col.split(', ') for col in f.readlines()][0]


def replace_brand(brand):
    brand_name = brand.upper()
    return {e: brand_name for e in load_brand(brand)}


def group_brands(df):
    brands = ['cu','jill','blend','veromoda','clt', 'sense', 'eksept', 'refill']
    for i in range(len(brands)):
        df.Brand = df.Brand.replace(replace_brand(brands[i]))
    return df

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
    # concat_brand_gaps(sales, inventory)
    # x_sales, y_sales, x_inventory, y_inventory = prepare_size_dist(sales, inventory)
    # print(inventory.columns)




# def prepare_gaps(data, **kwargs):
#     data = filter_data(data, **kwargs)
#     data = data[["Size", "Brand", "Quantity"]]
#     grouped = data.groupby(["Brand", "Size"]).sum()
#     return grouped
#
#
# def concat_brand_gaps(sales, inventory):
#     print(0)
#     sales = sales.rename(columns={"Quantity": "Out"})
#     inventory = inventory.rename(columns={"Quantity": "In"})
#     print(1)
#     data = pd.concat([inventory, sales], join='outer', axis=1).fillna(0)
#     print(2)
#     data = data[data['In'] > 0]
#     data2 = data.groupby(level=0).apply(lambda x: x['In'] / float(x['In'].sum()))
#     data3 = data.groupby(level=0).apply(lambda x: x['Out'] / float(x['Out'].sum()))
#     data2, data3 = pd.DataFrame(data2), pd.DataFrame(data3)
#     data = pd.concat([data2, data3], join='outer', axis=1).fillna(0)
#     print(data.columns)
#     data['gap'] = abs(data['In'] - data['Out'])
#     # data = data.groupby('Brand').sum().sort_values('gap', ascending=False)
#     data = data.groupby('Brand').agg({'gap': 'sum'}).sort_values('gap', ascending=False)
#
#     x_data = data.index
#     y_data = data['gap']
#     return x_data, y_data
