import pandas as pd
import plotly.graph_objs as go

from tools import filter_data
from controls import CATEGORIES, BRANDS
from layout import default_graph_layout


def display_category(selector):
    if selector == 'all':
        return list(CATEGORIES.keys())
    elif selector == 'Adult':
        return []
    else:
        return []


def display_brand(selector):
    if selector == 'all':
        return list(BRANDS.keys())
    elif selector == 'own_brand':
        return [brand for brand in BRANDS.keys() if brand.startswith("EK")]
    else:
        return []


def update_brand_text(data, brands, categories, month_slider):
    dff = filter_data(data, filter_many={"Brand": brands}, month_slider=month_slider)
    return "No of Wells: {}".format(dff.shape[0])


def size_distribution(inventory, categories, brands, month_slider):

    inventory = filter_data(inventory, filter_many={"Brand": brands}, month_slider=month_slider)

    stocks = inventory[(inventory["Sales"] == 0) & (inventory["NetQuantity"] > 0)]
    sales = inventory[inventory["Sales"] != 0]
    matenboog_stock = (stocks
                       .reset_index()
                       [["Size", "NetQuantity"]]
                       .groupby("Size")
                       .sum()
                       .apply(lambda x: x / float(x.sum()))
                       .rename(columns={"NetQuantity": "Inventory"})
                       )

    matenboog_sales = (sales
                       .reset_index()
                       [["Size", "Sales"]]
                       .groupby("Size")
                       .sum()
                       .apply(lambda x: x / float(x.sum()))
                       )

    matenboog = pd.concat([matenboog_stock, matenboog_sales], axis=1, join="outer").fillna(0)

    x_sales, y_sales = matenboog.index, matenboog["Sales"]
    x_inventory, y_inventory = matenboog.index, matenboog["Inventory"]

    traces = [
            go.Bar(
                x=x_sales,
                y=y_sales*100,
                text=list(map("{:02.2f}".format, y_sales*100)),
                textposition='auto',
                name='Sales'

            ), go.Bar(
                x=x_inventory,
                y=y_inventory*100,
                text=list(map("{:02.2f}".format, y_inventory*100)),
                textposition='auto',
                name='Stock levels',
                marker=dict(color='rgb(255, 125, 0)')
            )
        ]
    layout = default_graph_layout()
    layout["title"] = "Relative Size Distribution of Sales vs Stocks"
    # layout["margin"] = {'l': 40, 'b': 40, 't': 10, 'r': 0},

    return dict(data=traces, layout=layout)


def sales_history(sales, categories, brands, month_slider, frequency, relative):

    sales = filter_data(sales, filter_many={"Brand": brands}, month_slider=month_slider)
    sales = sales.groupby([pd.Grouper(freq=frequency), 'Size']).sum().reset_index()
    sales = sales.pivot(index="order_date", columns="Size", values="Quantity")  # , 'Quantity Returned'

    if 'True' in relative:
        sales = sales.apply(lambda s: s / s.sum(), axis=1)

    traces = [go.Bar(x=sales.index, y=sales[category], name=category) for category in sales.columns]

    layout = default_graph_layout()
    layout["barmode"] = 'stack'
    layout["title"] = "Sales History Including Size Distribution"

    return dict(
        data=traces,
        layout=layout)


def size_gap(inventory, categories, brands, month_slider):
    inventory = filter_data(inventory, filter_many={"Brand": brands}, month_slider=month_slider)

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

    matenboog["gap"] = matenboog["Inventory"] - matenboog["Sales"]
    gap_summary = matenboog.groupby(level=0).agg(lambda s: abs(s).sum())

    x_data, y_data = gap_summary.index, gap_summary["gap"]

    traces = [go.Bar(
        x=x_data,
        y=y_data,
        text=y_data,
        textposition='auto',
        marker=dict(color='rgb(255, 125, 0)')
    )]

    layout = default_graph_layout()
    layout['title'] = "Size Gap per Brand"

    return dict(data=traces, layout=layout)
