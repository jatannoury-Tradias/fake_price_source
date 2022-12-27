from app.models.currency import Currency

currencies = [
    Currency("EUR", "Euro", 2),
    Currency("TKN", "TestToken", 0)
]

currency_dict = {currency.currency_code: currency for currency in currencies}
