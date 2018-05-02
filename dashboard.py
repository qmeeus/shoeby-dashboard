import dash
import plotly.graph_objs as go

from layout import size_hist_layout
from data import load_sales, prepare_size_dist

# TODO: How to include pyplot & seaborn plots in dash?
# TODO: Dynamic filters
# TODO: Check how to manage multiple graphs
# TODO: Add a second graph with the inventory levels
# TODO: Add a third graph with the sales history
# TODO: Source of inspiration: https://github.com/plotly/dash-oil-and-gas-demo
# TODO: Source of inspiration: https://dash.plot.ly/gallery

def main():
    sales = load_sales()
    app = dash.Dash()
    app.layout = size_hist_layout(sales, [("Brand", "EKS")])
    output = dash.dependencies.Output('indicator-graphic', 'figure')
    inputs = [dash.dependencies.Input('xaxis-column', 'value'),
              dash.dependencies.Input('xaxis-type', 'value'), ]

    @app.callback(output, inputs)
    def update_graph(xaxis_column_name, xaxis_type):
        x_data, y_data = prepare_size_dist(sales, Brand=xaxis_column_name, relative=xaxis_type)

        return {
            'data': [go.Bar(
                x=x_data,
                y=y_data,
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

    app.run_server(debug=True)


if __name__ == '__main__':
    main()
