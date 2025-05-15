from datetime import datetime, timedelta
import yfinance as yf

symbols = ["TVBETETF.RO", "EPOL", "BGX"]
start_date = datetime.now() - timedelta(days=5)
end_date = datetime.now()

data = yf.download(symbols, start=start_date, end=end_date)
dictdata = {key: dict(data)[key] for key in ...} #TODO
