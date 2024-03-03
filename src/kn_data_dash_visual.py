# -*- coding: utf-8 -*-
"""
KN-Data-Dash-Visual

Step 5: Visualize KN-Data in Dash App

Author: Lukas Krabbe (mail@l-krabbe.de)

Copyright (c) 2023 Lukas Krabbe
"""
from datetime import date

import dash_auth
from dash import callback
from dash import Dash
from dash import dash_table
from dash import dcc
from dash import html
from dash import Input
from dash import Output
from helpers.db_connector import get_posgtres_connection

# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = {
    'lukaskrabbe': 'kn1'
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

def get_layout():
    return html.Div([
        html.H1('KN-Data Visualisation'),
        # dcc.Dropdown(['A', 'B'], 'A', id='dropdown'),
        dcc.DatePickerRange(
            id='date-picker',
            start_date='2024-01-01',
            end_date=date.today().strftime("%Y-%m-%d"),
            max_date_allowed=date.today().strftime("%Y-%m-%d"),
        ),
        dcc.Graph(id='graph'),
        html.H6('Last 10 days, for the selected period'),
        dash_table.DataTable(id='table'),
    ], className='container')

app.layout = get_layout()

def get_data(start_date, end_date):
    conn = get_posgtres_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT article_releasedate,
        CASE WHEN EXTRACT(DOW FROM article_releasedate) = 0 THEN 'Sunday'
            WHEN EXTRACT(DOW FROM article_releasedate) = 1 THEN 'Monday'
            WHEN EXTRACT(DOW FROM article_releasedate) = 2 THEN 'Tuesday'
            WHEN EXTRACT(DOW FROM article_releasedate) = 3 THEN 'Wednesday'
            WHEN EXTRACT(DOW FROM article_releasedate) = 4 THEN 'Thursday'
            WHEN EXTRACT(DOW FROM article_releasedate) = 5 THEN 'Friday'
            WHEN EXTRACT(DOW FROM article_releasedate) = 6 THEN 'Saturday'
            ELSE 'Unknown' END AS day,
        COUNT(*)
        FROM kn.dbt.stg_articles
        WHERE article_releasedate BETWEEN %s AND %s
        GROUP BY 1, 2
        ORDER BY 1 DESC
        """, (start_date, end_date)
    )
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

@callback(
    Output('table', 'data'),
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')],)
def update_table(start_date, end_date):
    data = get_data(start_date, end_date)
    # ALlow only last 10 days if more than 10 days are selected
    if len(data) > 10:
        data = data[:10]

    return [{'Date': x[0], 'Day': x[1], 'Count': x[2]} for x in data]


@callback(
    Output('graph', 'figure'),
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')],)
def update_graph(start_date, end_date):
    data = get_data(start_date, end_date)
    x = [x[0] for x in data]
    y = [x[2] for x in data]

    return {
        'layout': {
            'title': 'Number of articles per day, from ' +
                     start_date + ' to ' + end_date,
            'margin': {
                'l': 20,
                'b': 20,
                'r': 10,
                't': 60
            }
        },
        'data': [
            {
                'x': x,
                'y': y,
                'type': 'line'
            }
        ]
    }

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=9000)
