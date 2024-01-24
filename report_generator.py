from datetime import datetime
from fpdf import FPDF
from data_handler import setup_data, get_symbol_info
from analysis import analyze_data
import os

blue = (58, 176, 255)
red = (248, 166, 166)
white = (255, 255, 255)
grey = (238, 237, 237)

class ReportGenerator:
    def __init__(self, 
                 title,
                 date,
                 m_a,
                 s_a,
                 img_dir
                 ):
        self.title = title
        self.date = date
        self.markets_analysis = m_a
        self.stocks_analysis = s_a
        self.image_dir = img_dir

    def line(self, pdf):
        pdf.set_fill_color(*grey)
        pdf.cell(190, 2, txt="", ln=True, fill=True)
        pdf.ln(5)
    def head(self, pdf):
        pdf.set_font("Arial", "B", size=30) #타이틀
        pdf.cell(200, 10, txt=self.title, ln=True, align='C')        
        pdf.ln(5)
        pdf.set_font("Arial", size=12) #날짜
        pdf.cell(190, 10, txt=f"Date: {self.date}", ln=True, align='R')
    def subtitle1(self, pdf, txt):
        pdf.set_font("Arial", "B", size=20)
        pdf.cell(200, 10, txt=txt, ln=True)
        self.line(pdf)
        pdf.ln(5)
    def subtitle2(self,pdf,txt):
        pdf.set_font("Arial", "B", size=16)
        pdf.cell(200, 10, txt=txt, ln=True)
    def subtitle3(self,pdf,txt):
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=txt, ln=True)
    def add_charts(self,pdf, symbol, type):
        if pdf.get_y()+50>290:
                pdf.add_page()
        pdf.image(self.image_dir+f"{type}/{self.date}_{symbol}_1M_{type}_chart.png", x=10, y=pdf.get_y(), w=60, h=0)
        pdf.image(self.image_dir+f"{type}/{self.date}_{symbol}_3M_{type}_chart.png", x=70, y=pdf.get_y(), w=60, h=0)
        pdf.image(self.image_dir+f"{type}/{self.date}_{symbol}_1Y_{type}_chart.png", x=130, y=None, w=60, h=0)
        pdf.ln(5)
    def add_interest_table(self,pdf):
        cur_ir = self.markets_analysis[0]["current_rate"]
        avg_ir = self.markets_analysis[0]["average_rate"]
        pdf.set_fill_color(*grey)
        pdf.cell(40, 10, txt="", ln=False, border=1, align='C', fill=True)
        pdf.cell(65, 10, txt="Current", ln=False, border=1, align='C', fill=True)
        pdf.cell(65, 10, txt="Average", ln=False, border=1, align='C', fill=True)
        pdf.cell(20, 10, txt="Trend", ln=True, border=1, align='C', fill=True)
        pdf.cell(40, 10, txt=" Interest Rate:", ln=False, border=1, align='L')
        pdf.cell(65, 10, txt=f" {cur_ir:.2f}%", ln=False, border=1, align='C')
        pdf.cell(65, 10, txt=f" {avg_ir:.2f}%", ln=False, border=1, align='C')
        fill_color = red if cur_ir<avg_ir else blue if cur_ir>avg_ir else white
        pdf.set_fill_color(*fill_color)
        pdf.cell(20, 10, txt="up" if cur_ir<avg_ir else "down" if cur_ir>avg_ir else "-" , ln=True, border=1, align='C', fill=True)
        pdf.ln(5)
    def add_interest_report(self,pdf):
        cur_ir = self.markets_analysis[0]["current_rate"]
        avg_ir = self.markets_analysis[0]["average_rate"]
        pdf.multi_cell(0, 10, txt=f"Today's interest rate is {cur_ir:.2f}%")
        if cur_ir > avg_ir:
            pdf.multi_cell(0, 10, 
                           txt="Current interest rate is higher than average, " \
                            "which means market is likely to be trending downward.")
        elif cur_ir < avg_ir:
            pdf.multi_cell(0, 10, 
                           txt="Current interest rate is lower than average, " \
                            "which means market is likely to be trending upward." \
                            "Also there can be economic depression.")
        else:
            pdf.multi_cell(0, 10, 
                           txt="Current interest rate is equal to average.")
        pdf.ln(5)
    def add_trend_table(self, pdf, type, idx):
        if type == "market":
            analysis = self.markets_analysis[idx]
        elif type == "stock":
            analysis = self.stocks_analysis[idx]
        else:
            raise("Unvalid input.")
        c1 = analysis["cross1"]
        c1ds = analysis["cross1_days"]
        c1dt = analysis["cross1_date"]
        c1rt = analysis["cross1_rate"]
        c2 = analysis["cross2"]
        c2ds = analysis["cross2_days"]
        c2dt = analysis["cross2_date"]
        c2rt = analysis["cross2_rate"]
        ar = analysis["arrange"]
        ards = analysis["arrange_days"]
        ardt = analysis["arrange_date"]
        arrt = analysis["arrange_rate"]

        pdf.set_fill_color(*grey)
        pdf.cell(45, 10, txt="", ln=False, border=1, align='L', fill=True) 
        pdf.cell(35, 10, txt="State", ln=False, border=1, align='C', fill=True)
        pdf.cell(60, 10, txt="Days passed", ln=False, border=1, align='C', fill=True)
        pdf.cell(30, 10, txt="Rate", ln=False, border=1, align='C', fill=True)
        pdf.cell(20, 10, txt="Trend", ln=True, border=1, align='C', fill=True)
        
        pdf.cell(45, 10, txt=" Cross1 (5,60MA):", ln=False, border=1, align='L')
        pdf.cell(35, 10, txt=c1, ln=False, border=1, align='C')
        pdf.cell(60, 10, txt=f"{c1ds} days ({c1dt})", ln=False, border=1, align='C')
        pdf.cell(30, 10, txt=f"{c1rt:.2f}%", ln=False, border=1, align='C')
        fill_color = red if c1=="golden cross" else blue
        pdf.set_fill_color(*fill_color)
        pdf.cell(20, 10, txt="up" if c1=="golden cross" else "down", ln=True, border=1, align='C', fill=True)
        
        pdf.cell(45, 10, txt=" Cross2 (5,120MA):", ln=False, border=1, align='L')
        pdf.cell(35, 10, txt=c2, ln=False, border=1, align='C')
        pdf.cell(60, 10, txt=f"{c2ds} days ({c2dt})", ln=False, border=1, align='C')
        pdf.cell(30, 10, txt=f"{c2rt:.2f}%", ln=False, border=1, align='C')
        fill_color = red if c2=="golden cross" else blue
        pdf.set_fill_color(*fill_color)
        pdf.cell(20, 10, txt="up" if c2=="golden cross" else "down", ln=True, border=1, align='C', fill=True)
        
        pdf.cell(45, 10, txt=" Arrange (5,20,60MA):", ln=False, border=1, align='L',)
        pdf.cell(35, 10, txt=ar, ln=False, border=1, align='C')
        pdf.cell(60, 10, txt=f"{ards} days ({ardt})", ln=False, border=1, align='C')
        pdf.cell(30, 10, txt=f"{arrt:.2f}%", ln=False, border=1, align='C')
        fill_color = red if ar=="regular" else blue if ar=="reverse" else white
        pdf.set_fill_color(*fill_color)
        pdf.cell(20, 10, txt="up" if ar=="regular" else "down" if ar=="reverse" else "-" , ln=True, border=1, align='C', fill=True)
        pdf.ln(5)
    def analyze_and_add_market_report(self, pdf, idx):
        c1 = self.markets_analysis[idx]["cross1"]
        c2 = self.markets_analysis[idx]["cross2"]
        ar = self.markets_analysis[idx]["arrange"]
        price = self.markets_analysis[idx]["price"]
        rate = self.markets_analysis[idx]["rate_change"]
        
        trend_signal = [0,0]
        if c1 == "golden cross":
            trend_signal[0] += 1
        else:
            trend_signal[1] += 1
        if c2 == "golden cross":
            trend_signal[0] += 1
        else:
            trend_signal[1] += 1
        if ar == "regular":
            trend_signal[0] += 1
        elif ar == "reverse":
            trend_signal[1] += 1
        
        pdf.multi_cell(0, 10, txt=f"Today's market price is {price:.2f} ({rate:.2f}%)")
        pdf.multi_cell(0, 10, 
                        txt=f"Out of 3 signals, there are {trend_signal[0]} signals of market uptrend({trend_signal[0]}/3) " \
                        f"and {trend_signal[1]} signals of market downtrend({trend_signal[1]}/3).")
        if trend_signal[0] > trend_signal[1]:
            pdf.multi_cell(0, 10, txt="Currently market is likely to be trending upward.")
            output = (1,0)
        elif trend_signal[1] < trend_signal[1]:
            pdf.multi_cell(0, 10, txt="Currently market is likely to be trending downward.")
            output = (0,1)
        pdf.ln(5)
        return output
    def add_overall_market_report(self, pdf, market_trend):
        cur_ir = self.markets_analysis[0]["current_rate"]
        avg_ir = self.markets_analysis[0]["average_rate"]
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, 
                           txt=f"Out of {len(self.markets_analysis)-1} market indexes, {market_trend[0]} of them are showing uptrend({market_trend[0]}/{len(self.markets_analysis)-1}) " \
                            f"and {market_trend[1]} of them are showing downtrend({market_trend[1]}/{len(self.markets_analysis)-1}).")
        if cur_ir > avg_ir:
            pdf.multi_cell(0, 10, txt="Also current interest rate is high, which can have negative impact on the market.")
        elif cur_ir < avg_ir:
            pdf.multi_cell(0, 10, txt="Also current interest rate is low, which can have positive impact on the market.")
        if market_trend[0] > market_trend[1]:
            pdf.multi_cell(0, 10, txt="In total, current market is likely to be trending upward. At times of uptrend, having 50% stocks and 50% cash is recommended.")
        elif market_trend[1] < market_trend[1]:
            pdf.multi_cell(0, 10, txt="In total, current market is likely to be trending downward. At times of uptrend, having 20% stocks and 80% cash is recommended.")
        pdf.ln(5)
    def add_finance_idx_table(self,pdf, idx):
        per = self.stocks_analysis[idx]["per"]
        pbr = self.stocks_analysis[idx]["pbr"]
        eps = self.stocks_analysis[idx]["eps"]
        roe = self.stocks_analysis[idx]["roe"]
        avg_per = self.stocks_analysis[idx]["average_per"]
        avg_pbr = self.stocks_analysis[idx]["average_pbr"]
        avg_eps = self.stocks_analysis[idx]["average_eps"]
        avg_roe = self.stocks_analysis[idx]["average_roe"]

        pdf.set_fill_color(*grey)
        pdf.cell(30, 10, txt="", ln=False, border=1, align='L', fill=True)
        pdf.cell(70, 10, txt="Current", ln=False, border=1, align='C', fill=True)
        pdf.cell(70, 10, txt="Average", ln=False, border=1, align='C', fill=True)
        pdf.cell(20, 10, txt="Value", ln=True, border=1, align='C', fill=True)

        pdf.cell(30, 10, txt=" PER:", ln=False, border=1, align='L',)
        if per != None:
            pdf.cell(70, 10, txt=f"{per:.2f}", ln=False, border=1, align='C')
            pdf.cell(70, 10, txt=f"{avg_per:.2f}", ln=False, border=1, align='C')
            fill_color = blue if per>avg_per else red if per<avg_per else white
            pdf.set_fill_color(*fill_color)
            pdf.cell(20, 10, txt="over" if per>avg_per else "under" if per<avg_per else "-" , ln=True, border=1, align='C', fill=True)
        else:
            pdf.cell(140, 10, txt=str("not found"), ln=False, border=1, align='C')
            pdf.cell(20, 10, txt="-" , ln=True, border=1, align='C')
        
        pdf.cell(30, 10, txt=" PBR:", ln=False, border=1, align='L',)
        if pbr != None:
            pdf.cell(70, 10, txt=f"{pbr:.2f}", ln=False, border=1, align='C')
            pdf.cell(70, 10, txt=f"{avg_pbr:.2f}", ln=False, border=1, align='C')
            fill_color = blue if pbr>avg_pbr else red if pbr<avg_pbr else white
            pdf.set_fill_color(*fill_color)
            pdf.cell(20, 10, txt="over" if pbr>avg_pbr else "under" if pbr<avg_pbr else "-" , ln=True, border=1, align='C', fill=True)
        else:
            pdf.cell(140, 10, txt=str("not found"), ln=False, border=1, align='C')
            pdf.cell(20, 10, txt="-" , ln=True, border=1, align='C')
        
        pdf.cell(30, 10, txt=" EPS:", ln=False, border=1, align='L',)
        if eps != None:
            pdf.cell(70, 10, txt=f"{eps:.2f}", ln=False, border=1, align='C')
            pdf.cell(70, 10, txt=f"{avg_eps:.2f}", ln=False, border=1, align='C')
            fill_color = red if eps>avg_eps else blue if eps<avg_eps else white
            pdf.set_fill_color(*fill_color)
            pdf.cell(20, 10, txt="under" if eps>avg_eps else "over" if eps<avg_eps else "-" , ln=True, border=1, align='C', fill=True)
        else:
            pdf.cell(140, 10, txt=str("not found"), ln=False, border=1, align='C')
            pdf.cell(20, 10, txt="-" , ln=True, border=1, align='C')
        
        pdf.cell(30, 10, txt=" ROE:", ln=False, border=1, align='L',)
        if roe != None:
            pdf.cell(70, 10, txt=f"{roe:.2f}", ln=False, border=1, align='C')
            pdf.cell(70, 10, txt=f"{avg_roe:.2f}", ln=False, border=1, align='C')
            fill_color = red if roe>avg_roe else blue if roe<avg_roe else white
            pdf.set_fill_color(*fill_color)
            pdf.cell(20, 10, txt="under" if roe>avg_roe else "over" if roe<avg_roe else "-" , ln=True, border=1, align='C', fill=True)
        else:
            pdf.cell(140, 10, txt=str("not found"), ln=False, border=1, align='C')
            pdf.cell(20, 10, txt="-" , ln=True, border=1, align='C')
        pdf.ln(5)
    def add_stock_report(self, pdf, idx):
        c1 = self.stocks_analysis[idx]["cross1"]
        c2 = self.stocks_analysis[idx]["cross2"]
        ar = self.stocks_analysis[idx]["arrange"]
        per = self.stocks_analysis[idx]["per"]
        pbr = self.stocks_analysis[idx]["pbr"]
        eps = self.stocks_analysis[idx]["eps"]
        roe = self.stocks_analysis[idx]["roe"]
        avg_per = self.stocks_analysis[idx]["average_per"]
        avg_pbr = self.stocks_analysis[idx]["average_pbr"]
        avg_eps = self.stocks_analysis[idx]["average_eps"]
        avg_roe = self.stocks_analysis[idx]["average_roe"]
        price = self.stocks_analysis[idx]["price"]
        rate = self.stocks_analysis[idx]["rate_change"]
        
        trend_signal = [0,0,0,0]
        if c1 == "golden cross":
            trend_signal[0] += 1
        else:
            trend_signal[1] += 1
        if c2 == "golden cross":
            trend_signal[0] += 1
        else:
            trend_signal[1] += 1
        if ar == "regular":
            trend_signal[0] += 1
        elif ar == "reverse":
            trend_signal[1] += 1
        if per != None:
            if per > avg_per:
                trend_signal[2] += 1
            elif per < avg_per:
                trend_signal[3] += 1
        if pbr != None:
            if pbr > avg_pbr:
                trend_signal[2] += 1
            elif pbr < avg_pbr:
                trend_signal[3] += 1
        if eps != None:
            if eps < avg_eps:
                trend_signal[2] += 1
            elif eps > avg_eps:
                trend_signal[3] += 1
        if roe != None:
            if roe < avg_roe:
                trend_signal[2] += 1
            elif roe > avg_roe:
                trend_signal[3] += 1
        pdf.multi_cell(0, 10, txt=f"Today's stock price is {price:.2f} USD ({rate:.2f}%)")
        pdf.multi_cell(0, 10, 
                        txt=f"Out of 3 signals, there are {trend_signal[0]} signals of stock uptrend({trend_signal[0]}/3) " \
                        f"and {trend_signal[1]} signals of stock downtrend({trend_signal[1]}/3). " \
                        f"Out of 4 financial indexes, {trend_signal[2]} indexes suggest this company is overvalued({trend_signal[2]}/4) " \
                        f"and {trend_signal[3]} indexes suggest this company is undervalued({trend_signal[3]}/4).")
        if trend_signal[0] > trend_signal[1]:
            pdf.multi_cell(0, 10, txt="Currently stock is likely to be trending upward.")
        elif trend_signal[0] < trend_signal[1]:
            pdf.multi_cell(0, 10, txt="Currently stock is likely to be trending downward.")
        if trend_signal[2] > trend_signal[3]:
            pdf.multi_cell(0, 10, txt="Financial indexes show that this company is overevaluated.")
        elif trend_signal[2] < trend_signal[3]:
            pdf.multi_cell(0, 10, txt="Financial indexes show that this company is underevaluated.")
        pdf.ln(5)
    def generate(self, pdf):
        pdf.add_page()
        self.head(pdf)
        self.subtitle1(pdf,"1. Market Analysis")
        interest_symbol = self.markets_analysis[0]["name"]
        interest_name = get_symbol_info(interest_symbol)["shortName"]
        self.subtitle2(pdf, f"1.1. Interest Rate ({interest_name})")
        
        self.subtitle3(pdf,"(a) 1 Month, 3 Months, 1 Year Chart")
        self.add_charts(pdf,interest_symbol,"market")
        
        self.subtitle3(pdf,"(b) Table")
        self.add_interest_table(pdf)
        
        self.subtitle3(pdf, "(c) Report")
        self.add_interest_report(pdf)
        
        market_trend = [0,0]
        for i in range(1,len(self.markets_analysis)):
            market_symbol = self.markets_analysis[i]["name"]
            market_name = get_symbol_info(market_symbol)['shortName']
            self.subtitle2(pdf, f"1.{i+1}. {market_name}")
            
            self.subtitle3(pdf,"(a) 1 Month, 3 Months, 1 Year Chart")
            self.add_charts(pdf,market_symbol,"market")

            self.subtitle3(pdf,"(b) Table")
            self.add_trend_table(pdf,"market",i)

            self.subtitle3(pdf, "(c) Report")
            up_signal, down_signal = self.analyze_and_add_market_report(pdf, i)
            market_trend[0]+=up_signal
            market_trend[1]+=down_signal
            
        self.subtitle2(pdf,f"1.{len(self.markets_analysis)+1}. Market Overall")
        self.add_overall_market_report(pdf,market_trend)
        
        pdf.add_page()
        self.subtitle1(pdf,"2. Stock Analysis")
        
        for i in range(0,len(self.stocks_analysis)):
            stock_symbol = self.stocks_analysis[i]["name"]
            stock_name = get_symbol_info(stock_symbol)['shortName']
            self.subtitle2(pdf,f"2.{i+1}. {stock_name}")
            
            self.subtitle3(pdf,"(a) 1 Month, 3 Months, 1 Year Chart")
            self.add_charts(pdf,stock_symbol,"stock")

            self.subtitle3(pdf,"(b) Table")
            self.add_trend_table(pdf,"stock",i)
            self.add_finance_idx_table(pdf,i)            

            self.subtitle3(pdf, "(c) Report")
            self.add_stock_report(pdf,i)
    
    def export(self, output_path):
        pdf = FPDF()
        self.generate(pdf)
        os.makedirs(f"log/reports", exist_ok=True)
        pdf.output(output_path)

def export_report():
    markets, m_symbols, stocks, s_symbols = setup_data()
    markets_analysis, stocks_analysis = analyze_data(markets, m_symbols, stocks, s_symbols)

    cur_date = datetime.today().strftime("%Y-%m-%d")
    report_name = f"{cur_date}_정기리포트.pdf"
    reportGenerator = ReportGenerator("Daily Report", cur_date, markets_analysis, stocks_analysis, f"log/charts/{cur_date}/")
    reportGenerator.export(f"log/reports/{report_name}")

if __name__ == "__main__":
    export_report()