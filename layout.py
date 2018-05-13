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


def make_title(df, filters):
    return html.Div(
        [
            html.Div(
                [
                    html.H1(
                        'Shoeby Sales & Inventory - Overview',
                        className='eight columns',
                    ),
                    html.Img(
                        src="https://www.shoeby.nl/skin/frontend/shoeby/default/images/shoeby_logo.svg",
                        className='one columns',
                        style={
                            'height': '71',
                            'width': '170',
                            'float': 'right',
                            'position': 'relative',
                        },
                    ),
                ],
                className='row'
            ),
            html.Div(
                [
                    html.H5(
                        '',
                        id='inventory_text',
                        className='two columns'
                    ),
                    html.H5(
                        '',
                        id='gap_text',
                        className='eight columns',
                        style={'text-align': 'center'}
                    ),
                    html.H5(
                        '',
                        id='year_text',
                        className='two columns',
                        style={'text-align': 'right'}
                    ),
                ],
                className='row'
            ),
            make_selectors(df, filters)
        ]
    )


def make_selectors(df, filters):
    selectors = [dropdown(title, [None] + sorted(df[title].dropna().unique()), default)
     for title, default in filters]
    selectors.append(radio('Absolute or Relative', ['Absolute', 'Relative'], 'Absolute'))
    return html.Div(
        selectors,
        id="size_dist_selectors",
        style={'width': '48%', 'display': 'inline-block'}
    )


def make_graphs():
    size_dist = size_distribution()
    sales_hist = sales_history()
    inventory_level = inventory_history()
    return html.Div(
        [
            html.Div([size_dist, sales_hist], className="row"),
            html.Div([inventory_level], className="row"),
        ]
    )


def make_graph_layout(**kwargs):
    layout = dict(
        autosize=True,
        height=500,
        font=dict(color='#CCCCCC'),
        titlefont=dict(color='#CCCCCC', size='14'),
        margin=dict(
            l=35,
            r=35,
            b=35,
            t=45
        ),
        hovermode="closest",
        plot_bgcolor="#191A1A",
        paper_bgcolor="#020202",
        legend=dict(font=dict(size=10), orientation='h'),
        title='Satellite Overview',
    )
    for key, value in kwargs:
        layout[key] = value
    return layout


def build_page(inventory, filters):
    # TODO: Create and organise the filters in config.py
    # TODO: Position of the dropdown vs. graphs in html/css
    # TODO: Make filters dynamic
    """
    Create a div containers composed of filters and a histogram
    """

    # Add stylesheet
    dcc._css_dist[0]['relative_package_path'].append("resources/stylesheet.css")

    # Make the title
    title = make_title(inventory, filters)

    # Make the graphs
    graphs = make_graphs()

    # Return the whole layout
    return html.Div(
        [
            title,
            graphs
        ],
        className='ten columns offset-by-one'
    )
