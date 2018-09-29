import plotly.graph_objs as go
import dash_core_components as dcc


def get_avg_distance_chart():

    layout=go.Layout(title="Avg Distance per Car", 
                    xaxis={'title':'x1'},
                    yaxis={'title':'x2'})


    trace2=go.Scatter(x=['5. Aug', '6. Aug','7. Aug','8. Aug','9. Aug'], y=[298.0, 93.0, 155.0, 153.0, 78.0])

    data=go.Data([trace2])
    figure=go.Figure(data=data,layout=layout)

    return dcc.Graph(
            id='avg_distance',
            figure={
            'data': data,
            'layout': layout
        })