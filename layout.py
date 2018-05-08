import dash_core_components as dcc
import dash_html_components as html


def dropdown(title, values, default):
    """
    Creates a simple div container with a title and a dropdown.
    The id is set to be used in dashboard.py
    """
    # TODO: format title
    return html.Div([
        title,
        dcc.Dropdown(
            id='xaxis-column',
            options=[{'label': i, 'value': i} for i in values],
            value=default)
    ])


def radio(title, values, default):
    """
    Creates a simple div container with a title and radio buttons
    The id is set to be used in dashboard.py
    """
    # TODO: format title
    return html.Div([
        html.Div(title, style={}),
        dcc.RadioItems(
            id='xaxis-type',
            options=[{'label': i, 'value': i} for i in values],
            value=default,
            labelStyle={'display': 'inline-block'})
    ])


def size_distribution():
    """
    Creates a histogram
    The id is set to be used in dashboard.py
    """
    return html.Div(
        [dcc.Graph(id='indicator-graphic')],
        className='six columns',
        style={'margin-top': '20'}
    )


def sales_history():
    return html.Div(
        [dcc.Graph(id='sales')],
        className='six columns',
        style={'margin-top': '20'}
    )


def inventory_history():
    return html.Div(
        [dcc.Graph(id='inventory-levels')],
        className='six columns',
        style={'margin-top': '20'}
    )


def make_title():
    return html.Div(
        [
            html.H1(
                'Shoeby Sales & Inventory - Overview',
                className='eight columns',
            ),
            html.Img(
                src="https://www.shoeby.nl/skin/frontend/shoeby/default/images/shoeby_logo.svg",
                className='one columns',
                style={
                    'height': '100',
                    'width': '225',
                    'float': 'right',
                    'position': 'relative',
                },
            ),
        ],
        className='row'
    )


def build_layout(inventory, filters):
    # TODO: Create and organise the filters in config.py
    # TODO: Position of the dropdown vs. graphs in html/css
    # TODO: Make filters dynamic
    # TODO: How to make className effective (css)
    """
    Create a div containers composed of filters and a histogram
    """

    # Add stylesheet
    dcc._css_dist[0]['relative_package_path'].append("resources/stylesheet.css")

    # Make the title
    title = make_title()

    # Make the selectors
    selectors = [dropdown(title, [None] + sorted(inventory[title].dropna().unique()), default)
                 for title, default in filters]
    selectors.append(radio('Linear', ['Absolute', 'Relative'], 'Absolute'))

    # Make the graphs
    size_dist = size_distribution()
    sales_hist = sales_history()
    inventory_level = inventory_history()

    graphs = html.Div(
        [
            html.Div([size_dist, sales_hist], className="row"),
            html.Div([inventory_level], className="row"),
        ]
    )

    # Return the whole layout
    return html.Div(
        [
            title,
            html.Div(selectors,
                     id="size_dist_selectors",
                     style={'width': '48%', 'display': 'inline-block'},
                     ),
            graphs
        ],
        className='ten columns offset-by-one'
    )
