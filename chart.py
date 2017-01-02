# -*- coding: utf-8 -*-
# This set of functions is wrapping the plotly framework


import plotly.plotly as py
import plotly.graph_objs as go
import plotly


def print_chart(number_of_collaborations, occurrences):

    plotly.tools.set_credentials_file(username='riccardocandido', api_key='0k8sicv8yj')

    # Create and style traces
    trace0 = go.Scatter(
        x=number_of_collaborations,
        y=occurrences,
        name='A',
        line=dict(
            color='rgb(205, 12, 24)',
            width=4)
    )

    data = [trace0]

    # Edit the layout
    layout = go.Layout(title='Average High and Low Temperatures in New York',
                      xaxis=dict(
                      # type='log',
                      autorange=True,
                      title='Number of Collaborations'),
                      yaxis=dict(
                      # type='log',
                      autorange=True,
                      title='Counter'))

    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig)
