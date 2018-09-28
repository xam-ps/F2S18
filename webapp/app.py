# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import flask
import os

external_stylesheets = ['static/style.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

STATIC_PATH = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'static')


@app.server.route('/static/<resource>')
def serve_static(resource):
    return flask.send_from_directory(STATIC_PATH, resource)


app.layout = html.Div(children=[
    html.Meta(name='viewport', content='width=device-width, initial-scale=1.0'),
    html.Link(rel='shortcut icon', href='static/favicon.ico'),

    html.Div([
        html.Img(src='static/mechPandaProfile.png',
                 height='40', width='40', className='accountPic'),
        html.P('Adam Smith', className='accountName')
    ], className="account"),

    html.Div([
        html.Div(children='Slider', className='slider'),
        html.Div(children='Search', className='search'),
    ], className='header'),

    html.Div([
        html.Div([
            html.Div(
                dcc.Graph(
                    id='example-graph',
                    figure={
                        'data': [
                            {'x': [1, 2, 3], 'y': [4, 1, 2],
                             'type': 'bar', 'name': 'SF'},
                            {'x': [1, 2, 3], 'y': [2, 4, 5],
                             'type': 'bar', 'name': u'Montréal'},
                        ],
                        'layout': {
                            'title': 'Dash Data Visualization'
                        }
                    }
                ), className='test'),
        ], className='charts'),
        html.Div(children='Sidebar', className='sidebar'),
    ], className='main'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),
])

if __name__ == '__main__':
    app.run_server(debug=True)
