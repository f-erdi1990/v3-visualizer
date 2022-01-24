import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objects as go

from helper import Sheets

# style & format
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# get data
data = Sheets("v3-optimizer-data").df
data["date"] = pd.to_datetime(data['timestamp'], unit='s')
# find unique poolIds and managers
list_pool_ids = data.poolId.unique()
list_managers = data.manager.unique()

list_pool_id_figs = []
for pool_id in list_pool_ids:
    temp_fig = go.Figure()
    token_0, token_1, fee = pool_id.split("_")
    token_0 = token_0.upper()
    token_1 = token_1.upper()
    title = "Uniswap V3 Pool: {} / {} @ {}% fee".format(token_0, token_1, fee)
    temp_fig.update_layout(title_text=title, title_x=0.5)
    for manager in list_managers:
        temp_df = data[(data["poolId"] == pool_id) & (data["manager"] == manager)].copy()
        if not temp_df.empty:
            temp_df = temp_df.reset_index(drop=True)
            temp_df.sort_values("date", inplace=True)
            temp_initial_price = temp_df['vaultTokenPrice'].iloc[0]
            temp_df["priceDev"] = temp_df["vaultTokenPrice"] / temp_initial_price
            temp_fig.add_trace(go.Scatter(x=temp_df['date'], y=temp_df['priceDev'], name=manager))
        else:
            pass
    list_pool_id_figs.append(temp_fig)


output = []
for idx, fig in enumerate(list_pool_id_figs):
    output.append(dcc.Graph(id=str(idx+1),
                            figure=fig
                            )
                  )

app.layout = html.Div(children=output)

if __name__ == "__main__":
    app.run_server(debug=True)
