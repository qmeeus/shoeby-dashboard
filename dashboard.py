import dash
import plotly.graph_objs as go

from layout import build_layout
from data import load_sales, prepare_size_dist

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

    # Create the dashboard
    app = dash.Dash()

    # Add stylesheet
    app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})

    # Set the layout (HTML/CSS)
    app.layout = build_layout(sales, [("Brand", "EKS")])

    # Define the outputs required by the callback function
    output = dash.dependencies.Output('indicator-graphic', 'figure')

    # Define the inputs required by the callback function
    inputs = [dash.dependencies.Input('xaxis-column', 'value'),
              dash.dependencies.Input('xaxis-type', 'value'), ]

    @app.callback(output, inputs)
    def update_graph(xaxis_column_name, xaxis_type):

        # Prepare the data
        x_data, y_data = prepare_size_dist(sales, Brand=xaxis_column_name, relative=xaxis_type)

        return {

            # Draw a simple bar chart
            'data': [go.Bar(
                x=x_data,
                y=y_data,
            )],

            # Specify the layout defined by the filters & other CSS attributes
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
