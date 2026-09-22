# %%
%pip install pandas

import pandas as pd
import numpy as np
import datetime as dt
%pip install yfinance

import yfinance as yf

# %%
tataelxsi = yf.Ticker("TATAELXSI.NS")
tataelxsi.info


# %%
startdate = dt.datetime(2021,1,1)
enddate = dt.datetime(2026,9,21)

tataelxsi_df = tataelxsi.history(start = startdate, end = enddate)
tataelxsi_df


# %%
tataelxsi_df.drop(
    columns=['Dividends', 'Stock Splits'],
    errors='ignore',
    inplace=True
)

tataelxsi_df
tataelxsi_df

# %%
tataelxsi_df.isnull().sum()

# %%
tataelxsi_df.info()

# %%
tataelxsi_df['Daily Return'] = tataelxsi_df['Close'].pct_change(1) * 100
tataelxsi_df

# %%

tataelxsi_df['Daily Return'] = tataelxsi_df['Daily Return'].fillna(0)

tataelxsi_df

# %%
tataelxsi_df.describe().round(2)


# %%
%pip install matplotlib

import matplotlib.pyplot as plt

%pip install seaborn
import seaborn as sns

%pip install plotly

import plotly.express as px

# %%
tataelxsi_df.index = pd.to_datetime(tataelxsi_df.index).date
tataelxsi_df.index
tataelxsi_df = tataelxsi_df.reset_index()
tataelxsi_df.rename(columns={'index': 'Date'}, inplace=True)

# %%
tataelxsi_df

# %%
pip install --upgrade nbformat

# %%
import sys
import subprocess

subprocess.check_call([
    sys.executable,
    "-m",
    "pip",
    "install",
    "--upgrade",
    "nbformat"
])


# %%
import nbformat

print(nbformat.__version__)


# %%
import plotly.express as px

fig = px.line(
    title='Tata Elxsi Limited (TATAELXSI.NS) Closing Price [₹]'
)

fig.add_scatter(
    x=tataelxsi_df['Date'],
    y=tataelxsi_df['Close'],
    name='Close'
)

fig.show()

# %%
def plot_financial_data(df, title):
    
    fig = px.line(title = title)
    
    # For loop that plots all stock prices in the pandas dataframe df
    # Note that index starts with 1 because we want to skip the date column
    
    for i in df.columns[1:]:
        fig.add_scatter(x = df['Date'], y = df[i], name = i)

    fig.show()

# %%
plot_financial_data(tataelxsi_df.drop(['Volume', 'Daily Return'], axis = 1), 'Tata Elxsi Limited (TATAELXSI.NS) Stock Price [₹]')

# %%
plot_financial_data(tataelxsi_df.iloc[:,[0,5]], 'Tata Elxsi Limited (TATAELXSI.NS) Trading Volume')

# %%
plot_financial_data(tataelxsi_df.iloc[:,[0,6]], 'Tata Elxsi Limited (TATAELXSI.NS) Percentage Daily Return [%]')

# %%
def percentage_return_classifier(percentage_return):
    
    if percentage_return > -0.3 and percentage_return <= 0.3:
        return 'Insignificant Change'
    elif percentage_return > 0.3 and percentage_return <= 3:
        return 'Positive Change'
    elif percentage_return > -3 and percentage_return <= -0.3:
        return 'Negative Change'
    elif percentage_return > 3 and percentage_return <= 7:
        return 'Large Positive Change'
    elif percentage_return > -7 and percentage_return <= -3:
        return 'Large Negative Change'
    elif percentage_return > 7:
        return 'Bull Run'
    elif percentage_return <= -7:
        return 'Bear Sell Off'

# %%
tataelxsi_df['Trend'] = tataelxsi_df['Daily Return'].apply(percentage_return_classifier)
tataelxsi_df

# %%
trend_summary = tataelxsi_df['Trend'].value_counts()
trend_summary

# %%
plt.figure(figsize = (8, 8))
trend_summary.plot(kind = 'pie', y = 'Trend')

# %%
tataelxsi_df.set_index(['Date'], inplace = True)
tataelxsi_df

# %%
import sys
import subprocess

subprocess.check_call([
    sys.executable, "-m", "pip", "uninstall", "-y", "plotly"
])

subprocess.check_call([
    sys.executable, "-m", "pip", "install", "plotly==4.14.3"
])

# %%
import plotly
# Compatibility fix for NumPy 2.x and older Plotly/Cufflinks
if not hasattr(np, "bool8"):
    np.bool8 = np.bool_

import cufflinks

print("Plotly:", plotly.__version__)
print("Cufflinks:", cufflinks.__version__)

# %%
import cufflinks as cf

cf.go_offline()

figure = cf.QuantFig(
    tataelxsi_df,
    title='Tata Elxsi Limited (TATAELXSI) Candlestick Chart',
    name='TATAELXSI'
)

figure.add_sma(
    periods=[14, 21],
    column='Close',
    color=['magenta', 'green']
)

# Compatibility fix for older Cufflinks with newer pandas
if not hasattr(pd.DatetimeIndex, "format"):
    pd.DatetimeIndex.format = lambda self, *args, **kwargs: self.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

import plotly.graph_objects as go

plot = go.Figure()

plot.add_trace(go.Candlestick(
    x=tataelxsi_df.index,
    open=tataelxsi_df["Open"],
    high=tataelxsi_df["High"],
    low=tataelxsi_df["Low"],
    close=tataelxsi_df["Close"],
    name="TATAELXSI",
    increasing_line_color="green",
    decreasing_line_color="red"
))

plot.add_trace(go.Scatter(
    x=tataelxsi_df.index,
    y=tataelxsi_df["Close"].rolling(14).mean(),
    name="SMA 14",
    line=dict(color="magenta")
))

plot.add_trace(go.Scatter(
    x=tataelxsi_df.index,
    y=tataelxsi_df["Close"].rolling(21).mean(),
    name="SMA 21",
    line=dict(color="green")
))

plot.update_layout(
    title="Tata Elxsi Limited (TATAELXSI) Candlestick Chart",
    xaxis_rangeslider_visible=False
)

plot.show()

# %%
stocks_df = pd.read_csv('Multi_Stocks - Stocks.csv')
stocks_df = stocks_df.iloc[:-1]

stocks_df

# %%
daily_returns_df = stocks_df.iloc[:, 1:].pct_change() * 100
daily_returns_df.replace(np.nan, 0, inplace = True)
daily_returns_df

# %%
daily_returns_df.insert(0, "Date", stocks_df['Date'])
daily_returns_df

# %%
plot_financial_data(stocks_df, 'Stocks Closing Prices [$]')

# %%
plot_financial_data(daily_returns_df, 'Stocks Percentage Daily Returns [%]')

# %%
fig = px.histogram(daily_returns_df.drop(columns = ['Date']))
fig.update_layout({'plot_bgcolor': "white"})


# %%
plt.figure(figsize = (10, 8))
sns.heatmap(daily_returns_df.drop(columns = ['Date']).corr(), annot = True);

# %%
sns.pairplot(daily_returns_df);

# %%
def price_scaling(raw_prices_df):
    scaled_prices_df = raw_prices_df.copy()
    for i in raw_prices_df.columns[1:]:
          scaled_prices_df[i] = raw_prices_df[i]/raw_prices_df[i][0]
    return scaled_prices_df

# %%
price_scaling(stocks_df)


