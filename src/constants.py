from datetime import datetime, timedelta

SYMBOLS = [
    {"name": "TVBETETF.RO", "currency": "RON", "country": "RO", "title": "BET Tradeville"},
    {"name": "ROX.DE",      "currency": "EUR", "country": "RO", "title": "Expat Romania BET - BK UCITS"},
    {"name": "EPOL",        "currency": "USD", "country": "PL", "title": "iShares MSCI Poland"},
    {"name": "PLX.DE",      "currency": "EUR", "country": "PL", "title": "Expat Poland WIG20 UCITS"},
    {"name": "BGX.DE",      "currency": "EUR", "country": "BG", "title": "Expat Bulgaria SOFIX UCITS"},
    {"name": "LEER.DE",     "currency": "EUR", "country": "EU", "title": "Amundi MSCI Eastern Europe Ex Russia UCITS"},
    {"name": "TUR",         "currency": "USD", "country": "TR", "title": "iShares MSCI Turkey"}, 
    {"name": "TURP.XC",     "currency": "EUR", "country": "TR", "title": "Amundi MSCI Turkey UCITS"},
    {"name": "ITKYA.XC",    "currency": "EUR", "country": "TR", "title": "iShares MSCI Turkey UCITS"},
    {"name": "GREK",        "currency": "USD", "country": "GR", "title": "Global X MSCI Greece"},
    {"name": "LYMH.DE",     "currency": "EUR", "country": "GR", "title": "Amundi MSCI Greece UCITS"},
    {"name": "CZX.DE",      "currency": "EUR", "country": "CZ", "title": "Expat Czech PX UCITS"},
    {"name": "SK9A.DE",     "currency": "EUR", "country": "SK", "title": "Expat Slovakia Sax UCITS"},
    {"name": "HUBE.DE",     "currency": "EUR", "country": "HU", "title": "Expat Hungary BUX UCITS"},
    {"name": "ECDC.DE",     "currency": "EUR", "country": "HR", "title": "Expat Croatia Crobex UCITS"},
    {"name": "ESNB.DE",     "currency": "EUR", "country": "RS", "title": "Expat Serbia Belex15 UCITS"},
    {"name": "MKK1.DE",     "currency": "EUR", "country": "MK", "title": "Expat Macedonia Mbi10 UCITS"},
    {"name": "SLQX.DE",     "currency": "EUR", "country": "SI", "title": "Expat Slovenia SBI Top UCITS"},
]
CURRENCIES_NONEUR = ["RON", "USD"]
TIME_WINDOW_DAYS = 4000
START_DATE = datetime.now() - timedelta(days=TIME_WINDOW_DAYS)
END_DATE = datetime.now()

