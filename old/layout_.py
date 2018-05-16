import dash_core_components as dcc
import dash_html_components as html
from controls_ import make_all_options_dynamic_filter


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
    page = html.Div(
        [
            title,
            selectors,
            graphs
        ],
        className='ten columns offset-by-one'
    )
    return page


def make_title(df, filters):
    title = html.Div(
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
    return title


def make_selectors(df, filters):

    all_options = make_all_options_dynamic_filter()

    right_list = html.Div(
        [dropdown(title, [None] + sorted(df[title].dropna().unique()), default)
         for title, default in filters],
        className='six columns'
    )

    left_list = html.Div(
        [dropdown("Adult Children", all_options, list(all_options.keys())[2]),
         html.Hr(),
         dropdown("Leg Torso", [], None, id='Legs-Torso-values'),
         html.Hr(),
         html.Div(id='display-selected-values')],
        className='six columns',

    )

    selectors = html.Div(
        [right_list, left_list],
        id="size_dist_selectors",
        # style={'width': '48%', 'display': 'inline-block'},
        className="row"
    )

    return selectors


def make_graphs():

    graph_wrapper = html.Div(
        [
            html.Div([size_distribution(), sales_history()], className="row"),
            html.Hr(),
            html.Div([inventory_history(), gaps()], className="row"),
        ]
    )

    return graph_wrapper


def dropdown(title, values, default, id='xaxis-column'):
    """
    Creates a simple div container with a title and a dropdown.
    The id is set to be used in dashboard_.py
    """

    dropdown = html.Div(
        [
            title,
            dcc.Dropdown(
                id=id,
                options=[{'label': i, 'value': i} for i in values],
                value=default)
        ]
    )

    return dropdown


def radio(title, values, default):
    """
    Creates a simple div container with a title and radio buttons
    The id is set to be used in dashboard_.py
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
    The id is set to be used in dashboard_.py
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


def gaps():
    return html.Div(
        [dcc.Graph(id='brand-gaps')],
        className='six columns',
        style={'margin-top': '20'}
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
