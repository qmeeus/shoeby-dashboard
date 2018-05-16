import dash_html_components as html
import dash_core_components as dcc

from controls import SIZES, BRANDS, FREQUENCIES


def make_options(options_dict):
    return [{'label': str(options_dict[option]), 'value': str(option)}
            for option in options_dict]

def default_graph_layout():
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
        title='Title',
    )
    return layout.copy()

def make_layout():

    sampling_options = make_options(FREQUENCIES)
    size_options = [{'label': option, 'value': option} for option in SIZES]
    brand_options = make_options(BRANDS)

    layout = html.Div(
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
                        id='gap_text',
                        className='two columns',
                    ),
                    html.H5(
                        '',
                        id='production_text',
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
            html.Div(
                [
                    html.Div(
                        [html.P('Modify the summary frequency:'),
                         dcc.Dropdown(
                             id='sample_frequency',
                             options=sampling_options,
                             value="M"
                         )],
                        className='three columns'
                    ),
                    html.Div(
                        [html.P('Filter by month:'),
                         dcc.RangeSlider(
                            id='month_slider',
                            min=1,
                            max=12,
                            value=[1, 12]
                        )],
                    className='four columns'),
                    html.Div(
                        [dcc.Checklist(
                            id='relative_selector',
                            options=[{'label': 'Relative sales', 'value': 'True'}],
                            values=["True"])],
                        style = {'text-align': 'right'},
                        className='three columns'
                    )
                ],
                style={'margin-top': '20'},
                className='row'
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.P('Filter by product category:'),
                            dcc.RadioItems(
                                id='category_selector',
                                options=[
                                    {'label': 'All ', 'value': 'all'},
                                    {'label': 'Adult', 'value': 'adult'},
                                    {'label': 'Children ', 'value': 'kids'}
                                ],
                                value='all',
                                labelStyle={'display': 'inline-block'}
                            ),
                            dcc.Dropdown(
                                id='categories',
                                options=size_options,
                                multi=True,
                                value=[]
                            )
                        ],
                        className='six columns'
                    ),
                    html.Div(
                        [
                            html.P('Filter by product type:'),
                            dcc.RadioItems(
                                id='brand_selector',
                                options=[
                                    {'label': 'All ', 'value': 'all'},
                                    {'label': 'Own brand ', 'value': 'own_brand'},
                                    {'label': 'Custom ', 'value': 'custom'}
                                ],
                                value='all',
                                labelStyle={'display': 'inline-block'}
                            ),
                            dcc.Dropdown(
                                id='brands',
                                options=brand_options,
                                multi=True,
                                value=[]
                            )
                        ],
                        className='six columns'
                    ),
                ],
                className='row'
            ),
            html.Div(
                [
                    html.Div(
                        [
                            dcc.Graph(id='matenboog')
                        ],
                        className='six columns',
                        style={'margin-top': '20'}
                    ),
                    html.Div(
                        [
                            dcc.Graph(id='sales_history')
                        ],
                        className='six columns',
                        style={'margin-top': '20'}
                    ),
                ],
                className='row'
            ),
            html.Div(
                [
                    html.Div(
                        [
                            dcc.Graph(id='size_gap')
                        ],
                        className='four columns',
                        style={'margin-top': '10'}
                    ),
                    html.Div(
                        [
                            dcc.Graph(id='pie_graph')
                        ],
                        className='four columns',
                        style={'margin-top': '10'}
                    ),
                    html.Div(
                        [
                            dcc.Graph(id='aggregated_graph')
                        ],
                        className='four columns',
                        style={'margin-top': '10'}
                    ),
                ],
                className='row'
            ),
        ],
        className='ten columns offset-by-one'
    )
    return layout
