import platform
import aiohttp
import asyncio
import sys
from datetime import timedelta
from datetime import date

async def determiner(currency):
    count = 0
    for el in  ['AUD', 'AZN', 'BYN', 'CAD', 'CHF', 'CNY', 'CZK', 'DKK', 'EUR', 'GBP', 'GEL', 'HUF', 'ILS', 'JPY', 'KZT', 'MDL', 'NOK', 'PLN', 'SEK', 'SGD', 'TMT', 'TRY', 'UAH', 'USD', 'UZS', 'XAU']:
        if el == currency:
            break
        else:
            count += 1
      
    currency_info = data['exchangeRate'][count]
    currency_format = {"sale": currency_info['saleRateNB'], "purchase": currency_info['purchaseRateNB']}
    return currency_format

async def fetch_currency(session, days, currencies):
    currencies_list = []
    for day in range(days, 0, -1):
        today = date.today() - timedelta(days=day)
        formatted_date = today.strftime('%d.%m.%Y')
        async with session.get(f'https://api.privatbank.ua/p24api/exchange_rates?json&date={formatted_date}') as response:
            global data
            data = await response.json()
            currency_data = {currency: await determiner(currency) for currency in currencies}
            currencies_list.append({formatted_date: currency_data})
    return currencies_list 

async def main(days, currencies):
    async with aiohttp.ClientSession() as session:
        return await fetch_currency(session, days, currencies) 


if __name__ == "__main__":
    currencies = sys.argv[2::]
    valid_currencies = {'AUD', 'AZN', 'BYN', 'CAD', 'CHF', 'CNY', 'CZK', 'DKK', 'EUR', 'GBP', 'GEL', 'HUF', 'ILS', 'JPY', 'KZT', 'MDL', 'NOK', 'PLN', 'SEK', 'SGD', 'TMT', 'TRY', 'UAH', 'USD', 'UZS', 'XAU'}
    
    for el in currencies:
        if el not in valid_currencies:
            print("Неправильна валюта")
            sys.exit(1)

    try:
        days = int(sys.argv[1])
    except ValueError:
        print("Дні повинні бути цілим числом")
        sys.exit(1)
      
    if not 1 <= days <= 10:
        print("Дні повинні бути від 1 до 10")
        sys.exit(1)

    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main(days, currencies))
    print(r)
