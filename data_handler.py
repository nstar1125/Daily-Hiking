from datetime import datetime, timedelta
import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf
from config import load_config
import os

def initialize_data():
    data_cfg = load_config("data")
    today_date, one_month_date, three_months_date, one_year_date, ten_years_date = calculate_date()
    m_symbols = []
    markets = []
    s_symbols = []
    stocks = []
    for symbol in data_cfg["markets"]:
        temp_data = get_data(symbol, ten_years_date, today_date)
        add_moving_average(temp_data)
        m_symbols.append(symbol)
        markets.append(temp_data)
    for symbol in data_cfg["stocks"]:
        temp_data = get_data(symbol, ten_years_date, today_date)
        add_moving_average(temp_data)
        s_symbols.append(symbol)
        stocks.append(temp_data)
    return markets, m_symbols, stocks, s_symbols

def get_data(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)
    return data

def get_symbol_info(symbol):
    symbol_info = yf.Ticker(symbol)
    info = symbol_info.info
    return info

def add_moving_average(data):
    data['5MA'] = data['Close'].rolling(window=5).mean()
    data['20MA'] = data['Close'].rolling(window=20).mean()
    data['60MA'] = data['Close'].rolling(window=60).mean()
    data['120MA'] = data['Close'].rolling(window=120).mean()

def export_chart(data, symbol, period, type, start_date=None, end_date=None):
    if start_date is not None and end_date is not None:
        data = data.loc[start_date:end_date]
    ohlc = data[['Open', 'High', 'Low', 'Close']]
    ohlc.index.name = 'Date'

    # 스타일 설정
    style = mpf.make_mpf_style(base_mpl_style='default', rc={'axes.grid': False})
    
    # 상승은 빨강, 하강은 파랑으로 설정
    mc = mpf.make_marketcolors(up='red', down='blue', inherit=True)
    
    # 차트 스타일 및 색상 설정
    s = mpf.make_mpf_style(marketcolors=mc, base_mpl_style='default', rc={'axes.grid': False})

    if type=="stock":
        ylabel = 'Price (USD)'
    else:
        ylabel = 'index'
    fig, axlist = mpf.plot(ohlc, type='candle', title=f'{symbol} {type} Chart', ylabel=ylabel, show_nontrading=True, style=s, returnfig=True,
             addplot=[
            mpf.make_addplot(data['5MA'], color='green', secondary_y=False),
            mpf.make_addplot(data['20MA'], color='red', secondary_y=False),
            mpf.make_addplot(data['60MA'], color='purple', secondary_y=False),
            mpf.make_addplot(data['120MA'], color='orange', secondary_y=False),
        ])

    # 이미지 파일로 차트 저장
    cur_date = datetime.today().strftime("%Y-%m-%d")
    os.makedirs(f"log/charts/{cur_date}/{type}", exist_ok=True)
    chart_image_path = f"log/charts/{cur_date}/{type}/{cur_date}_{symbol}_{period}_{type}_chart.png"
    fig.savefig(chart_image_path, format='png')
    plt.close()

def calculate_date():
    today = datetime.today()
    one_month = today - timedelta(days=30)
    three_months = today - timedelta(days=30 * 3)
    one_year = today - timedelta(days=365.25)
    ten_years = today - timedelta(days=365.25 * 10)

    today_date = today.strftime("%Y-%m-%d")
    one_month_date = one_month.strftime("%Y-%m-%d")
    three_months_date = three_months.strftime("%Y-%m-%d")
    one_year_date = one_year.strftime("%Y-%m-%d")
    ten_years_date = ten_years.strftime("%Y-%m-%d")

    return today_date, one_month_date, three_months_date, one_year_date, ten_years_date

def setup_data():
    today_date, one_month_date, three_months_date, one_year_date, ten_years_date = calculate_date()
    start_dates = [one_month_date, three_months_date, one_year_date]
    
    markets, m_symbols, stocks, s_symbols = initialize_data()
    for date_index, start_date in enumerate(start_dates):
        if date_index == 0:
            period = "1M"
        elif date_index == 1:
            period = "3M"
        elif date_index == 2:
            period = "1Y"
        for symbol_index in range(len(s_symbols)):
            export_chart(stocks[symbol_index], s_symbols[symbol_index], period, "stock", start_date, today_date)
        for symbol_index in range(len(m_symbols)):
            export_chart(markets[symbol_index], m_symbols[symbol_index], period, "market", start_date, today_date)
    return markets, m_symbols, stocks, s_symbols

if __name__ == "__main__":
    setup_data()