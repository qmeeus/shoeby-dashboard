import dash
from dash.dependencies import Input, Output
import plotly.graph_objs as go

from layout_ import build_page
from data import (
    load_sales,
    size_dist_plot,
    load_inventory,
    prepare_inventory,
    prepare_sales_history,
    gap_plot,
    group_brands
)
from controls_ import make_all_options_dynamic_filter


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
    sales = group_brands(sales)
    inventory = load_inventory()

    # Create the dashboard
    app = dash.Dash()

    app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})  # noqa: E501

    # Set the layout (HTML/CSS)
    app.layout = build_page(sales, [("Brand", "EKS")])

    #Importing the dynamic dropdown
    all_options = make_all_options_dynamic_filter()

    # Define the outputs required by the callback function
    size_dist_output = Output('indicator-graphic', 'figure')
    sales_history_output = Output('sales', 'figure')
    inventory_output = Output('inventory-levels', 'figure')
    brand_gaps_output = Output('brand-gaps', 'figure')

    # Define the inputs required by the callback function
    inputs = [Input('xaxis-column', 'value'),
              Input('xaxis-type', 'value'), ]

    @app.callback(size_dist_output, inputs)
    def make_size_distribution(xaxis_column_name, xaxis_type):
        return size_dist_plot(xaxis_column_name, xaxis_type, inventory)


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
                name='Stock levels1',
                marker=dict(
                    color='rgb(255, 125, 0)'
                )


            )

                      ],


            'layout': go.Layout(
                xaxis={
                    'title': xaxis_column_name,
                    'type': 'Relative' if xaxis_type == 'Relative' else 'Absolute'
                },
                margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
                hovermode='closest',


            )
        }


    @app.callback(brand_gaps_output, inputs)
    def update_graph_inventory(xaxis_column_name, xaxis_type):
        return gap_plot(xaxis_column_name, xaxis_type, inventory)


    @app.callback(
        Output('Boys-Girl-dropdown', 'options'),
        [Input('Adult-Children-dropdown', 'value')])
    def set_collection(selected_collection):
        return [{'label': i, 'value': i} for i in all_options[selected_collection]]

    @app.callback(
        Output('Legs-Torso-values', 'options'),
        [Input('Boys-Girl-dropdown', 'value')])
    def set_boy_girl(selected_boy_girl):
        selected_collection = [i for i in all_options.keys() for f in all_options[i] if f == selected_boy_girl]
        return [{'label': i, 'value': i} for i in all_options[selected_collection[0]][selected_boy_girl]]

        # return [[{'label': k, 'value': k} for i in all_options.keys() for k in all_options[available_option].keys()]]

    @app.callback(
        Output('Legs-Torso-values', 'value'),
        [Input('Legs-Torso-values', 'options')])
    def set_cities_value(available_option):
        return [available_option[0]['value']][0]

    @app.callback(
        Output('display-selected-values', 'children'),
        [Input('Adult-Children-dropdown', 'value'),
         Input('Boys-Girl-dropdown', 'value'),
         Input('Legs-Torso-values', 'value')])
    def set_display_children(selected_collection=None, selected_boy_girl=None, selected_leg_torso=None):
        if selected_collection == 'OverAll':
            return 'You are displaying Over All'
        return u'{} -  {} - {}'.format(
            selected_collection, selected_boy_girl, selected_leg_torso
        )

    # Run the server
    app.run_server(debug=True)


if __name__ == '__main__':
    main()