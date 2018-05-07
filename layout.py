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


def histogram():
    """
    Creates a histogram
    The id is set to be used in dashboard.py
    """
    return dcc.Graph(id='indicator-graphic')


def size_hist_layout(inventory, filters):
    """
    Create a div containers composed of filters and a histogram
    """
    # TODO: Create and organise the filters in config.py
    # TODO: Position of the dropdown vs. graphs in html/css
    # TODO: Make filters dynamic
    selectors = [dropdown(title, [None] + sorted(inventory[title].dropna().unique()), default)
                 for title, default in filters]

    selectors.append(radio('Linear', ['Absolute', 'Relative'], 'Absolute'))
    graph = histogram()
    return html.Div([
        html.Div(selectors,
                 id="size_dist_selectors",
                 style={'width': '48%', 'display': 'inline-block'},
                 ),
        graph])
