import dash
import plotly.graph_objs as go

from layout import build_page
from data import (
    load_sales,
    prepare_size_dist,
    load_inventory,
    prepare_inventory,
    prepare_sales_history
)


# TODO: How to include pyplot & seaborn plots in dash?
# TODO: Dynamic filters
# TODO: Check how to manage multiple graphs
# TODO: Add a second graph with the inventory levels
# TODO: Add a third graph with the sales history
# TODO: Source of inspiration: https://github.com/plotly/dash-oil-and-gas-demo
# TODO: Source of inspiration: https://dash.plot.ly/gallery


def main():
    # Load the data
    sales = load_sales()
    inventory = load_inventory()

    # Create the dashboard
    app = dash.Dash()

    app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})  # noqa: E501

    # Set the layout (HTML/CSS)
    app.layout = build_page(sales, [("Brand", "EKS")])

    # Define the outputs required by the callback function
    size_dist_output = dash.dependencies.Output('indicator-graphic', 'figure')
    sales_history_output = dash.dependencies.Output('sales', 'figure')
    inventory_output = dash.dependencies.Output('inventory-levels', 'figure')

    # Define the inputs required by the callback function
    inputs = [dash.dependencies.Input('xaxis-column', 'value'),
              dash.dependencies.Input('xaxis-type', 'value'), ]

    @app.callback(size_dist_output, inputs)
    def make_size_distribution(xaxis_column_name, xaxis_type):
        x_sales, y_sales, x_inventory, y_inventory = prepare_size_dist(sales, inventory, Brand=xaxis_column_name, relative=xaxis_type)

        return {
            'data': [go.Bar(
                x=x_sales,
                y=y_sales,
                name='Sales'
            ), go.Bar(
            x=x_inventory,
            y=y_inventory,
                name='StockLevels'
            )],

            'layout': go.Layout(
                xaxis={
                    'title': xaxis_column_name,
                    'type': 'Relative' if xaxis_type == 'Relative' else 'Absolute'
                },
                margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
                hovermode='closest'
            )
        }

    @app.callback(sales_history_output, inputs)
    def make_sales_history(xaxis_column_name, xaxis_type):
        x_data, y_data = prepare_sales_history(sales, Brand=xaxis_column_name, relative=xaxis_type)

        data = [go.Bar(x=x_data, y=y_data)]
        layout = go.Layout(
                xaxis={
                    'title': xaxis_column_name,
                    'type': 'Relative' if xaxis_type == 'Relative' else 'Absolute'
                },
                margin={'l': 40, 'b': 40, 't': 10, 'r': 0}
            )
        return dict(data=data, layout=layout)

    @app.callback(inventory_output, inputs)
    def make_inventory_level(xaxis_column_name, xaxis_type):
        x_inventory, y_inventory = prepare_inventory(inventory, Brand=xaxis_column_name, relative=xaxis_type)

        return {

            'data': [go.Bar(
                x=x_inventory,
                y=y_inventory,

            )
                      ],

            'layout': go.Layout(
                xaxis={
                    'title': xaxis_column_name,
                    'type': 'Relative' if xaxis_type == 'Relative' else 'Absolute'
                },
                margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
                hovermode='closest'
            )
        }

    # Run the server
    app.run_server(debug=True)


if __name__ == '__main__':
    main()
