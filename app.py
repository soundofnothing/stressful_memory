import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from docarray import DocArray
from dash.exceptions import PreventUpdate

# Load the data from the persistent datastore or any other source
datastore_path = 'your_database_path'
doc_array = DocArray.load(datastore_path)

# Create a Dash app
app = dash.Dash(__name__)

# Define app layout
app.layout = html.Div(
    children=[
        html.H1("DocArray Data Visualization"),
        dcc.Loading(
            id="loading",
            type="circle",
            children=[
                html.Div(
                    children=[
                        dash_table.DataTable(
                            id="datatable",
                            columns=[{"name": col, "id": col} for col in doc_array.columns],
                            data=doc_array.get_dict(),
                            editable=True,
                            filter_action="native",
                            sort_action="native",
                        )
                    ]
                )
            ],
        ),
    ]
)


@app.callback(
    dash.dependencies.Output("datatable", "data"),
    [dash.dependencies.Input("datatable", "data_timestamp")],
)
def update_data(timestamp):
    """Update the data every 5 seconds"""
    if not timestamp:
        raise PreventUpdate

    # Load the updated data from the persistent datastore or any other source
    doc_array = DocArray.load(datastore_path)

    return doc_array.get_dict()


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
