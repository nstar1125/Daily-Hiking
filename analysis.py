from data_handler import setup_data, get_symbol_info
from datetime import datetime, timedelta
import numpy as np

def analyze_data(markets, m_symbols, stocks, s_symbols):
    cur_date = datetime.today().strftime("%Y-%m-%d")
    yesterday_date=(datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    markets_anlysis = []
    cur, avg = analyze_interst(markets[0])    
    i_anlysis = {}
    i_anlysis["name"]=m_symbols[0]
    i_anlysis["current_rate"]=cur
    i_anlysis["average_rate"]=avg
    markets_anlysis.append(i_anlysis)
    for i in range(1,len(m_symbols)):
        c1,c2,c1_date,c2_date = analyze_cross(markets[i])
        a, a_date = analyze_arrangement(markets[i])
        market_price, market_rate_change = calc_diff_rate(markets[i], yesterday_date, cur_date)
        _, c1_rate = calc_diff_rate(markets[i], c1_date, cur_date)
        _, c2_rate = calc_diff_rate(markets[i], c2_date, cur_date)
        _, a_rate = calc_diff_rate(markets[i], a_date, cur_date)
        m_anlysis = {}
        m_anlysis["name"]=m_symbols[i]
        m_anlysis["price"]=market_price
        m_anlysis["rate_change"]=market_rate_change
        m_anlysis["cross1"]=c1
        m_anlysis["cross1_date"]=c1_date
        m_anlysis["cross1_days"]=(datetime.today()-datetime.strptime(c1_date, "%Y-%m-%d")).days
        m_anlysis["cross1_rate"]=c1_rate
        m_anlysis["cross2"]=c2
        m_anlysis["cross2_date"]=c2_date
        m_anlysis["cross2_days"]=(datetime.today()-datetime.strptime(c2_date, "%Y-%m-%d")).days
        m_anlysis["cross2_rate"]=c2_rate
        m_anlysis["arrange"]=a
        m_anlysis["arrange_date"]=a_date
        m_anlysis["arrange_days"]=(datetime.today()-datetime.strptime(a_date, "%Y-%m-%d")).days
        m_anlysis["arrange_rate"]=a_rate
        markets_anlysis.append(m_anlysis)
    
    stocks_anlysis = []
    per_list = []
    pbr_list = []
    eps_list = []
    roe_list = []
    for i in range(len(s_symbols)):
        per, pbr, eps, roe = calc_value(symbol=s_symbols[i])
        per_list.append(per)
        pbr_list.append(pbr)
        eps_list.append(eps)
        roe_list.append(roe)
    avg_per = np.nanmean([value for value in per_list if value is not None])
    avg_pbr = np.nanmean([value for value in pbr_list if value is not None])
    avg_eps = np.nanmean([value for value in eps_list if value is not None])
    avg_roe = np.nanmean([value for value in roe_list if value is not None])
    for i in range(len(s_symbols)):
        per, pbr, eps, roe = calc_value(symbol=s_symbols[i])
        c1,c2,c1_date,c2_date = analyze_cross(stocks[i])
        a, a_date = analyze_arrangement(stocks[i])
        stock_price, stock_rate_change = calc_diff_rate(stocks[i], yesterday_date, cur_date)
        _, c1_rate = calc_diff_rate(stocks[i], c1_date, cur_date)
        _, c2_rate = calc_diff_rate(stocks[i], c2_date, cur_date)
        _, a_rate = calc_diff_rate(stocks[i], a_date, cur_date)
        s_anlysis = {}
        s_anlysis["name"]=s_symbols[i]
        s_anlysis["price"]=stock_price
        s_anlysis["rate_change"]=stock_rate_change
        s_anlysis["cross1"]=c1
        s_anlysis["cross1_date"]=c1_date
        s_anlysis["cross1_days"]=(datetime.today()-datetime.strptime(c1_date, "%Y-%m-%d")).days
        s_anlysis["cross1_rate"]=c1_rate
        s_anlysis["cross2"]=c2
        s_anlysis["cross2_date"]=c2_date
        s_anlysis["cross2_days"]=(datetime.today()-datetime.strptime(c2_date, "%Y-%m-%d")).days
        s_anlysis["cross2_rate"]=c2_rate
        s_anlysis["arrange"]=a
        s_anlysis["arrange_date"]=a_date
        s_anlysis["arrange_days"]=(datetime.today()-datetime.strptime(a_date, "%Y-%m-%d")).days
        s_anlysis["arrange_rate"]=a_rate
        s_anlysis["per"]=per
        s_anlysis["pbr"]=pbr
        s_anlysis["eps"]=eps
        s_anlysis["roe"]=roe
        s_anlysis["average_per"]=avg_per
        s_anlysis["average_pbr"]=avg_pbr
        s_anlysis["average_eps"]=avg_eps
        s_anlysis["average_roe"]=avg_roe
        stocks_anlysis.append(s_anlysis)

    return markets_anlysis, stocks_anlysis

def analyze_interst(ir_data):
    # 현재 금리
    cur_rate = ir_data['Close'].iloc[-1]
    # 평균 금리
    avg_rate = np.mean(ir_data['Close'])
    return cur_rate, avg_rate

def analyze_cross(data):
    cross_1 = True
    cross_2 = True
    last_cross_1=True
    last_cross_2=True
    last_cross_date_1 = None
    last_cross_date_2 = None

    for i in range(len(data)):
        if data['5MA'].iloc[i] > data['60MA'].iloc[i]:
            cross_1=True
        elif data['5MA'].iloc[i] < data['60MA'].iloc[i]:
            cross_1=False
        
        if data['5MA'].iloc[i] > data['120MA'].iloc[i]:
            cross_2=True
        elif data['5MA'].iloc[i] < data['120MA'].iloc[i]:
            cross_2=False
        
        if last_cross_1!=cross_1:
            last_cross_1=cross_1
            last_cross_date_1 = data.index[i].strftime("%Y-%m-%d")
        if last_cross_2!=cross_2:
            last_cross_2=cross_2
            last_cross_date_2 = data.index[i].strftime("%Y-%m-%d")
    cross1_type = "golden cross" if last_cross_1 else "dead cross"
    cross2_type = "golden cross" if last_cross_2 else "dead cross"
    
    return cross1_type, cross2_type, last_cross_date_1, last_cross_date_2

def analyze_arrangement(data):
    arrange = 0 #up: 1, default:0, down:-1
    last_arrange = 0
    last_arrange_date = None
    for i in range(len(data)):
        if data['5MA'].iloc[i] > data['20MA'].iloc[i] and data['20MA'].iloc[i] > data['60MA'].iloc[i]:
            arrange = 1
        elif data['5MA'].iloc[i] < data['20MA'].iloc[i] and data['20MA'].iloc[i] < data['60MA'].iloc[i]:
            arrange = -1
        else:
            arrange = 0
        if last_arrange != arrange:
            last_arrange=arrange
            last_arrange_date = data.index[i].strftime("%Y-%m-%d")
    if arrange == 1:
        arrange_state = "regular"
    elif arrange == 0:
        arrange_state = "changing"
    elif arrange == -1:
        arrange_state = "reverse"

    return arrange_state, last_arrange_date

def calc_diff_rate(data, date1, date2):
    i = 0
    while True:
        try:
            start_index = data.index.get_loc(date1)
            end_index = data.index.get_loc(date2)
            break
        except Exception as e:
            date1=(datetime.strptime(date1, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
            date2=(datetime.strptime(date2, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
            i=i+1
            if i>10:
                raise RuntimeError("주가 정보를 찾을 수 없습니다.")

    start_price = data['Close'].iloc[start_index]
    end_price = data['Close'].iloc[end_index]
    change_rate = (end_price / start_price) * 100 - 100
    return end_price, change_rate

def calc_value(symbol):
    per = get_symbol_info(symbol).get("trailingPE", None)
    pbr = get_symbol_info(symbol).get("priceToBook", None)
    eps = get_symbol_info(symbol).get("trailingEps", None) #주당순이익
    roe = get_symbol_info(symbol).get("returnOnEquity", None)
    return per, pbr, eps, roe


if __name__ == "__main__":
    markets, m_symbols, stocks, s_symbols = setup_data()
    markets_analysis, stocks_analysis = analyze_data(markets, m_symbols, stocks, s_symbols)