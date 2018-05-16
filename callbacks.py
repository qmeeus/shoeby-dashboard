import pandas as pd
import plotly.graph_objs as go
import calendar

from tools import filter_data, make_matenboog
from controls import SIZES, BRANDS
from layout import default_graph_layout


# def display_category(selector):
#     if selector == 'all':
#         return SIZES
#     elif selector == 'Adult':
#         return []
#     else:
#         return []


def display_brand(selector):
    if selector == 'all':
        return list(BRANDS.keys())
    elif selector == 'own_brand':
        return [brand for brand in BRANDS.keys() if brand.startswith("EK")]
    else:
        return []


def update_brand_text(data, sizes, brands, month_slider):
    dff = filter_data(data, filter_many={"Brand": brands, "Size": sizes}, month_slider=month_slider)
    return "No of Products: {}".format(dff.shape[0])


def update_gap_text(inventory, sizes, brands, month_slider):
    matenboog = make_matenboog(inventory, sizes, brands, month_slider, ["Size"])

    def sum_squared(s): return (s**2).sum()
    def sum_absolute(s): return s.abs().sum()
    def sum_negative(s): return s[s < 0].sum()

    gap_summary = (
        (matenboog["Inventory"] - matenboog["Sales"])
        .groupby(level=0)
        .agg([sum_squared, sum_absolute, sum_negative])
        .sum()
    )
    print(gap_summary)
    return (f"Sum of Squared Differences {gap_summary['sum_squared']:.2f} "
            f"| Sum of Absolute Differences {gap_summary['sum_absolute']:.2f}")


def update_year_text(month_slider):
    months = [calendar.month_abbr[month] for month in month_slider]
    return "{} | {}".format(*months)


def size_distribution(inventory, sizes, brands, month_slider):

    matenboog = make_matenboog(inventory, sizes, brands, month_slider, ["Size"])

    x_sales, y_sales = matenboog.index, matenboog["Sales"]
    x_inventory, y_inventory = matenboog.index, matenboog["Inventory"]

    traces = [
            go.Bar(
                x=x_sales,
                y=y_sales,
                # text=list(map("{:.0%}".format, y_sales*100)),
                # textposition='auto',
                name='Sales'

            ), go.Bar(
                x=x_inventory,
                y=y_inventory,
                # text=list(map("{:.0%}".format, y_inventory)),
                # textposition='auto',
                name='Stock levels',
                marker=dict(color='rgb(255, 125, 0)')
            )
        ]
    layout = default_graph_layout()
    layout["title"] = "Relative Size Distribution of Sales vs Stocks"

    return dict(data=traces, layout=layout)


def sales_history(sales, sizes, brands, month_slider, frequency, relative):

    sales = filter_data(sales, filter_many={"Brand": brands}, month_slider=month_slider)
    sales = sales.groupby([pd.Grouper(freq=frequency), 'Size']).sum().reset_index()
    sales = sales.pivot(index="order_date", columns="Size", values="Quantity")  # , 'Quantity Returned'

    if 'True' in relative:
        sales = sales.apply(lambda s: s / s.sum(), axis=1)

    traces = [go.Bar(x=sales.index, y=sales[category], name=category) for category in sales.columns]

    layout = default_graph_layout()
    layout["barmode"] = 'stack'
    layout["title"] = "Sales History Including Size Distribution"

    return dict(data=traces, layout=layout)


def size_gap(inventory, sizes, brands, month_slider):
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
        # text=list(map("{:02.2f}%".format, y_data * 100)),
        # textposition='auto',
        marker=dict(color='rgb(255, 125, 0)')
    )]

    layout = default_graph_layout()
    layout['title'] = "Size Gap per Brand"

    return dict(data=traces, layout=layout)


def pie_graph(sales, sizes, brands, month_slider, relative_selector):
    sales = filter_data(sales, filter_many={'Brand': brands}, month_slider=month_slider)
    brand_group = sales.groupby('Brand').sum()
    size_group = sales.groupby('Size').sum()
    if "True" in relative_selector:
        brand_group = brand_group.apply(lambda x: x/x.sum(), axis=1)
        size_group = size_group.apply(lambda x: x/x.sum(), axis=1)

    data = [
        dict(
            type='pie',
            labels=list(brand_group.index),
            values=list(brand_group['Quantity'].values),
            name='Brand Breakdown',
            # text=['Total Gas Produced (mcf)', 'Total Oil Produced (bbl)', 'Total Water Produced (bbl)'],  # noqa: E501
            hoverinfo="value+percent",
            textinfo="label+percent+name",
            hole=0.5,
            # marker=dict(
            #     colors=['#fac1b7', '#a9bb95', '#92d8d8']
            # ),
            domain={"x": [0, .45], 'y': [0.2, 0.8]},
        ),
        dict(
            type='pie',
            labels=list(size_group.index),
            values=list(size_group['Quantity'].values),
            name='Size Breakdown',
            hoverinfo="label+text+value+percent",
            textinfo="label+percent+name",
            hole=0.5,
            # marker=dict(
            #     colors=[WELL_COLORS[i] for i in aggregate.index]
            # ),
            domain={"x": [0.55, 1], 'y': [0.2, 0.8]},
        )
    ]

    layout = default_graph_layout()
    layout['title'] = "Sales Repartition by Brand"
    layout['font'] = dict(color='#777777')
    layout['legend'] = dict(
        font=dict(color='#CCCCCC', size='10'),
        orientation='h',
        bgcolor='rgba(0,0,0,0)'
    )

    return dict(data=data, layout=layout)
