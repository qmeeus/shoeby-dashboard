import dash
from dash.dependencies import Input, Output

from data import load_sales, load_inventory
from layout import make_layout
import callbacks

# TODO: How to include pyplot & seaborn plots in dash?
# TODO: Dynamic filters
# TODO: Check how to manage multiple graphs
# TODO: Add a second graph with the inventory levels
# TODO: Add a third graph with the sales history
# TODO: Source of inspiration: https://github.com/plotly/dash-oil-and-gas-demo
# TODO: Source of inspiration: https://dash.plot.ly/gallery


def main():

    app = dash.Dash(__name__)
    app.css.append_css({
        'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'}
    )

    # Load the data
    sales = load_sales()
    # sales = group_brands(sales)
    inventory = load_inventory()

    # Create the dashboard
    app = dash.Dash()

    app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})  # noqa: E501

    app.layout = make_layout()

    # Create callbacks

    # Radio -> multi
    @app.callback(Output('categories', 'value'),
                  [Input('category_selector', 'value')])
    def display_category(selector):
        return callbacks.display_category(selector)

    # Radio -> multi
    @app.callback(Output('brands', 'value'),
                  [Input('brand_selector', 'value')])
    def display_brand(selector):
        return callbacks.display_brand(selector)
    
    @app.callback(Output('year_text', 'children'),
                  [Input('month_slider', 'value')])
    def update_year_text(month_slider):
        return callbacks.update_year_text(month_slider)
    
    # Selectors -> gap text
    @app.callback(Output('gap_text', 'children'),
                  [Input('categories', 'value'),
                   Input('brands', 'value'),
                   Input('month_slider', 'value')])
    def update_brand_text(categories, brands, month_slider):
        return callbacks.update_brand_text(inventory, categories, brands, month_slider)

    # Selectors -> production text
    @app.callback(Output('production_text', 'children'),
                  [Input('categories', 'value'),
                   Input('brands', 'value'),
                   Input('month_slider', 'value')])
    def update_production_text(categories, brands, month_slider):
        return callbacks.update_gap_text(inventory, categories, brands, month_slider)

    # Selectors -> matenboog
    @app.callback(Output('matenboog', 'figure'),
                  [Input('categories', 'value'),
                   Input('brands', 'value'),
                   Input('month_slider', 'value')])
    def size_distribution(categories, brands, month_slider):
        return callbacks.size_distribution(inventory, categories, brands, month_slider)

    # Selectors -> history
    @app.callback(Output('sales_history', 'figure'),
                  [Input('categories', 'value'),
                   Input('brands', 'value'),
                   Input('month_slider', 'value'),
                   Input('sample_frequency', 'value'),
                   Input('relative_selector', 'values')])
    def sales_history(categories, brands, month_slider, frequency, relative):
        return callbacks.sales_history(sales, categories, brands, month_slider, frequency, relative)

    # Selectors -> size gap
    @app.callback(Output('size_gap', 'figure'),
                  [Input('categories', 'value'),
                   Input('brands', 'value'),
                   Input('month_slider', 'value')])
    def size_gap(categories, brands, month_slider):
        return callbacks.size_gap(inventory, categories, brands, month_slider)

    # Selectors -> pie graph
    @app.callback(Output('pie_graph', 'figure'),
                  [Input('categories', 'value'),
                   Input('brands', 'value'),
                   Input('month_slider', 'value'),
                   Input('relative_selector', 'values')])
    def pie_graph(categories, brands, month_slider, relative_selector):
        return callbacks.pie_graph(sales, categories, brands, month_slider, relative_selector)

    app.run_server(debug=True)


if __name__ == '__main__':
    main()
