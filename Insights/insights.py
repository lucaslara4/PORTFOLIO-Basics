import pandas as pd 
import numpy as np 
import yfinance as yf 
from datetime import datetime
import math
import plotly.express as px 
import plotly.graph_objects as go
from IPython.display import HTML

# List of tickers
tickers = ["MMM", "AMZN", "FDX", "GE", "HD", "PPL", "JNJ", "AAPL", "WMT", "MS"]

# Define start and end dates
start_date = "2024-01-01"
end_date = datetime.now().strftime("%Y-%m-%d")

# Download data for all tickers
df = yf.download(tickers, start=start_date, end=end_date, interval="1wk")

# Prices and Returns
M = len(df)
N = len(tickers)
Prices = np.zeros((M, N))

for i, t in enumerate(tickers):
    print("Downloading ticker", t)
    df_ticker = yf.download(t, start=start_date, end=end_date, interval="1wk")
    df_ticker = df_ticker.dropna()
    Prices[:, i] = df_ticker["Adj Close"]

# Calculate Returns
datelocation = df_ticker.index
P = pd.DataFrame(Prices, index=datelocation, columns=tickers)

P_aux = P.to_numpy()
diffP = np.diff(P_aux, n=1, axis=0)

rate_of_return = pd.DataFrame(diffP / P_aux[:-1, :], index=datelocation[1:], columns=tickers)

# Train set for analysis
t_inic = int(math.ceil(2 * M / 3))
r_train = rate_of_return.iloc[:t_inic - 1, :]

# Calculate mean, standard deviation, and correlation
u = 12 * r_train.mean()
sigma = math.sqrt(12) * r_train.std()
rho = r_train.corr()

# Add background gradient style to correlation matrix
styled_rho = rho.style.background_gradient(cmap="coolwarm")

# Include styled_rho in the DataFrame
df["Styled Correlation"] = styled_rho.render()

# Create a scatter plot with annotations
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=sigma,
    y=u,
    mode='markers',
    marker=dict(color='black'),
    text=tickers,
    name='Profitability/Risk'
))

for i in range(len(tickers)):
    fig.add_annotation(
        go.layout.Annotation(
            x=sigma[i],
            y=u[i],
            text=tickers[i],
            showarrow=True,
            arrowhead=5,
            ax=0,
            ay=-40
        )
    )

fig.update_layout(
    title="Profitability/Risk",
    xaxis_title="Volatility",
    yaxis_title="Profitability"
)

# Save the scatter plot as HTML
html_path_scatter = "scatter_plot.html"
fig.write_html(html_path_scatter)

# Save DataFrame as HTML with the styled correlation matrix
html_path = "output_table.html"
df.to_html(html_path, escape=False)

# Display the HTML in the notebook
HTML(filename=html_path)
