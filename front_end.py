from flask import Flask, render_template, request, url_for, redirect
from AllinOne import *
from influx_loading_search_stock import *
from alpaca_news_search import *
from Config import *
app = Flask(__name__)
from alpaca.trading.client import TradingClient, OrderRequest

@app.route("/")
def main():
    return render_template('index.html')


@app.route("/search_company")
def search_company():
    return render_template('search_company.html')


@app.route('/return_company', methods = ['GET', 'POST'])
def CompanySearchResult():
    form = request.form

    # headings = ('name', 'symbol','exchange','asset_class','status','tradable','marginable','shortable','easy_to_borrow','fractionable')
    headings = ('Name', 'Symbol','Exchange','Asset Class','Status','Tradable','Marginable','Shortable','Easy_to_borrow','Fractionable')

    inputDic = {}

    if(form["compName"] != ''): inputDic['name'] = form["compName"]
    if(form["compSymbol"] != ''): inputDic['symbol'] = form["compSymbol"]
    if(form["compExchange"] != ''): inputDic['exchange'] = form["compExchange"]

    createIndex()# need to create index before doing text search, but we already have one.

    return render_template('UglyCompanies2.html', headings = headings, data = search(inputDic))


@app.route("/search_news")
def search_the_news():
    return render_template('search_news.html')

@app.route("/return_news", methods = ['GET', 'POST'])
def newsSearchResult():
    form = request.form
    # headings = ('Summary', 'Source', 'Author', 'Time')
    headings = ('News')

    # print(form.get("newsDate"))
    date_input = form.get("newsDate")
    symbol_input = form.get("newsSymbol")
    if date_input == '':
        result = get_stock_news(symbol=symbol_input)
    elif symbol_input != '':
        result = get_stock_news(symbol=symbol_input, date=date_input)
    else:
        result = get_stock_news_date(date=date_input)

    return render_template('NewsTable.html', data = result)


@app.route("/get_stock")
def get_stock():
    return render_template('get_stock.html')

@app.route('/return_stock', methods = ['GET', 'POST'])
def StockSearchResult():

    form = request.form

    # headings = ('_time','_measurement','close','high','low','open','trade_count', 'volume', 'vwap')
    headings = ('Time', 'Measurement', 'Close', 'High', 'Low', 'Open', 'Trade Count', 'Volume', 'Vwap')

    inputDic = {
        'stock': form["stock"],
        'startTime': form["startTime"],
        'endTime': form["endTime"]
    }

    first_result = get_stock_price_json(inputDic)#unprocessed json from api.
    second_result = processJson(first_result)#processed, formatted json

    print(json.dumps(json.loads(first_result), indent=2)) # prettyprint for json
    # print(second_result)

    return render_template('StockTable.html', headings = headings, data = second_result)


@app.route("/make_order")
def search_news():
    return render_template('make_order.html')


@app.route("/submit_Order", methods = ['GET', 'POST'])
def submit_Order():
    form = request.form
    print(str(form))
    symbol = form['tradeSymbol']
    position = form['tradePosition']
    number = int(form['tradeNumber'])


    API_NAME = 'PK4KNHN1288FU75AUBDI'
    API_KEY = '2pfsnioo6cjRVs4PqVlPHKd2WRl47yndffIVqQpj'
    trading_client = TradingClient(API_NAME, API_KEY)

    order_request = OrderRequest(symbol=symbol, qty=number, side=position, type="market", time_in_force="day")
    order_info = trading_client.submit_order(order_request)
    order_info = order_info.dict()
    account = trading_client.get_account()
    acc = account.dict()
    log_trade(acc, order_info, symbol)
    # print("you submitted an order: SYMBOL: " + symbol +", POSITION: " + position + ",Number: " + number )
    return render_template('make_order.html')










if __name__ == "__main__":
    app.run()






