### PORTFOLIO OPTIMIZATION -  STOCKS INFORMATION, CORRELATIONS AND PROFITABILITY/VOLATILITY

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
import math
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import webbrowser
import os

# List of tickers
tickers = ["NVDA", "AMZN", "META", "MELI", "COPEC.SN", "PPL", "SQM", "AAPL", "WMT", "MS"]

# Define start and end dates
start_date = "2023-01-01"
end_date = datetime.now().strftime("%Y-%m-%d")  # TODAY

# Download data for all tickers
df = yf.download(tickers, start=start_date, end=end_date, interval="1mo")

# Prices and Returns
M = len(df)
N = len(tickers)
Prices = np.zeros((M, N))

for i, t in enumerate(tickers):
    print("Downloading ticker", t)
    df_ticker = yf.download(t, start=start_date, end=end_date, interval="1mo")
    df_ticker = df_ticker.dropna()
    Prices[:, i] = df_ticker["Adj Close"]

# Returns:
datelocation = df_ticker.index
P = pd.DataFrame(Prices, index=datelocation, columns=tickers)

P_aux = P.to_numpy()
diffP = np.diff(P_aux, n=1, axis=0)

rate_of_return = pd.DataFrame(diffP / P_aux[:-1, :], index=datelocation[1:], columns=tickers)

# Train set for analysis:
t_inic = int(math.ceil(2 * M / 3))
r_train = rate_of_return.iloc[:t_inic - 1, :]

# Statistics of interest: Mean, standard deviation and correlation
u = 12 * r_train.mean()
sigma = math.sqrt(12) * r_train.std()
rho = r_train.corr()

# DataFrame as HTML
html_path_dataframe = "output_dataframe.html"
df.to_html(html_path_dataframe, escape=False)

column_sets = [['Adj Close'], ['Low', 'High'], ['Open', 'Close'], ['Volume']]

html_paths = []
for i, columns in enumerate(column_sets):
    df_subset = df[columns]
    html_path = f"output_dataframe_subset_{i}.html"
    df_subset.to_html(html_path, escape=False)
    html_paths.append(html_path)


print("HTML Paths:", html_paths)

combined_html = "combined_output_tables.html"
with open(combined_html, 'w') as f:
    for html_path in html_paths:
        with open(html_path, 'r') as subfile:
            f.write(subfile.read() + '<br><br>\n')

# Scatter:
fig_scatter = go.Figure()

fig_scatter.add_trace(go.Scatter(
    x=sigma,
    y=u,
    mode='markers',
    marker=dict(color='black'),
    text=tickers,
    name='Profitability/Risk'
))

for i in range(len(tickers)):
    fig_scatter.add_annotation(
        text=tickers[i],
        x=sigma[i],
        y=u[i],
        showarrow=True,
        arrowhead=5,
        ax=0,
        ay=-40
    )

fig_scatter.update_layout(
    title="Profitability/Risk",
    xaxis_title="Volatility",
    yaxis_title="Profitability"
)

# Correlation matrix:
fig_corr_matrix = make_subplots(rows=1, cols=1, subplot_titles=["Correlation Matrix"])
fig_corr_matrix.add_trace(go.Heatmap(z=rho.values, x=tickers, y=tickers, colorscale="Viridis"))

# Show figures and DataFrame:
fig_scatter.show()
fig_corr_matrix.show()

webbrowser.open('file://' + os.path.realpath(combined_html))
