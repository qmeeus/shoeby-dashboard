import pandas as pd
import plotly.graph_objs as go

from tools import filter_data
from controls2 import CATEGORIES, BRANDS


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
                'title': categories,
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest',
        ),

    )
    return barplot

def sales_history(sales, categories, brands, month_slider, frequency):

    sales = filter_data(sales, filter_many={"Brand": brands}, month_slider=month_slider)
    sales = sales.resample(frequency).sum()
    print(sales.shape)
    print(sales.columns)

    # frequency = kwargs.get("frequency", SAMPLING)
    # y_data = kwargs.get("y_data")
    # if y_data:
    #     columns = FILTERS[list(map(lambda x: x[1], FILTERS)).index(y_data)][0]
    #     sales = sales.reset_index().pivot_table(index="order_date", columns=columns, values="Quantity", aggfunc="sum")
    # else:
    #     data = data["Quantity"]
    # data = data.resample(frequency).sum()
    # x_data, y_data = data.index, data.values
    #
    # data = [go.Bar(x=x_data, y=y_data)]
    # layout = go.Layout(
    #         xaxis={
    #             'title': "Sales history",
    #         },
    #         margin={'l': 40, 'b': 40, 't': 10, 'r': 0}
    #     )
    # return dict(data=data, layout=layout)
